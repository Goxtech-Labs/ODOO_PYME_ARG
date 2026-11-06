/** @odoo-module **/
import { Component, onWillStart, proxy, t, useProps } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { standardActionServiceProps } from "@web/webclient/actions/action_plugin";
import { useSetupAction } from "@web/search/action_hook";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { Dialog } from "@web/core/dialog/dialog";
class PriceReview extends Component {
    static template = "arg_pyme_catalogo.PriceReview";
    static components = { Dialog };
    props = useProps({close:t.function(), changes:t.array(t.any()), confirm:t.function()});
    state = proxy({busy:false});
    async apply() {
        if (this.state.busy) return;
        this.state.busy = true;
        try { await this.props.confirm(); this.props.close(); }
        finally { this.state.busy = false; }
    }
}
export class PriceMatrix extends Component {
    static template = "arg_pyme_catalogo.PriceMatrix";
    props = useProps({...standardActionServiceProps});
    state = proxy({rows:[], columns:[], lists:[], categories:[], selected:[], pending:{},
        query:"", kind:"", category:"", sale:false, purchase:false, quantity:1, date:"",
        offset:0, limit:30, count:0, loading:false, saving:false, canEdit:false, error:""});
    setup() {
        this.orm = useService("orm"); this.dialog = useService("dialog");
        this.notification = useService("notification"); this.action = useService("action");
        this.request = 0; this.operation = null;
        this.templateId = this.props.action.params?.template_id || false;
        this.templateName = this.props.action.params?.template_name || "";
        useSetupAction({beforeLeave:() => this.beforeLeave(),
            beforeUnload:event => {if (this.dirty) {event.preventDefault(); event.returnValue = "";}}});
        onWillStart(async () => {
            const data = await this.orm.call("arg.pyme.pricelist.matrix", "options", []);
            this.state.lists = data.lists; this.state.categories = data.categories;
            this.state.canEdit = data.can_edit; this.state.date = data.date;
            this.state.selected = data.lists.slice(0,5).map(p => p.id);
            await this.load(0);
        });
    }
    get changes() { return Object.values(this.state.pending); }
    get dirty() { return this.changes.length > 0; }
    key(row,col) { return `${row.id}:${col.id}`; }
    cell(row,col) { return row.cells[String(col.id)]; }
    value(row,col) { return this.state.pending[this.key(row,col)]?.price ?? this.cell(row,col).price; }
    format(value) { return value === null ? "—" : new Intl.NumberFormat("es-AR", {maximumFractionDigits:4}).format(value); }
    async load(offset=this.state.offset) {
        const request = ++this.request;
        this.state.loading = true; this.state.error = "";
        try {
            if (!this.state.selected.length) {this.state.rows=[]; this.state.columns=[]; this.state.count=0; return;}
            const data = await this.orm.call("arg.pyme.pricelist.matrix", "page", [[...this.state.selected],
                {query:this.state.query,kind:this.state.kind,category:this.state.category,sale:this.state.sale,purchase:this.state.purchase,
                 template_id:this.templateId},
                offset,Number(this.state.quantity),this.state.date]);
            if (request !== this.request) return;
            Object.assign(this.state,{rows:data.rows,columns:data.columns,count:data.count,offset:data.offset,limit:data.limit});
        } catch (error) { if (request === this.request) this.state.error = error.data?.message || error.message; }
        finally { if (request === this.request) this.state.loading=false; }
    }
    edit(row,col,event) {
        const cell=this.cell(row,col), value=event.target.value, amount=Number(value);
        if (!cell.editable || !this.state.canEdit || value.trim()==="" || !Number.isFinite(amount) || amount<0) {
            event.target.value=this.value(row,col);
            this.notification.add("Ingresá un precio no negativo.",{type:"warning"}); return;
        }
        const key=this.key(row,col), previous=this.state.pending[key];
        if (amount === (previous?.before ?? cell.price)) delete this.state.pending[key];
        else this.state.pending[key]={product_id:row.id,list_id:col.id,price:amount,
            token:previous?.token ?? cell.token,date:previous?.date ?? this.state.date,
            before:previous?.before ?? cell.price,name:row.name,code:row.code,list:col.name,currency:col.currency,unit:row.unit};
    }
    async toggleList(id,event) {
        const selected=[...this.state.selected];
        if (event.target.checked) {
            if (selected.length>=5) {event.target.checked=false; this.notification.add("Hasta cinco columnas por consulta.",{type:"info"}); return;}
            selected.push(id);
        } else selected.splice(selected.indexOf(id),1);
        this.state.selected=selected; await this.load(0);
    }
    review() {
        if (!this.dirty || this.state.saving || this.state.loading) return;
        const changes=this.changes.map(c=>({...c}));
        this.dialog.add(PriceReview,{changes,confirm:async()=>{
            this.state.saving=true;
            const payload=changes.map(({product_id,list_id,token,date,price})=>({product_id,list_id,token,date,price}));
            const signature=JSON.stringify(payload);
            if (this.operation?.signature!==signature) this.operation={signature,key:crypto.randomUUID()};
            try {
                const result=await this.orm.call("arg.pyme.pricelist.matrix","apply",[this.operation.key,payload]);
                for (const c of changes) delete this.state.pending[`${c.product_id}:${c.list_id}`];
                this.notification.add(`${result.count} precios guardados. Registro ${result.batch_id}.`,{type:"success"});
                await this.load();
            } finally {this.state.saving=false;}
        }});
    }
    discard() {
        this.dialog.add(ConfirmationDialog,{title:"Descartar precios pendientes",body:`Se descartarán ${this.changes.length} cambios sin guardar.`,
            confirmLabel:"Descartar",confirmClass:"btn-danger",cancelLabel:"Seguir editando",
            confirm:async()=>{this.state.pending={};this.operation=null;await this.load();}});
    }
    beforeLeave() {
        if (this.state.saving) return false;
        if (!this.dirty) return true;
        return new Promise(resolve=>this.dialog.add(ConfirmationDialog,{
            title:"Precios sin guardar",body:"Hay precios pendientes, incluso en páginas o columnas ocultas.",
            confirmLabel:"Descartar y salir",confirmClass:"btn-danger",cancelLabel:"Seguir editando",
            confirm:()=>{this.state.pending={};resolve(true);},cancel:()=>resolve(false),dismiss:()=>resolve(false)}));
    }
    advanced() {return this.action.doAction("arg_pyme_catalogo.action_pricelists");}
}
registry.category("actions").add("arg_pyme.price_matrix",PriceMatrix);
