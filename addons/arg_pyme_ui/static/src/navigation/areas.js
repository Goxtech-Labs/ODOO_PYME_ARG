/** @odoo-module **/
import { Component, useProps, proxy } from "@odoo/owl";
import { WebClient } from "@web/webclient/webclient";
import { patch } from "@web/core/utils/patch";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { session } from "@web/session";
import { standardActionServiceProps } from "@web/webclient/actions/action_plugin";

function firstAction(menu, service) {
    if (!menu) return null;
    if (menu.actionID) return menu;
    for (const id of menu.children || []) {
        const found = firstAction(service.getMenu(id), service);
        if (found) return found;
    }
    return null;
}
class ArgAreas extends Component {
    setup() { this.menu = useService("menu"); }
    get areas() {
        return (session.arg_pyme?.areas || []).map(area => ({ ...area,
            target: firstAction(this.menu.getMenu(area.id), this.menu),
        }));
    }
    iconUrl(name) { return `/arg_pyme_ui/static/icons/lucide/${name}.svg`; }
    areaIcon(name) {
        return {Ventas:"shopping-cart", Compras:"truck", Stock:"warehouse",
            Administración:"wallet-cards", Informes:"chart-no-axes-combined"}[name] || "factory";
    }
    openArea(area) { if (area.target) return this.menu.selectMenu(area.target); }
    get otherApps() { return this.menu.getApps().filter(app => app.id !== session.arg_pyme?.root_menu_id); }
    openApp(app) { const target = firstAction(app, this.menu); if (target) return this.menu.selectMenu(target); }
}
export class ArgHome extends ArgAreas {
    static template = "arg_pyme_ui.Home";
    props = useProps({ ...standardActionServiceProps });
}
export class ArgWorkspaceRibbon extends ArgAreas {
    static template = "arg_pyme_ui.WorkspaceRibbon";
    setup() {
        super.setup();
        this.action = useService("action");
        this.state = proxy({areaId: null, collapsed: false});
    }
    get visible() { return this.menu.getCurrentApp()?.id === session.arg_pyme?.root_menu_id; }
    get availableAreas() {
        const areas = this.areas.filter(area => area.target);
        const config = this.menu.getMenu(session.arg_pyme?.config_menu_id);
        const target = firstAction(config, this.menu);
        if (target) areas.push({id:config.id, name:config.name, target});
        return areas;
    }
    commands(menu) {
        if (!menu) return [];
        const result = menu.actionID ? [menu] : [];
        for (const id of menu.children || []) result.push(...this.commands(this.menu.getMenu(id)));
        return result;
    }
    get activeArea() {
        const areas = this.availableAreas;
        if (this.state.areaId) return areas.find(a => a.id === this.state.areaId) || areas[0];
        const actionId = this.action.currentController?.action.id;
        return areas.find(a => this.commands(this.menu.getMenu(a.id)).some(m => m.actionID === actionId)) || areas[0];
    }
    get groups() {
        const area = this.activeArea;
        const commands = area ? this.commands(this.menu.getMenu(area.id)) : [];
        const master = /Clientes|Proveedores|Productos|Precios|Categorías|Atributos/;
        return [
            {name:"Documentos y operaciones", items:commands.filter(m => !master.test(m.name))},
            {name:"Datos y catálogos", items:commands.filter(m => master.test(m.name))},
        ].filter(group => group.items.length);
    }
    commandIcon(name) {
        if (/Clientes|Proveedores/.test(name)) return "users";
        if (/Productos|Categorías|Atributos/.test(name)) return "package";
        if (/Precios/.test(name)) return "receipt";
        if (/Existencias|Inventarios/.test(name)) return "boxes";
        if (/Movimientos/.test(name)) return "arrow-left-right";
        if (/Caja|cobro|pago|Cuentas|Recibos/.test(name)) return "wallet-cards";
        if (/Consultas/.test(name)) return "chart-no-axes-combined";
        return "file-text";
    }
    selectArea(area) { this.state.areaId = area.id; this.state.collapsed = false; }
    openCommand(menu) { return this.menu.selectMenu(menu); }
    openHome() { return this.menu.selectMenu(session.arg_pyme.root_menu_id); }
}
patch(WebClient, {components: {...WebClient.components, ArgWorkspaceRibbon}});
registry.category("actions").add("arg_pyme.home", ArgHome);
registry.category("user_menuitems").add("support", () => ({type:"item", id:"support",
    description:"Soporte ARG", href:"/arg/soporte", callback: () => window.open("/arg/soporte", "_blank", "noopener"), sequence:20}), {force:true});
registry.category("user_menuitems").add("arg_about", () => ({type:"item", id:"arg_about",
    description:"Acerca de ARG", href:"/arg/acerca", callback: () => window.open("/arg/acerca", "_blank", "noopener"), sequence:21}));
registry.category("services").add("arg_pyme_preferences", {
    start() {
        const settings = session.arg_pyme;
        if (!settings) return;
        const media = window.matchMedia("(prefers-color-scheme: dark)");
        const apply = () => {
            document.documentElement.dataset.argTheme = settings.theme === "system" ? (media.matches ? "dark" : "light") : (settings.theme || "light");
            document.documentElement.dataset.argDensity = settings.density || "comfortable";
        };
        apply(); media.addEventListener("change", apply);
    },
});
