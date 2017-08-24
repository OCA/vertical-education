.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

========================================
Education Management System - Attendance
========================================

This module provide attendance for Education Management System over Odoo.

Features includes managing Attendance Sheets and Attendance Registers.

Attendance Sheet can register Attendance Lines for each student on a session.

Attendance Register can group several Attendance Sheets for same batch.

Usage
=====

First of all you need to create timetable and generate session, see education_timetable module.

Then, on Attendances menu, you can:
* create an Attendance Register, for a batch, it can be done for a week or day.
* create several Attendance Sheets for this Attendance Register, one per session.
* On each Attendance Sheet you can create Attencance Line for each student.


.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/217/10.0

Known issues / Roadmap
======================

* Wizard to create Attendance Register for course, subject or faculty, by day or week.
* Create Attendance Lines for Attendance Sheet on Session onchange.
* Report to print Attendance Sheet.
* Report to print Attendance Register.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/vertical-education/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Angel Moya <angel.moya@pesol.es>

Do not contact contributors directly about support or help with technical issues.

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
