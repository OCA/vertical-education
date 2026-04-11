/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import {registry} from '@web/core/registry';
import {listView} from '@web/views/list/list_view';


export class PageListController extends listView.Controller {
    onClickCreate() {
        return this.actionService.doAction('openeducat_fees.action_select_fees_term_type');
    }
}

export const PageListView = {
    ...listView,
    Controller: PageListController,
};

registry.category("views").add("fees_wizard_list", PageListView);
