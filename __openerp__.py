# -*- coding: utf-8 -*-
##############################################################################
#
#    sale_minimal_price module for OpenERP, Module to block validation of the sale order
#    Copyright (C) 2011 SYLEAM (<http://www.syleam.fr/>)
#              Christophe CHAUVET <christophe.chauvet@syleam.fr>
#
#    This file is a part of sale_minimal_price
#
#    sale_minimal_price is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    sale_minimal_price is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Sale Minimal Price',
    'version': '1.0',
    'category': 'Custom',
    'description': """Module to block validation of the sale order
    when price is lower than minimum price
    """,
    'author': 'SYLEAM',
    'website': 'http://www.syleam.fr/',
    'depends': [
        'product',
        'sale',
    ],
    'init_xml': [],
    'images': [],
    'update_xml': [
        #'security/groups.xml',
        #'security/ir.model.access.csv',
        #'view/menu.xml',
        #'wizard/wizard.xml',
        #'report/report.xml',
    ],
    'demo_xml': [],
    'test': [],
    #'external_dependancies': {'python': ['kombu'], 'bin': ['which']},
    'installable': True,
    'active': False,
    'license': 'AGPL-3',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
