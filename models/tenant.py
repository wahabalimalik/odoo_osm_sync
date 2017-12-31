# -*- coding: utf-8 -*-

from odoo import models, fields, api
from ..controllers import main

class BuildingTenant(models.Model):
	_name = 'building.tenant'
	_rec_name = 'tenant'

	#####################################################
	# Below varibles are tenant information
	# which we want to upload to OSM database.
	#####################################################

	bus_ids = fields.Char(string='Business ID' ,readonly=True)
	
	tenant = fields.Char('Tenant Name')
	citizen = fields.Boolean()
	rent = fields.Integer()
	vrn = fields.Integer('VRN')
	assess = fields.Boolean()
	branch = fields.Boolean()
	tax = fields.Float(compute='_compute_tax')
	tin = fields.Integer('TIN')
	efd = fields.Integer('EFD')
	valued = fields.Integer()

	#####################################################
	# Connection of tenant's class to owner's class.
	#####################################################

	tnt_id = fields.Many2one('res.partner',ondelete='cascade')

	#####################################################
	# Connection of tenant's class to Info class.
	#####################################################

	tenant_name = fields.Many2one('building.read.line','Tenant Name',domain=[('tenant', '!=', 'Nr')])

	@api.onchange('tenant_name')
	def onchange_tenant_name(self):
		if self.tenant_name:
			if self.tenant_name.citizen == 'True':
				self.citizen = True
			self.rent = int(self.tenant_name.rent)
			self.tax = float(self.tenant_name.tax)

	#####################################################
	# Below function is for auto caculation of tax
	# for citizen and non-citizen tenants.
	# citizens should have to pay 10% while non-citizen 
	# will pay 15% of total rent they are going to pay to 
	# the owner of building.
	######################################################
	
	@api.one
	@api.depends('citizen','rent')
	def _compute_tax(self):
		if self.citizen:
			if self.rent:
				self.tax = (self.rent/100) * 10
		else:
			self.tax = (self.rent/100) * 15

	#####################################################
	# Below function is a dispatch data to dispatch_rpc() 
	# function where it will redirect to appropriate 
	# controller 
	#####################################################

	@api.multi
	def create_tenant(self):
		data = {
			"params": {
				"bus_ids" : self.bus_ids,
				"tenant" : self.tenant,
				"citizen" : self.citizen,
				"rent" : self.rent,
				"vrn" : self.vrn,
				"assess" : self.assess,
				"branch" : self.branch,
				"tax" : self.tax,
				"tin" : self.tin,
				"efd" : self.efd,
				"valued" : self.valued,
			}
		}
		main.dispatch_rpc(category = 'tenant' ,data = data)