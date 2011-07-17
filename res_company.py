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

from osv import osv
from osv import fields


class ResCompany(osv.osv):
    """
    Add the possibility to block the confirmation of the sale order 
    when the price unit is lower than the minimum price
    """
    _inherit = 'res.company'

    _columns = {
        'minimum_pricelist_id': fields.many2one('product.pricelist', 'Minimum pricelist', help='This pricelist can compute the minimum price of the product, ' \
                                                'to block if the unit price on sale order is lower\nIf empty there is no blocking'),
        'unblock_group_id': fields.many2one('res.groups', 'Unblock group', help='Group to unblock the sale order, if unit price is lower than the minimal price'),
    }

    _defaults = {
        'minimum_pricelist_id': lambda *a: False,
        'unblock_group_id': lambda *a: False,
    }

ResCompany()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
