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
from tools.translate import _
import logging

_logger = logging.getLogger('sale_minimal_price')


class sale_order(osv.osv):
    _inherit = 'sale.order'

    def action_wait(self, cr, uid, ids, context=None):
        """
        Check if price unit for each lines is lower than block price
        if True and user not in the group on company, raise an error
        """
        if context is None:
            context = self.pool.get('res.users').context_get(cr, uid)

        user = self.pool.get('res.users').browse(cr, uid, uid)
        have_group = user.company_id.unblock_group_id.id in [z.id for z in user.groups_id]
        for so in self.browse(cr, uid, ids):
            if not have_group and [x.id for x in so.order_line if x.price_unit < x.block_price]:
                raise osv.except_osv(_('Validation Error'),
                    _('You cannot validate the sale order, some lines have a unit price lower than minimal price'))

        return super(sale_order, self).action_wait(cr, uid, ids, context)

sale_order()


class sale_order_line(osv.osv):
    _inherit = 'sale.order.line'

    _columns = {
        'block_price': fields.float('Block price', help='The product cannot be sale below this price'),
    }

    _defaults = {
         'block_price': lambda *a: 0.0,
    }

    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False):
        """
        This function compute the minimal price, with the pricelist define on the company
        """
        res = super(sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty,
            uom, qty_uos, uos, name, partner_id, lang, update_tax, date_order, packaging, fiscal_position, flag)

        if product:
            context = self.pool.get('res.users').context_get(cr, uid)
            cny = self.pool.get('res.users').browse(cr, uid, uid).company_id
            if cny.minimum_pricelist_id:
                extra = {
                    'uom': uom,
                    'date': date_order,
                }
                price = self.pool.get('product.pricelist').price_get(cr, uid, [cny.minimum_pricelist_id.id],
                            product, qty or 1.0, partner_id, extra)[cny.minimum_pricelist_id.id]

                warning = res['warning']
                if price is False:
                    warning = {
                        'title': _('No valid minimal pricelist line found !'),
                        'message':
                            _("Couldn't find a pricelist line matching this product and quantity.\nYou have to change either the product, the quantity or the pricelist.")
                    }

                res['value']['block_price'] = price or 0.0
                _logger.debug('Price unit: %f, Block price: %f' % (res['value']['price_unit'], res['value']['block_price']))
                if price > res['value']['price_unit']:
                    warning = {
                        'title': _('The unit price is lower than the price unit'),
                        'message':
                            _("You have a price unit lower than the minimal\nYou cannot confirm your sale order, please ask to your manager to do it.")
                    }

                res['warning'] = warning

        return res

    def onchange_price_unit(self, cr, uid, ids, price_unit, block_price):
        """
        If price unit is lower than block price, send a warning
        """
        if price_unit and block_price and (price_unit < block_price):
            _logger.debug('Price unit: %f, Block price: %f' % (price_unit, block_price))
            context = self.pool.get('res.users').context_get(cr, uid)
            return {'warning': {
                'title': _('The unit price is lower than the price unit'),
                'message':
                    _('You have a price unit lower than the minimal\nYou cannot confirm your sale order, please ask to your manager to do it.')
            }}
        return {}

sale_order_line()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
