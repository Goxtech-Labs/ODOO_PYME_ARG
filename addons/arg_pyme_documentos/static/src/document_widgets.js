/** @odoo-module **/
import { Component, onWillStart, proxy, useProps } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { standardWidgetProps } from "@web/views/widgets/standard_widget_props";
import { standardActionServiceProps } from "@web/webclient/actions/action_plugin";

const stateLabels = {pending:"Pendiente",partial:"Parcial",complete:"Completo",na:"No corresponde",unknown:"No determinado"};
export class DocumentHeader extends Component {
    static template="arg_pyme_documentos.DocumentHeader";
    props=useProps({...standardWidgetProps});
    setup() {this.action=useService("action");this.orm=useService("orm");}
    get number() {return this.props.record.data.arg_number || "Sin guardar";}
    get axes() {return this.props.record.data.arg_completion_axes || [];}
    label(state) {return stateLabels[state] || state;}
    stateIcon(state) {
        return {
            pending:"M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18 M12 7v5l3 2",
            partial:"M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18 M12 3v18 M12 8h5 M12 12h7 M12 16h5",
            complete:"M4 12l5 5L20 6",
            na:"M5 12h14",
            unknown:"M8 8a4 4 0 1 1 6 3.5L12 13v2 M12 19h.01",
        }[state] || "M5 12h14";
    }
    async openLinks() {
        const record=this.props.record;
        if (record.isNew) return;
        const action=await this.orm.call(record.resModel,"action_arg_links",[[record.resId]]);
        return this.action.doAction(action);
    }
}
registry.category("view_widgets").add("arg_document_header",{component:DocumentHeader,
    fieldDependencies:[{name:"arg_number",type:"char"},{name:"arg_completion_axes",type:"json"}]});

export class DocumentLinks extends Component {
    static template="arg_pyme_documentos.DocumentLinks";
    props=useProps({...standardActionServiceProps});
    state=proxy({number:"",groups:[],line_links:[]});
    setup() {
        this.orm=useService("orm");this.action=useService("action");
        onWillStart(async()=>{
            const params=this.props.action.params;
            Object.assign(this.state,await this.orm.call(params.model,"arg_document_links",[[params.id]]));
        });
    }
    open(model,id) {return this.action.doAction({type:"ir.actions.act_window",res_model:model,res_id:id,views:[[false,"form"]]});}
}
registry.category("actions").add("arg_pyme.document_links",DocumentLinks);
