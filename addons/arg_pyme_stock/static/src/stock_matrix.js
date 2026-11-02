/** @odoo-module **/
import {Component,onWillStart,proxy,t,useProps} from "@odoo/owl";
import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";
import {standardActionServiceProps} from "@web/webclient/actions/action_plugin";
class StockMatrix extends Component {
 static template="arg_pyme_stock.Matrix";
 props=useProps({...standardActionServiceProps});
 state=proxy({warehouses:[],locations:[],warehouse:0,location:0,query:"",rows:[],count:0,offset:0,error:"",loading:false,asOf:"",company:""});
 setup(){this.orm=useService("orm");this.request=0;onWillStart(async()=>{const data=await this.orm.call("arg.pyme.stock.matrix","options",[]);Object.assign(this.state,data);this.state.warehouse=data.warehouses[0]?.id||0;await this.load(0);});}
 format(value){return new Intl.NumberFormat("es-AR",{maximumFractionDigits:4}).format(value);}
 async load(offset=0){if(!this.state.warehouse){this.state.rows=[];this.state.error="Configurá un depósito de la compañía.";return;}const request=++this.request;this.state.loading=true;this.state.error="";try{const data=await this.orm.call("arg.pyme.stock.matrix","page",[Number(this.state.warehouse),Number(this.state.location)||false,this.state.query,offset]);if(request===this.request)Object.assign(this.state,{rows:data.rows,count:data.count,offset:data.offset,asOf:data.as_of,company:data.company});}catch(error){if(request===this.request)this.state.error=error.data?.message||error.message;}finally{if(request===this.request)this.state.loading=false;}}
}
registry.category("actions").add("arg_pyme.stock_matrix",StockMatrix);
