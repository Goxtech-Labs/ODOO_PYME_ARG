/** @odoo-module **/
import { registry } from "@web/core/registry";
import { FormController } from "@web/views/form/form_controller";
import { formView } from "@web/views/form/form_view";
import { listView } from "@web/views/list/list_view";

export class ArgFormController extends FormController {
    get className() { return {...super.className, arg_document_form:true}; }
    async argSaveNew() { if (await this.saveButtonClicked()) return this.create(); }
    async argSaveClose() { if (await this.saveButtonClicked()) return this.env.config.historyBack(); }
    argBack() { return this.env.config.historyBack(); }
}
registry.category("views").add("arg_form", {...formView, Controller:ArgFormController,
    buttonTemplate:"arg_pyme_ui.DocumentButtons"});
// Native list model owns edits, pagination, keyboard navigation and dirty-row guards.
registry.category("views").add("arg_list", {...listView});
