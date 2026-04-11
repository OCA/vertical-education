###############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<https://www.openeducat.org>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

{
    "name": "OpenEduCat Classroom",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "category": "Education",
    "sequence": 3,
    "summary": "Manage Classroom",
    "complexity": "easy",
    "author": "OpenEduCat Inc, Odoo Community Association (OCA), Sufyaldy IAIN Parepare",
    "website": "https://github.com/OCA/vertical-education",
    "depends": ["openeducat_core", "openeducat_facility", "product"],
    "data": [
        "security/op_classroom_security.xml",
        "security/ir.model.access.csv",
        "views/classroom_view.xml",
        "menus/op_menu.xml",
    ],
    "demo": ["demo/classroom_demo.xml", "demo/facility_line_demo.xml"],
    "images": [
        "static/description/openeducat-classroom_banner.jpg",
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
}
