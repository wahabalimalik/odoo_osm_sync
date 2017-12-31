# -*- coding: utf-8 -*-

from odoo import models, fields, api
from ..controllers import main

class BuildingOwner(models.Model):
	_inherit = 'res.partner'

	#####################################################
	# Below varibles are owner information
	# which we want to upload to OSM database.
	#####################################################

	bus_ids = fields.Many2one('building.read',string="Business ID")

	citizen = fields.Boolean()
	vrn = fields.Integer('VRN')
	assess = fields.Boolean()
	branch = fields.Boolean('Branch')
	tax = fields.Float(compute='_compute_tax',string='Total Tenant Tax')
	tin = fields.Char('TIN')
	efd = fields.Char('EFD')
	valued = fields.Char('Valued')
	
	tenants_id = fields.One2many('building.tenant','tnt_id')

	#####################################################
	# Fields defining 
	#   i)area own by owner.
	#   ii)Type of building e.g(residential or commercial).
	# 	iii) Replacement cost of building.
	#   iv) Tax on the base of replacement cost.
	#  These fields are storing in res.partner and not 
	#  pushing to OSM.
	#####################################################

	area_own = fields.Float()
	building = fields.Char(compute='_compute_building')
	property_valuation = fields.Float(compute='_compute_valuation',string='Property Valuation')
	property_tax = fields.Float(compute='_compute_tax',string='Property Tax')
	
	#####################################################
	# This is unique killbill ID of Owner for charging 
	# tax money from Owner.
	#####################################################

	killbill_id = fields.Char('KillBill ID')

	#####################################################
	# Below function is for computing building type
	#  e.g(residential or commercial). form reading buil-
	#  -ding information
	####################################################

	@api.one
	@api.depends('bus_ids.building')
	def _compute_building(self):
		if self.bus_ids.building:
			self.building = self.bus_ids.building

	#####################################################
	# Below function is for calculating property tax
	# with respect to building type 
	# e.g(residential or commercial) and property 
	# replacement value.
	####################################################

	@api.one
	@api.depends('property_valuation','building')
	def _compute_tax(self):
		if self.property_valuation and self.building:
			if 'commercial' in self.building:
				self.property_tax = self.property_valuation * 0.20 / 100
			else:
				self.property_tax = self.property_valuation * 0.15 / 100
	#####################################################
	# Below function is for auto caculation of property
	# value it depend on area own by owner
	####################################################

	@api.one
	@api.depends('area_own')
	def _compute_valuation(self):
		if self.area_own:
			self.property_valuation = float(self.area_own) * 50000

	#####################################################
	# Below function is a dispatch data to dispatch_rpc() 
	# function where it will redirect to appropriate 
	# controller 
	#####################################################

	@api.multi
	def create_owner(self):
		tenant_name = []
		for x in self.tenants_id:
			tenant_name.append(x.tenant_name.tenant)

		data = {
			"params": {
				"bus_ids" : self.bus_ids.bus_ids,
				"name" : self.name,
				"citizen" : self.citizen,
				"vrn" : self.vrn,
				"assess" : self.assess,
				"branch" : self.branch,
				"tax" : self.tax,
				"tin" : self.tin,
				"efd" : self.efd,
				"valued" : self.valued,
				'tenants_id' : tenant_name
			}
		}
		main.dispatch_rpc(category = 'owner' ,data = data)
