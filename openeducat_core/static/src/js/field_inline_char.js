/** @odoo-module **/

import { CharField, charField } from "@web/views/fields/char/char_field";
import { registry } from "@web/core/registry";
import { onMounted, useEffect } from "@odoo/owl";

export class InlineCharField extends CharField {
    static template = 'openeducat_core.InlineCharField';

    setup() {
        super.setup();
        onMounted(() => {
            this._createSizer();
            this._resizeInput();
        });
    }

    setup() {
        super.setup();
        useEffect(() => {
            this._createSizer();
            this._resizeInput();
        });
    }

    onInputType() {
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

registry.category("fields").add("inline_char", {
    ...charField,
    component: InlineCharField,
});
