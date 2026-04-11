/** @odoo-module **/

import { Many2OneField, many2OneField } from "@web/views/fields/many2one/many2one_field";
import { registry } from "@web/core/registry";
import { Many2XAutocomplete } from "@web/views/fields/relational_utils";
import { onMounted, useRef } from "@odoo/owl";

export class AutoMany2XAutocomplete extends Many2XAutocomplete{
    static template = 'openeducat_core.Many2XAutocomplete';
    setup() {
        this.input = useRef('input');
        super.setup();
        onMounted(() => {
            this._createSizer();
            this._resizeInput();
        });
    }

    onChange({ inputValue }) {
        super.onChange(...arguments);
        this._resizeInput();
    }

    onSelect(option, params = {}) {
        super.onSelect(...arguments);
        this._resizeInput(option.displayName);
    }

    _createSizer() {
        if (!this._sizer) {
            this._sizer = document.createElement("span");
            Object.assign(this._sizer.style, {
                position: "absolute",
                visibility: "hidden",
                whiteSpace: "pre",
                font: getComputedStyle(document.body).font,
            });
            document.body.appendChild(this._sizer);
        }
    }

    _resizeInput(defaultValue = null) {
        const input = this.autoCompleteContainer.el.querySelector('input');
        if (!input) return;

        const value = defaultValue || input.value || input.placeholder || "";
        this._sizer.textContent = value;
        this._sizer.style.font = getComputedStyle(input).font;

        const targetWidth = this._sizer.offsetWidth + 20;
        input.style.width = `${targetWidth}px`;
    }
}

export class InlineMany2OneField extends Many2OneField {
    static components = {
        ...Many2OneField.components,
        Many2XAutocomplete: AutoMany2XAutocomplete
    }
    setup() {
        super.setup();
        onMounted(() => {
            //this._createSizer();
            //this._resizeInput();
        });
    }

    onInputTypeMany2One() {
        this._resizeInput();
    }

    _createSizer() {
        if (!this._sizer) {
            this._sizer = document.createElement("span");
            Object.assign(this._sizer.style, {
                position: "absolute",
                visibility: "hidden",
                whiteSpace: "pre",
                font: getComputedStyle(document.body).font,
            });
            document.body.appendChild(this._sizer);
        }
    }

    _resizeInput() {
        const input = this.input.el;
        if (!input) return;

        const value = input.value;
        if (value) {
            input.style.width = "1px";
            input.style.width = `${input.scrollWidth + 2}px`;
        } else {
            this._sizer.textContent = input.placeholder || "";
            this._sizer.style.font = getComputedStyle(input).font;
            input.style.width = `${this._sizer.offsetWidth + 10}px`;
        }
    }

    willUnmount() {
        super.willUnmount?.();
        if (this._sizer) {
            this._sizer.remove();
            this._sizer = null;
        }
    }
}

registry.category("fields").add("inline_many2one", {
    ...many2OneField,
    component: InlineMany2OneField,
});
