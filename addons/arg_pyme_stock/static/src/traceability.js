/** @odoo-module **/
import { Component, onWillStart, proxy, t, useProps } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { standardActionServiceProps } from "@web/webclient/actions/action_plugin";
import { useSetupAction } from "@web/search/action_hook";
import { Dialog } from "@web/core/dialog/dialog";
import { DateTimeInput } from "@web/core/datetime/datetime_input";
import { deserializeDateTime, serializeDateTime, formatDateTime } from "@web/core/l10n/dates";

class TraceChoiceDialog extends Component {
    static template = "arg_pyme_stock.TraceChoiceDialog";
    static components = {Dialog};
    props = useProps({close:t.function(),kind:t.string(),choose:t.function(),productId:t.number().optional()});
    state = proxy({rows:[],query:"",offset:0,count:0,loading:false,error:""});
    setup() {this.orm=useService("orm");this.request=0;onWillStart(()=>this.load(0));}
    async load(offset=0) {
        const request=++this.request;this.state.loading=true;this.state.error="";
        try {
            const result=await this.orm.call("arg.pyme.stock.trace","choices",
                [this.props.kind,this.state.query,offset,this.props.productId||false]);
            if(request===this.request) Object.assign(this.state,result);
        } catch(error) {if(request===this.request)this.state.error=error.data?.message||error.message;}
        finally {if(request===this.request)this.state.loading=false;}
    }
    choose(row) {this.props.choose(row);this.props.close();}
    get title() {return this.props.kind==="lot" ? "Elegir serie o lote" : "Elegir producto rastreable";}
}

export class StockTrace extends Component {
    static template = "arg_pyme_stock.StockTrace";
    static components = {DateTimeInput};
    props = useProps({...standardActionServiceProps});
    state = proxy({company:"",canCreate:false,product:null,lot:null,start:"",end:"",result:null,quantities:null,
        loading:false,qLoading:false,opening:false,error:"",qError:""});
    setup() {
        this.orm=useService("orm");this.dialog=useService("dialog");this.action=useService("action");
        this.request=0;this.quantRequest=0;
        useSetupAction({getLocalState:()=>({argTrace:{productId:this.state.product?.id,lotId:this.state.lot?.id,
            start:this.state.start,end:this.state.end,offset:this.state.result?.history.offset||0,
            quantOffset:this.state.quantities?.offset||0,
            applied:this.state.result ? {start:this.state.result.start,end:this.state.result.end} : null}})});
        onWillStart(async()=>{
            try {
                const options=await this.orm.call("arg.pyme.stock.trace","options",[]);
                this.state.company=options.company;this.state.canCreate=options.can_create;
                const saved=this.props.state?.argTrace;
                if(saved){this.state.start=saved.start;this.state.end=saved.end;}
                const lotId=saved ? saved.lotId : this.props.action.params?.lot_id;
                if(lotId) {
                    this.state.lot=await this.orm.call("arg.pyme.stock.trace","reference",["lot",lotId]);
                    this.state.product=this.state.lot.product.id ? this.state.lot.product : null;
                    await this.load(saved?.offset||0,saved?.applied||null);
                    if(saved?.quantOffset) await this.quantPage(saved.quantOffset);
                } else if(saved?.productId) {
                    this.state.product=await this.orm.call("arg.pyme.stock.trace","reference",["product",saved.productId]);
                }
            } catch(error) {this.state.error=error.data?.message||error.message;}
        });
    }
    get busy(){return this.state.loading||this.state.qLoading||this.state.opening;}
    get startValue(){return this.state.start ? deserializeDateTime(this.state.start) : false;}
    get endValue(){return this.state.end ? deserializeDateTime(this.state.end) : false;}
    get dirty(){return !!this.state.result && ((this.state.result.start||"")!==this.state.start || (this.state.result.end||"")!==this.state.end);}
    when(value){return value ? formatDateTime(deserializeDateTime(value)) : "Sin límite";}
    number(value){return value===null || value===undefined ? "—" : new Intl.NumberFormat("es-AR",{maximumSignificantDigits:15}).format(value);}
    range(field,value){this.state[field]=value?.isValid ? serializeDateTime(value) : "";this.state.error="";}
    kind(row){
        if(row.return_of.status==="known")return "Devolución";
        if(row.inventory)return "Ajuste / inventario";
        if(row.scrap)return "Descarte";
        if(row.source_usage==="supplier")return "Recepción";
        if(row.destination_usage==="supplier")return "Salida a proveedor";
        if(row.destination_usage==="customer")return "Entrega";
        if(row.source_usage==="customer")return "Entrada desde cliente";
        if(row.source_usage==="production")return "Entrada de producción";
        if(row.destination_usage==="production")return "Consumo de producción";
        if(["internal","transit"].includes(row.source_usage)&&["internal","transit"].includes(row.destination_usage))return "Traslado";
        return "Movimiento nativo";
    }
    pick(kind){
        if(this.busy)return;
        const props={kind,choose:row=>this.selected(kind,row)};
        if(kind==="lot"&&this.state.product?.id)props.productId=this.state.product.id;
        this.dialog.add(TraceChoiceDialog,props);
    }
    async selected(kind,row){
        this.state.error="";this.state.result=null;this.state.quantities=null;
        if(kind==="product"){this.state.product=row;this.state.lot=null;return;}
        this.state.lot=row;this.state.product=row.product.id ? row.product : null;
        await this.load(0);
    }
    clearProduct(){if(this.busy)return;this.state.product=null;this.state.lot=null;this.state.result=null;this.state.quantities=null;}
    page(offset){return this.load(offset,{start:this.state.result.start,end:this.state.result.end});}
    async load(offset=0,range=null){
        if(this.busy)return;
        if(!this.state.lot){this.state.error="Elegí una serie o lote para consultar.";return;}
        const request=++this.request;this.state.loading=true;this.state.error="";this.state.qError="";
        try{
            const data=await this.orm.call("arg.pyme.stock.trace","page",[this.state.lot.id,offset],
                {start:(range ? range.start : this.state.start)||false,end:(range ? range.end : this.state.end)||false});
            if(request===this.request){this.state.result=data;this.state.lot=data.lot;
                this.state.product=data.lot.product.id ? data.lot.product : null;this.state.quantities=data.quantities;}
        }catch(error){if(request===this.request){this.state.error=error.data?.message||error.message;this.state.result=null;this.state.quantities=null;}}
        finally{if(request===this.request)this.state.loading=false;}
    }
    async quantPage(offset=0){
        if(this.busy||!this.state.lot)return;
        const request=++this.quantRequest;this.state.qLoading=true;this.state.qError="";
        try{
            const data=await this.orm.call("arg.pyme.stock.trace","quantities",[this.state.lot.id,offset]);
            if(request===this.quantRequest)this.state.quantities=data;
        }catch(error){if(request===this.quantRequest){this.state.qError=error.data?.message||error.message;this.state.quantities=null;}}
        finally{if(request===this.quantRequest)this.state.qLoading=false;}
    }
    async open(method,args){
        if(this.busy)return;this.state.opening=true;this.state.error="";
        try{await this.action.doAction(await this.orm.call("arg.pyme.stock.trace",method,args));}
        catch(error){this.state.error=error.data?.message||error.message;}
        finally{this.state.opening=false;}
    }
    createLot(){return this.open("create_lot",[this.state.product?.id||false]);}
    lotCard(){if(this.state.lot)return this.open("open_lot",[this.state.lot.id]);}
    advanced(){if(this.state.lot)return this.open("advanced",[this.state.lot.id]);}
    document(row){return this.open("open_document",[this.state.lot.id,row.id]);}
}
registry.category("actions").add("arg_pyme.stock_trace",StockTrace);
