/** @odoo-module **/

import {PageDependencies} from '@website/components/dialog/page_properties';
import {standardFieldProps} from '@web/views/fields/standard_field_props';
import { UrlField, urlField } from "@web/views/fields/url/url_field";
import {registry} from '@web/core/registry';
import { _t } from '@web/core/l10n/translation';
import { Component, useEffect, useRef } from "@odoo/owl";

/**
 * Displays website page dependencies and URL redirect options when the page URL
 * is updated.
 */
class PageUrlField extends UrlField {
    static components = { PageDependencies };
    static template = "website.PageUrlField";
    static defaultProps = {
        ...UrlField.defaultProps,
        websitePath: true,
    };

    setup() {
        super.setup();
        this.serverUrl = `${window.location.origin}/`;
        this.inputRef = useRef("input");

        // Trigger onchange api on input event to display redirection
        // parameters as soon as the user types.
        // TODO should find a way to do this more automatically (and option in
        // the framework? or at least a t-on-input?)
        useEffect(
            (inputEl) => {
                if (inputEl) {
                    const fireChangeEvent = () => {
                        inputEl.dispatchEvent(new Event("change"));
                    };

                    inputEl.addEventListener("input", fireChangeEvent);
                    return () => {
                        inputEl.removeEventListener("input", fireChangeEvent);
                    };
                }
            },
            () => [this.inputRef.el],
        );
    }

    get value() {
        let value = super.value;
        if (value[0] === "/") {
            value = value.substring(1);
        }
        this.props.record.data[this.props.name] = `/${value.trim()}`;
        return value;
    }
}


export class FeesTermsDisplay extends Component {
    static template = "website.FieldFeesTermsDisplay";
    static props = {
        ...standardFieldProps,
    };

    setup() {
        const selection = this.props.record.fields[this.props.name].selection;
        this.terms = selection.filter(item => item[0] || item[1]).map(item => ({
            value: item[0],
            label: item[1],
            description: this.props.record.data.fees_terms_description || ''
//            image: this.getImagePath(item[0]),
        }));

    }
    _onClickLabel(value) {
        this.props.record.update({ [this.props.name]: value });
    }

     get description() {
         return {
            'fixed_days': 'Fixed fee per attendance day.',
            'fixed_date': 'Fixed fee for a specific period or dates.',
            'duration_based': 'Fees based on session or program length.',
            'session_based': 'Fee per session; pay-as-you-go.',
            'faculty_based': 'Fees depends on faculty expertise and specialization.'
        }
     }
    get ImagePath() {
        return {
            'fixed_days': '/openeducat_fees/static/description/term_type_1.svg',
            'fixed_date': '/openeducat_fees/static/description/term_type_2.svg',
            'duration_based': '/openeducat_fees/static/description/term_type_3.svg',
            'session_based': '/openeducat_fees/static/description/term_type_4.svg',
            'faculty_based': '/openeducat_fees/static/description/term_type_5.svg'
        }
    }
    onSelectValue(value) {
        this.props.record.update({ [this.props.name]: value });
    }
}

export const feesTermsDisplay = {
    component: FeesTermsDisplay,
    supportedTypes: ['selection'],
};

registry.category("fields").add("fees_terms_display", feesTermsDisplay);
