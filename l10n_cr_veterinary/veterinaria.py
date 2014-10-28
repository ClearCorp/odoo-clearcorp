# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Addons modules by CLEARCORP S.A.
#    Copyright (C) 2009-TODAY CLEARCORP S.A. (<http://clearcorp.co.cr>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields,api
from datetime import datetime
from openerp.exceptions import Warning
import openerp.addons.decimal_precision as dp

class specie (models.Model):
    
    _name='veterinaria.specie'
    
    name = fields.Char('Name', size=128, required=True)
    scientific_name= fields.Char('Scientific Name', size=128, required=True,
                                 help='This is the scientific name of...')
    breed_ids=fields.One2many('veterinaria.breed','specie_id', string='Breed')
    
            
class breed(models.Model):
    
    _name='veterinaria.breed'
    _order='size asc'
    _rec_name='breed_name'
    
    breed_name = fields.Char('Name', size=128, required=True)
    scientific_name= fields.Char('Scientific Name', size=128)
    size = fields.Float('Size', digits=(16,3))
    specie_id = fields.Many2one('veterinaria.specie', string='Specie',required=True)

class patient(models.Model):
    
    _name='veterinaria.patient'
    _order='patient_name asc'
    
    @api.one
    @api.depends('brith_date')
    def _compute_age (self):
        ageaux = 0.0
        if self.brith_date:
            date = datetime.strptime(self.brith_date,'%Y-%m-%d')
            delta = datetime.now() - date
            ageaux = delta.days / 365.00
        self.age = ageaux
            
    @api.multi
    def patient_healthy (self):
        self.write({'state':'healthy'})
        
    @api.multi
    def patient_sick (self):
        self.write({'state':'sick'})
        
    @api.onchange('pure_breed')
    def onchange_pure_breed(self):
        self.pedrigree=''
        
    @api.constrains('specie_id','breed_id')
    def check_breed_id(self):
        if self.breed_id not in self.specie_id.breed_ids:
            raise Warning('Breed does not belong to Specie')
        return True
    
    patient_name = fields.Char('Patient', size=128, required=True)
    brith_date= fields.Date ('Birth Date')    
    age = fields.Float('Age', compute='_compute_age', digits=(16,1))
    pure_breed= fields.Boolean('Pure Breed')
    gender = fields.Selection([('male','Male'),('female','Female')], 
                              string='Gender', default='male')
    state = fields.Selection([('healthy','Healthy'),('sick','Sick')], 
                             string='State', default='healthy')
    pedrigree = fields.Char('Pedigree',size=64)
    food = fields.Text('Food')
    castreded = fields.Boolean('Castreded')
    weight = fields.Float('Weight')
    specie_id = fields.Many2one('veterinaria.specie', string='Specie', required=True)
    breed_id = fields.Many2one('veterinaria.breed', string='Breed')    
    product_uom_id = fields.Many2one('product.uom', string=' ')    
    partner_id = fields.Many2one ('res.partner', string='Family', required=True)
    