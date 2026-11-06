/** @odoo-module **/
import { Component, onWillStart, proxy, t, useProps } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { standardActionServiceProps } from "@web/webclient/actions/action_plugin";
import { useSetupAction } from "@web/search/action_hook";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { deserializeDateTime, formatDateTime } from "@web/core/l10n/dates";

const MODEL = "arg.pyme.replenishment";
const TITLES = { product: "Elegir producto", warehouse: "Elegir depósito", location: "Elegir ubicación",
    route: "Elegir ruta", multiple: "Elegir presentación o múltiplo" };

export class Replenishment extends Component {
    static template = "arg_pyme_stock.Replenishment";
    props = useProps({ ...standardActionServiceProps });
    state = proxy({ company: "", canCreate: false, loading: false, saving: false, error: "",
        query: "", warehouse: null, product: null, result: null, applied: null, editor: null, picker: null,
        extensions: [], horizon: null, horizonEditing: false, horizonDraft: "" });

    setup() {
        this.orm = useService("orm"); this.dialog = useService("dialog");
        this.action = useService("action"); this.notification = useService("notification");
        useSetupAction({ beforeLeave: () => this.beforeLeave(),
            beforeUnload: event => { if (this.dirty || this.state.saving) { event.preventDefault(); event.returnValue = ""; } },
            getLocalState: () => ({ argReplenishment: { query: this.state.query,
                productId: this.state.product?.id, warehouseId: this.state.warehouse?.id,
                applied: this.state.applied, offset: this.state.result?.offset || 0 } }) });
        onWillStart(async () => {
            this.state.loading = true;
            try {
                const options = await this.orm.call(MODEL, "options", []);
                this.state.company = options.company; this.state.canCreate = options.can_create;
                this.state.extensions = options.extensions; this.state.horizon = options.horizon;
                const saved = this.props.state?.argReplenishment;
                if (saved) {
                    this.state.query = saved.query || "";
                    for (const kind of ["product", "warehouse"]) {
                        if (saved[`${kind}Id`]) this.state[kind] = await this.orm.call(MODEL, "reference", [kind, saved[`${kind}Id`]]);
                    }
                }
                await this.fetchPage(saved?.offset || 0, saved?.applied || this.filters);
            } catch (error) { this.fail(error); }
            finally { this.state.loading = false; }
        });
    }

    fail(error) { this.state.error = error.data?.message || error.message; }
    get busy() { return this.state.loading || this.state.saving; }
    get filters() { return { query: this.state.query, product_id: this.state.product?.id || false,
        warehouse_id: this.state.warehouse?.id || false }; }
    get filtersDirty() { return !!this.state.applied && JSON.stringify(this.filters) !== JSON.stringify(this.state.applied); }
    get dirty() { return (!!this.state.editor && JSON.stringify(this.state.editor.values) !== this.state.editor.original)
        || (this.state.horizonEditing && this.state.horizonDraft !== String(this.state.horizon.days)); }
    number(value) { return value === null || value === undefined ? "—" : new Intl.NumberFormat("es-AR", { maximumSignificantDigits: 15 }).format(value); }
    when(value) { return value ? formatDateTime(deserializeDateTime(value)) : "—"; }
    mode(value) { return ({ manual: "Manual", auto: "Automática" })[value] || value; }

    async fetchPage(offset, filters) {
        const result = await this.orm.call(MODEL, "page", [], { ...filters, offset });
        this.state.result = result; this.state.applied = { ...filters }; this.state.company = result.company;
    }
    async load(offset = 0, applied = false) {
        if (this.busy || this.state.editor || this.state.picker || this.state.horizonEditing) return;
        this.state.loading = true; this.state.error = "";
        try { await this.fetchPage(offset, applied ? this.state.applied : this.filters); }
        catch (error) { this.fail(error); this.state.result = null; }
        finally { this.state.loading = false; }
    }

    async edit(row = null) {
        if (this.busy || this.state.editor || this.state.picker || this.state.horizonEditing) return;
        this.state.loading = true; this.state.error = "";
        try {
            const data = await this.orm.call(MODEL, "defaults", [row?.id || false, this.state.product?.id || false]);
            const values = { ...data.values, product_min_qty: String(data.values.product_min_qty),
                product_max_qty: String(data.values.product_max_qty) };
            const refs = {};
            for (const [key, kind] of [["product_id", "product"], ["warehouse_id", "warehouse"],
                ["location_id", "location"], ["route_id", "route"], ["replenishment_uom_id", "multiple"],
                ...this.state.extensions.map(spec => [spec.field, spec.kind])]) {
                if (data.configuration) refs[kind] = data.configuration[kind] || data.configuration.extensions[kind];
                else if (values[key]) refs[kind] = await this.orm.call(MODEL, "reference", [kind, values[key]]);
            }
            const product = refs.product;
            this.state.editor = { id: row?.id || false, token: data.configuration?.token || false,
                trigger: data.configuration?.trigger || "manual", values, refs,
                unit: data.configuration?.unit || product?.unit || null, original: JSON.stringify(values) };
        } catch (error) { this.fail(error); }
        finally { this.state.loading = false; }
    }
    refName(kind) { return this.state.editor.refs[kind]?.name || "Sin especificar"; }
    setBound(name, value) { this.state.editor.values[name] = value; this.state.error = ""; }
    clear(kind) {
        if (this.busy) return;
        if (this.state.editor) {
            const key = kind === "multiple" ? "replenishment_uom_id" : `${kind}_id`;
            this.state.editor.values[key] = false;
            this.state.editor.refs[kind] = { id: false, name: "Sin especificar", status: "unset" };
        } else this.state[kind] = null;
    }
    parseBound(value) {
        const text = String(value).trim();
        if (!/^[+]?(?:\d+(?:[.,]\d*)?|[.,]\d+)(?:[eE][+-]?\d+)?$/.test(text)) throw new Error("Ingresá mínimos y máximos numéricos, sin separador de miles.");
        const number = Number(text.replace(",", "."));
        if (!Number.isFinite(number) || number < 0) throw new Error("Los límites deben ser finitos y mayores o iguales a cero.");
        return number;
    }
    saveValues() {
        const values = { ...this.state.editor.values };
        values.product_min_qty = this.parseBound(values.product_min_qty);
        values.product_max_qty = this.parseBound(values.product_max_qty);
        if (values.product_min_qty > values.product_max_qty) throw new Error("El mínimo no puede superar al máximo.");
        if (!values.product_id || !values.warehouse_id || !values.location_id) throw new Error("Elegí producto, depósito y ubicación.");
        return values;
    }
    async save() {
        if (this.busy || this.state.picker) return;
        let values;
        try { values = this.saveValues(); } catch (error) { this.fail(error); return; }
        this.state.saving = true; this.state.error = "";
        try {
            const editor = this.state.editor;
            const result = await this.orm.call(MODEL, "save_rule", [values, editor.id, editor.token]);
            this.state.editor = null;
            this.notification.add(result.message, { type: "success" });
            try { await this.fetchPage(this.state.result?.offset || 0, this.state.applied || this.filters); }
            catch (error) { this.state.result = null; this.fail(error); }
        } catch (error) { this.fail(error); }
        finally { this.state.saving = false; }
    }
    async beforeLeave() {
        if (this.busy) return false;
        if (!this.dirty) return true;
        return new Promise(resolve => this.dialog.add(ConfirmationDialog, {
            title: "Configuración sin guardar", body: "Hay cambios de configuración pendientes.",
            confirmLabel: "Descartar y salir", confirmClass: "btn-danger", cancelLabel: "Seguir editando",
            confirm: () => { this.state.editor = null; this.state.picker = null; this.state.horizonEditing = false; resolve(true); },
            cancel: () => resolve(false), dismiss: () => resolve(false) }));
    }
    async discard() {
        if (await this.beforeLeave()) { this.state.editor = null; this.state.picker = null; this.state.horizonEditing = false; this.state.error = ""; }
    }
    async advanced(row) {
        if (this.busy || this.state.editor || this.state.picker || this.state.horizonEditing) return;
        this.state.loading = true; this.state.error = "";
        let action;
        try { action = await this.orm.call(MODEL, "open_rule", [row.id]); }
        catch (error) { this.fail(error); }
        finally { this.state.loading = false; }
        if (action) {
            try { await this.action.doAction(action); }
            catch (error) { this.fail(error); }
        }
    }

    async pick(kind) {
        if (this.busy || this.state.picker) return;
        let values = null;
        if (kind === "multiple") {
            try { values = this.saveValues(); } catch (error) { this.fail(error); return; }
        }
        const spec = this.state.extensions.find(spec => spec.kind === kind);
        if (spec && !this.state.editor?.values.product_id) { this.state.error = "Elegí un producto antes de buscar opciones de abastecimiento."; return; }
        this.state.error = "";
        this.state.picker = { kind, title: spec ? `Elegir ${spec.label}` : TITLES[kind], extension: !!spec,
            values, query: "", applied: "", rows: [], count: 0, offset: 0 };
        await this.choices(0);
    }
    async choices(offset = 0, applied = false) {
        if (this.busy || !this.state.picker) return;
        const picker = this.state.picker;
        const query = applied ? picker.applied : picker.query;
        this.state.loading = true; this.state.error = "";
        try {
            const result = picker.extension
                ? await this.orm.call(MODEL, "extension_choices", [picker.kind, this.state.editor.values.product_id, query, offset])
                : picker.kind === "multiple"
                ? await this.orm.call(MODEL, "multiple_choices", [picker.values, this.state.editor.id, query, offset])
                : await this.orm.call(MODEL, "choices", [picker.kind, query, offset,
                    this.state.editor?.values.warehouse_id || false]);
            Object.assign(picker, result, { applied: query });
        } catch (error) { this.fail(error); picker.rows = []; picker.count = 0; }
        finally { this.state.loading = false; }
    }
    closePicker() { if (!this.busy) { this.state.picker = null; this.state.error = ""; } }
    async choose(row) {
        if (this.busy) return;
        const kind = this.state.picker.kind;
        if (!this.state.editor) { this.state[kind] = row; this.closePicker(); return; }
        this.state.loading = true; this.state.error = "";
        try {
            const ref = this.state.picker.extension
                ? await this.orm.call(MODEL, "extension_reference", [kind, row.id, this.state.editor.values.product_id])
                : await this.orm.call(MODEL, "reference", [kind === "multiple" ? "unit" : kind, row.id]);
            const editor = this.state.editor;
            const key = kind === "multiple" ? "replenishment_uom_id" : `${kind}_id`;
            const previousId = editor.values[key];
            editor.values[key] = ref.id; editor.refs[kind] = { ...ref, status: "known" };
            if (kind === "product") editor.unit = ref.unit;
            if (kind === "warehouse" && previousId !== ref.id) {
                editor.values.location_id = ref.default_location.status === "known" ? ref.default_location.id : false;
                editor.refs.location = ref.default_location;
            }
            this.state.picker = null;
        } catch (error) { this.fail(error); }
        finally { this.state.loading = false; }
    }
    async editHorizon() {
        if (this.busy || this.state.editor || this.state.picker || !this.state.horizon?.can_edit) return;
        this.state.loading = true; this.state.error = "";
        try {
            const result = await this.orm.call(MODEL, "options", []);
            this.state.horizon = result.horizon;
            if (!result.horizon.can_edit) throw new Error("Modificar el horizonte requiere permiso de edición de la compañía.");
            this.state.horizonDraft = String(result.horizon.days); this.state.horizonEditing = true;
        } catch (error) { this.fail(error); }
        finally { this.state.loading = false; }
    }
    async refreshHorizon() {
        if (this.busy || !this.state.horizonEditing) return;
        this.state.loading = true; this.state.error = "";
        try {
            const result = await this.orm.call(MODEL, "options", []);
            this.state.horizon = result.horizon;
        } catch (error) { this.fail(error); }
        finally { this.state.loading = false; }
    }
    async saveHorizon() {
        if (this.busy || !this.state.horizonEditing) return;
        const text = this.state.horizonDraft.trim(); const days = Number(text);
        if (!/^\d+$/.test(text) || !Number.isSafeInteger(days) || days > 2147483647) {
            this.state.error = "Ingresá una cantidad entera de días mayor o igual a cero."; return;
        }
        this.state.saving = true; this.state.error = "";
        try {
            const result = await this.orm.call(MODEL, "save_horizon", [days, this.state.horizon.token]);
            this.state.horizon = result.horizon; this.state.horizonEditing = false;
            this.notification.add(result.message, { type: "success" });
        } catch (error) { this.fail(error); }
        finally { this.state.saving = false; }
    }
}
registry.category("actions").add("arg_pyme.replenishment", Replenishment);
