/** @odoo-module **/
import { Component, useProps } from "@odoo/owl";
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
    areaIcon(name) {
        return {
            Ventas: "M3 4h2l2 11h11l3-8H6 M9 20h.01 M17 20h.01",
            Compras: "M5 7h14v14H5z M9 7V5a3 3 0 0 1 6 0v2 M9 12h6",
            Stock: "M3 7l9-4 9 4v10l-9 4-9-4z M3 7l9 4 9-4 M12 11v10",
            Administración: "M3 6h18v14H3z M3 10h18 M14 14h4 M6 3v3 M18 3v3",
            Informes: "M4 3v18h17 M8 17v-5 M13 17V8 M18 17V5",
        }[name] || "M4 4h6v6H4z M14 4h6v6h-6z M4 14h6v6H4z M14 14h6v6h-6z";
    }
    openArea(area) { if (area.target) return this.menu.selectMenu(area.target); }
    get otherApps() { return this.menu.getApps().filter(app => app.id !== session.arg_pyme?.root_menu_id); }
    openApp(app) { const target = firstAction(app, this.menu); if (target) return this.menu.selectMenu(target); }
}
export class ArgHome extends ArgAreas {
    static template = "arg_pyme_ui.Home";
    props = useProps({ ...standardActionServiceProps });
}
export class ArgCircuitNav extends ArgAreas { static template = "arg_pyme_ui.CircuitNav"; }
registry.category("actions").add("arg_pyme.home", ArgHome);
registry.category("systray").add("arg_pyme.nav", { Component: ArgCircuitNav }, { sequence: 40 });
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
