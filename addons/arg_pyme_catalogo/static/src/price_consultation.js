/** @odoo-module **/
import { Component, onWillStart, onWillUnmount, proxy, t, useProps } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { standardActionServiceProps } from "@web/webclient/actions/action_plugin";
import { useSetupAction } from "@web/search/action_hook";
import { Dialog } from "@web/core/dialog/dialog";
import { DateTimeInput } from "@web/core/datetime/datetime_input";
import { deserializeDateTime, serializeDateTime, formatDateTime } from "@web/core/l10n/dates";

class PriceResult extends Component {
    static template = "arg_pyme_catalogo.PriceResult";
    props = useProps({data:t.object()});
    number(value) { return value===null || value===undefined ? "—" : new Intl.NumberFormat("es-AR",{maximumFractionDigits:4}).format(value); }
    when(value) { return value ? formatDateTime(deserializeDateTime(value)) : "Sin límite"; }
    kind(step) { return ({fixed:"Precio fijo",discount:"Descuento",markup:"Recargo",catalog:"Precio del catálogo"})[step.kind] || "Extensión nativa"; }
    scope(step) { return ({"0_product_variant":"Variante","1_product":"Plantilla","2_product_category":"Categoría","3_global":"General"})[step.scope] || "Catálogo"; }
    basis(step) { return ({fixed:"Importe fijo",list_price:"Catálogo y extras nativos",standard_price:"Costo nativo",pricelist:"Otra lista"})[step.basis] || "Extensión nativa"; }
}

export class PriceExplanationDialog extends Component {
    static template = "arg_pyme_catalogo.PriceExplanationDialog";
    static components = {Dialog, PriceResult};
    props = useProps({close:t.function(),productId:t.number(),pricelistId:t.number(),quantity:t.number(),date:t.string(),
        expectedToken:t.or([t.string(),t.boolean()]).optional(false),onDone:t.function().optional()});
    state = proxy({result:null,error:"",loading:true});
    setup() {
        this.orm=useService("orm");
        onWillUnmount(()=>this.props.onDone?.());
        onWillStart(async()=>{
            try {this.state.result=await this.orm.call("arg.pyme.price.consultation","explain",
                [this.props.productId,this.props.pricelistId,this.props.quantity,this.props.date],
                {expected_token:this.props.expectedToken});}
            catch(error) {this.state.error=error.data?.message||error.message;}
            finally {this.state.loading=false;}
        });
    }
}

class PriceChoiceDialog extends Component {
    static template = "arg_pyme_catalogo.PriceChoiceDialog";
    static components = {Dialog};
    props = useProps({close:t.function(),kind:t.string(),title:t.string(),choose:t.function(),templateId:t.number().optional()});
    state = proxy({rows:[],query:"",offset:0,count:0,loading:false,error:""});
    setup() {this.orm=useService("orm");this.request=0;onWillStart(()=>this.load(0));}
    async load(offset=0) {
        const request=++this.request;this.state.loading=true;this.state.error="";
        try {
            const result=await this.orm.call("arg.pyme.price.consultation","choices",
                [this.props.kind,this.state.query,offset,this.props.templateId||false]);
            if(request===this.request) Object.assign(this.state,result);
        } catch(error) {if(request===this.request) this.state.error=error.data?.message||error.message;}
        finally {if(request===this.request) this.state.loading=false;}
    }
    choose(value) {this.props.choose(value);this.props.close();}
}

export class PriceConsultation extends Component {
    static template = "arg_pyme_catalogo.PriceConsultation";
    static components = {DateTimeInput, PriceResult};
    props = useProps({...standardActionServiceProps});
    state = proxy({when:"",partner:null,product:null,pricelist:null,manualList:false,quantity:1,
        conditions:null,result:null,company:"",canConfigure:false,loading:false,error:""});
    setup() {
        this.orm=useService("orm");this.dialog=useService("dialog");this.action=useService("action");
        this.request=0;this.templateId=this.props.action.params?.template_id||false;
        useSetupAction({getLocalState:()=>({argPrice:{when:this.state.when,partnerId:this.state.partner?.id,
            productId:this.state.product?.id,pricelistId:this.state.pricelist?.id,manualList:this.state.manualList,
            quantity:this.state.quantity}})});
        onWillStart(async()=>{
            this.state.loading=true;
            try {
                const options=await this.orm.call("arg.pyme.price.consultation","options",[]);
                Object.assign(this.state,{when:options.when,company:options.company,canConfigure:options.can_configure});
                const saved=this.props.state?.argPrice;
                if(saved) Object.assign(this.state,{when:saved.when,quantity:saved.quantity,manualList:saved.manualList});
                else if(this.props.action.params?.pricelist_id) this.state.manualList=true;
                const partnerId=saved?.partnerId||this.props.action.params?.partner_id;
                if(partnerId) {
                    this.state.conditions=await this.orm.call("arg.pyme.price.consultation","defaults",[partnerId]);
                    this.state.partner=this.state.conditions.partner;
                    if(!this.state.manualList) this.state.pricelist=this.state.conditions.pricelist;
                }
                const productId=saved?.productId||this.props.action.params?.product_id;
                if(productId) this.state.product=await this.orm.call("arg.pyme.price.consultation","reference",["product",productId]);
                const pricelistId=saved ? ((saved.manualList || !partnerId) ? saved.pricelistId : false)
                    : this.props.action.params?.pricelist_id;
                if(pricelistId) this.state.pricelist=await this.orm.call("arg.pyme.price.consultation","reference",["pricelist",pricelistId]);
            } catch(error) {this.state.error=error.data?.message||error.message;}
            finally {this.state.loading=false;}
        });
    }
    get whenValue() {return this.state.when ? deserializeDateTime(this.state.when) : false;}
    change(field,value) {this.state[field]=value;this.state.result=null;this.state.error="";++this.request;}
    whenChanged(value) {this.change("when",value?.isValid ? serializeDateTime(value) : "");}
    pick(kind) {
        if(this.state.loading) return;
        const props={kind,title:({partner:"Elegir cliente",product:"Elegir variante o producto",pricelist:"Elegir lista"})[kind],
            choose:value=>this.selected(kind,value)};
        if(kind==="product" && this.templateId) props.templateId=this.templateId;
        this.dialog.add(PriceChoiceDialog,props);
    }
    async selected(kind,value) {
        this.change(kind,value);
        if(kind==="pricelist") this.state.manualList=true;
        if(kind!=="partner") return;
        this.state.conditions=null;
        if(!this.state.manualList) this.state.pricelist=null;
        const request=++this.request;this.state.loading=true;
        try {
            const data=await this.orm.call("arg.pyme.price.consultation","defaults",[value.id]);
            if(request!==this.request) return;
            this.state.conditions=data;
            if(!this.state.manualList) this.state.pricelist=data.pricelist;
        } catch(error) {if(request===this.request) this.state.error=error.data?.message||error.message;}
        finally {if(request===this.request) this.state.loading=false;}
    }
    clearPartner() {this.change("partner",null);this.state.conditions=null;if(!this.state.manualList)this.state.pricelist=null;}
    useCustomerList() {this.change("pricelist",this.state.conditions?.pricelist||null);this.state.manualList=false;}
    async consult() {
        if(this.state.loading) return;
        if(!this.state.product || !this.state.when) {this.state.error="Elegí un producto y una fecha válidos.";return;}
        const request=++this.request;this.state.loading=true;this.state.error="";this.state.result=null;
        try {
            const data=await this.orm.call("arg.pyme.price.consultation","explain",[],{
                product_id:this.state.product.id,pricelist_id:this.state.pricelist?.id||false,
                quantity:Number(this.state.quantity),partner_id:this.state.partner?.id||false,at:this.state.when});
            if(request===this.request) this.state.result=data;
        } catch(error) {if(request===this.request) this.state.error=error.data?.message||error.message;}
        finally {if(request===this.request) this.state.loading=false;}
    }
    async open(method,id) {
        if(this.state.loading || !id) return;
        try {await this.action.doAction(await this.orm.call("arg.pyme.price.consultation",method,[id]));}
        catch(error) {this.state.error=error.data?.message||error.message;}
    }
    rules() {return this.open("open_rules",this.state.pricelist?.id);}
    partner() {return this.open("open_partner",this.state.partner?.id);}
}
registry.category("actions").add("arg_pyme.price_consultation",PriceConsultation);
