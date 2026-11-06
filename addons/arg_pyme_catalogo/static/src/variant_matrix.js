/** @odoo-module **/
import { Component, onWillStart, proxy, t, useProps } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { standardActionServiceProps } from "@web/webclient/actions/action_plugin";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { Dialog } from "@web/core/dialog/dialog";

class VariantValuePicker extends Component {
    static template = "arg_pyme_catalogo.VariantValuePicker";
    static components = { Dialog };
    props = useProps({close:t.function(), templateId:t.number(), line:t.object(), choose:t.function()});
    state = proxy({rows:[], query:"", offset:0, count:0, loading:false, error:""});
    setup() { this.orm=useService("orm"); this.request=0; onWillStart(()=>this.load(0)); }
    async load(offset=0) {
        const request=++this.request; this.state.loading=true; this.state.error="";
        try {
            const data=await this.orm.call("arg.pyme.variant.matrix","values",[this.props.templateId,this.props.line.id,this.state.query,offset]);
            if (request===this.request) Object.assign(this.state,data);
        } catch(error) { if(request===this.request) this.state.error=error.data?.message||error.message; }
        finally { if(request===this.request) this.state.loading=false; }
    }
    select(value) { this.props.choose(value); this.props.close(); }
}

export class VariantMatrix extends Component {
    static template = "arg_pyme_catalogo.VariantMatrix";
    props = useProps({...standardActionServiceProps});
    state = proxy({templates:[], templateQuery:"", templateOffset:0, templateCount:0,
        template:null, lines:[], x:false, y:false, fixed:{}, xQuery:"", yQuery:"",
        xOffset:0, yOffset:0, xCount:0, yCount:0, rows:[], columns:[], selected:{},
        loading:false, error:"", company:""});
    setup() {
        this.orm=useService("orm"); this.action=useService("action");
        this.dialog=useService("dialog"); this.notification=useService("notification");
        this.request=0; this.templateRequest=0;
        onWillStart(async()=>{
            await this.searchTemplates();
            const id=this.props.action.params?.template_id;
            if(id) await this.selectTemplate(id);
        });
    }
    get fixedLines() { return this.state.lines.filter(line=>line.id!==this.state.x && line.id!==this.state.y); }
    get selection() { return Object.values(this.state.selected); }
    number(value) { return value===null || value===undefined ? "—" : new Intl.NumberFormat("es-AR",{maximumFractionDigits:4}).format(value); }
    async searchTemplates(offset=0) {
        const request=++this.templateRequest;
        try {
            const data=await this.orm.call("arg.pyme.variant.matrix","templates",[this.state.templateQuery,offset]);
            if(request===this.templateRequest) Object.assign(this.state,{templates:data.rows,templateOffset:data.offset,templateCount:data.count});
        } catch(error) { this.state.error=error.data?.message||error.message; }
    }
    async selectTemplate(id) {
        if(this.state.template?.id===id || this.state.loading) return;
        if(this.selection.length) {
            this.dialog.add(ConfirmationDialog,{title:"Cambiar producto",body:"Se descartará la selección de etiquetas del producto anterior.",
                confirmLabel:"Cambiar producto",cancelLabel:"Conservar selección",confirm:()=>this.configure(id)});
        } else await this.configure(id);
    }
    async configure(id) {
        const request=++this.request; this.state.loading=true; this.state.error="";
        try {
            const data=await this.orm.call("arg.pyme.variant.matrix","configure",[id]);
            if(request!==this.request) return;
            Object.assign(this.state,{template:data.template,lines:data.lines,x:data.x,y:data.y,
                fixed:{},selected:{},rows:[],columns:[],xQuery:"",yQuery:"",company:data.company});
            this.state.loading=false; await this.load(0,0);
        } catch(error) { if(request===this.request) this.state.error=error.data?.message||error.message; }
        finally { if(request===this.request) this.state.loading=false; }
    }
    async load(xOffset=this.state.xOffset,yOffset=this.state.yOffset) {
        if(!this.state.template) return;
        const request=++this.request; this.state.loading=true; this.state.error="";
        const fixed={}; for(const line of this.fixedLines) if(this.state.fixed[String(line.id)]) fixed[String(line.id)]=this.state.fixed[String(line.id)].id;
        try {
            const data=await this.orm.call("arg.pyme.variant.matrix","page",[this.state.template.id,this.state.x,this.state.y,fixed,
                xOffset,yOffset,this.state.xQuery,this.state.yQuery]);
            if(request!==this.request) return;
            Object.assign(this.state,{rows:data.rows,columns:data.columns,fixed:data.fixed,xOffset:data.x_offset,
                yOffset:data.y_offset,xCount:data.x_count,yCount:data.y_count,company:data.company});
        } catch(error) { if(request===this.request) {this.state.error=error.data?.message||error.message;this.state.rows=[];this.state.columns=[];} }
        finally { if(request===this.request) this.state.loading=false; }
    }
    async axis(which,event) {
        const value=Number(event.target.value)||false, other=which==="x"?"y":"x";
        if(value && value===this.state[other]) this.state[other]=this.state[which];
        this.state[which]=value;
        const fixed={};for(const line of this.fixedLines) if(this.state.fixed[String(line.id)]) fixed[String(line.id)]=this.state.fixed[String(line.id)];
        this.state.fixed=fixed; await this.load(0,0);
    }
    pick(line) {
        const templateId=this.state.template.id;
        this.dialog.add(VariantValuePicker,{templateId,line,choose:value=>{
            if(this.state.template?.id!==templateId) return;
            this.state.fixed[String(line.id)]={...value,line_name:line.name}; this.load(0,0);
        }});
    }
    toggle(cell,event) {
        if(event.target.checked) {
            if(this.selection.length>=200) {event.target.checked=false;this.notification.add("Hasta 200 variantes por preparación de etiquetas.",{type:"warning"});return;}
            this.state.selected[String(cell.id)]={id:cell.id,name:cell.name,code:cell.code};
        } else delete this.state.selected[String(cell.id)];
    }
    async command(method,args=[]) {
        if(this.state.loading || !this.state.template) return;
        try { const action=await this.orm.call("arg.pyme.variant.matrix",method,[this.state.template.id,...args]);await this.action.doAction(action); }
        catch(error) { this.notification.add(error.data?.message||error.message,{type:"danger"}); }
    }
    open(cell) { return this.command("open_variant",[cell.id]); }
    prices() { return this.command("prices"); }
    labels() { return this.command("labels",[this.selection.map(product=>product.id)]); }
    remove(id) { delete this.state.selected[String(id)]; }
}
registry.category("actions").add("arg_pyme.variant_matrix",VariantMatrix);
