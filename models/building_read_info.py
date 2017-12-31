# -*- coding: utf-8 -*-

from odoo import models, fields, api

class BuildingRead(models.Model):
	_name = 'building.read'
	_rec_name = 'bus_ids'

	#####################################################
	# Below varibles are building information
	# which we want to know about Building.
	#####################################################

	bus_ids = fields.Integer("Building ID")
	name = fields.Char()
	street = fields.Char()
	area = fields.Float()
	building = fields.Char()
	levels = fields.Integer()
	material = fields.Char()
	shop = fields.Char()
	types = fields.Char()
	amenity = fields.Char()
	info_data = fields.One2many('building.read.line', 'info_id')

	#####################################################
	# Below varibles and functions are for property tax
	# and valuation calculations
	#####################################################
	
	property_valuation = fields.Float(compute='_compute_valuation',string='Property Valuation')
	property_tax = fields.Float(compute='_compute_tax',string='Property Tax')

	@api.one
	@api.depends('property_valuation','building')
	def _compute_tax(self):
		if self.property_valuation and self.building:
			if 'commercial' in self.building:
				self.property_tax = self.property_valuation * 0.20 / 100
			else:
				self.property_tax = self.property_valuation * 0.15 / 100

	@api.one
	@api.depends('area')
	def _compute_valuation(self):
		if self.area:
			self.property_valuation = float(self.area) * 50000

	#####################################################
	# Below function is to redirect to add tenant page.
	#####################################################

	@api.multi
	def button_open_wizard_tnt(self):
		return {
		'type': 'ir.actions.act_window',
		'name': 'Tenant',
		'res_model': 'building.tenant',
		'view_type': 'form',
		'view_mode': 'form',
		'target' : 'new',
		'context':"{'default_bus_ids': %s}" %(self.bus_ids)
		}

	#####################################################
	# Below function is to redirect to add owner page.
	#####################################################

	@api.multi
	def button_open_wizard_own(self):
		return {
		'type': 'ir.actions.act_window',
		'name': 'Owner',
		'res_model': 'res.partner',
		'view_type': 'form',
		'view_mode': 'form',
		'target' : 'new',
		'context':"{'default_bus_ids': %s,'default_area_own': %s}" %(self.id,self.area)
		}

	#####################################################
	# Below function is to redirect to add building info
	# page.
	#####################################################

	@api.multi
	def button_add_build_info(self):
		return {
		'type': 'ir.actions.act_window',
		'name': 'Building Info',
		'res_model': 'build.info',
		'view_type': 'form',
		'view_mode': 'form',
		'target' : 'new',
		'context':"{'default_bus_ids': %s}" %(self.id)
		}

class BuildingReadLine(models.Model):
	_name = 'building.read.line'
	_rec_name = 'tenant'

	##########################################
	# Constant fields for all nodes
	##########################################

	types = fields.Char()
	bus_ids = fields.Char()
	lat = fields.Char()
	lon = fields.Char()
	name = fields.Char()
	shop = fields.Char()
	amenity = fields.Char()

	##########################################
	# Nodes fields only for Tenants
	##########################################

	tenant = fields.Char()
	rent = fields.Char()

	##########################################
	# Nodes fields only for Owner
	##########################################
	
	tenants_id = fields.Char()

	##########################################
	# Nodes fields common for Owner and Tenant
	##########################################

	citizen = fields.Char()
	vrn = fields.Char()
	assess = fields.Char()
	branch = fields.Char()
	tax = fields.Char()
	tin = fields.Char()
	efd = fields.Char()
	valued = fields.Char()

	##########################################
	# Nodes fields common for Owner and Building 
	# Information
	##########################################

	owner = fields.Char()

	##########################################
	# Nodes fields only for Building Information
	##########################################

	property_name = fields.Char()
	ward = fields.Char()
	sub_ward = fields.Char()
	street = fields.Char()
	plot_no = fields.Char()
	post_code_no = fields.Char()
	user = fields.Char()
	tenure = fields.Char()
	address = fields.Char()
	state = fields.Selection([
        ('complete', 'Complete'),
        ('incomplete', 'Inomplete'),
        ])
	discription = fields.Text()
	roof = fields.Selection([
        ('roof_slab', 'Roof Slab'),
        ('iron_sheet', 'Iron Sheet'),
        ('cemented_tiles', 'Cemented tiles'),
        ('tiles_sheets', 'Tiles Sheets'),
        ('asbestos', 'Asbestos'),
        ('grass', 'Grass'),
        ('other', 'OTHERS'),
        ('none', 'NONE'),
        ])
	ceiling = fields.Selection([
        ('cement', 'Cement'),
        ('gipsum', 'Gipsum'),
        ('treated_timber', 'Treated Timber'),
        ('hardboard', 'Hardboard'),
        ('other', 'OTHERS'),
        ('none', 'NONE'),
        ])
	walls = fields.Selection([
        ('cement_blocks', 'Cement Blocks'),
        ('glass', 'Glass'),
        ('burnt_bricks', 'Burnt Bricks'),
        ('treated_timber', 'Treated Timber'),
        ('iron_sheet', 'Iron Sheet'),
        ('tree_sticks', 'Tree Sticks/Soil/Soil Bricks'),
        ('other', 'OTHERS'),
        ('none', 'NONE'),
        ])
	windows = fields.Selection([
        ('glass', 'Glass'),
        ('treated_timber', 'Treated Timber'),
        ('treated_timber', 'Treated Timber'),
        ('iron_sheet', 'Iron Sheet'),
        ('marine_board', 'Marine Board'),
        ('other', 'OTHERS'),
        ('none', 'NONE'),
        ])
	doors = fields.Selection([
        ('treated_timber', 'Treated Timber'),
        ('glass', 'Glass'),
        ('iron_sheet', 'Iron Sheet'),
        ('marine_board', 'Marine Board'),
        ('other', 'OTHERS'),
        ('none', 'NONE'),
        ])
	floor = fields.Selection([
        ('tiles', 'Tiles'),
        ('stones', 'Stones'),
        ('terrazo', 'Terrazo'),
        ('treated_timber', 'Treated Timber'),
        ('cement', 'Cement'),
        ('other', 'OTHERS'),
        ('none', 'NONE'),
        ])
	room_counts = fields.Text('Room Count & Use')
	fixture_and_fittng = fields.Text('Fixture & Fitting')
	brif_dis = fields.Text('Brief description of Building')
	main_building = fields.Char()
	out_building = fields.Char()
	site_work = fields.Text()
	services = fields.Selection([
        ('electricity_water_telephone', 'Electricity, Water, Telephone,'),
        ('electricity_water', 'Electricity and Water'),
        ('telephone_electricity ', 'Telephone and electricity '),
        ('electricity_only', 'Electricity Only'),
        ('other', 'OTHERS'),
        ('none', 'NONE'),
        ])
	condition = fields.Text()
	depreciation = fields.Float()

	##########################################
	# Nodes fields only for Building Valuations
	##########################################

	total_area = fields.Float(compute='_compute_area')
	rate_per_meter_square = fields.Float(compute='_compute_rate')
	replacement_cost = fields.Float(compute='_compute_replacement_cost')
	depreciation_factor = fields.Float()
	depreciated_replacement_cost = fields.Float()
	site_works = fields.Float()
	rateable_value = fields.Char()
	say = fields.Char()

	@api.one
	@api.depends('info_id.area')
	def _compute_area(self):
		self.total_area = self.info_id.area

	@api.one
	@api.depends('walls','roof','ceiling','floor','windows','doors','services')
	def _compute_rate(self):
		walls = self.walls
		roof = self.roof
		ceiling = self.ceiling
		floor = self.floor
		windows = self.windows
		doors = self.doors
		services = self.services

		walls_type = {
			'cement_blocks' : 100,
			'glass' : 87.5,
			'burnt_bricks' : 75,
			'treated_timber' : 62.5,
			'iron_sheet' : 50,
			'tree_sticks' : 37.5,
			'other' : 25,
			'none' : 12.5,
			}
		roof_type = {
			'roof_slab' : 100,
			'iron_sheet' : 87.5,
			'cemented_tiles' : 75,
			'tiles_sheets' : 62.5,
			'asbestos' : 50,
			'grass' : 37.5,
			'other' : 25,
			'none' : 12.5,
			}
		ceiling_type = {
			'cement' : 100,
			'gipsum' : 87.5,
			'treated_timber' : 75,
			'hardboard' : 62.5,
			'other' : 50,
			'none' : 37.5,
			}
		floor_type = {
			'tiles' : 100,
			'stones' : 87.5,
			'terrazo' : 75,
			'treated_timber' : 62.5,
			'cement' : 50,
			'other' : 37.5,
			'none' : 25,
			}
		windows_type = {
			'glass' : 100,
			'treated_timber' : 87.5,
			'treated_timber' : 75,
			'iron_sheet' : 62.5,
			'marine_board' : 50,
			'other' : 37.5,
			'none' : 25,
			}
		doors_type = {
			'treated_timber' : 100,
			'glass' : 87.5,
			'iron_sheet' : 75,
			'marine_board' : 62.5,
			'other' : 50,
			'none' : 37.5,
			}
		services_type = {
			'electricity_water_telephone' : 100,
			'electricity_water' : 87.5,
			'telephone_electricity' : 75,
			'electricity_only' : 62.5,
			'other' : 50,
			'none' : 37.5,
			}

		walls = walls_type[walls]
		roof = roof_type[roof]
		ceiling = ceiling_type[ceiling]
		floor = floor_type[floor]
		windows = windows_type[windows]
		doors = doors_type[doors]
		services = services_type[services]
		build_condition = (walls+roof+ceiling+floor+windows+doors+services) / 7

		self.rate_per_meter_square = 10000 * build_condition/100

	@api.one
	@api.depends('rate_per_meter_square','total_area')
	def _compute_replacement_cost(self):
		self.replacement_cost = self.rate_per_meter_square * self.total_area

	@api.onchange('depreciation_factor')
	def _compute_depreciated_replacement_cost(self):
		if self.depreciation_factor:
			self.depreciated_replacement_cost = self.replacement_cost - (self.replacement_cost * (self.depreciation_factor / 100))

	@api.onchange('site_works')
	def _compute_depreciated_site_works(self):
		if self.site_works:
			self.rateable_value = self.depreciated_replacement_cost + (self.depreciated_replacement_cost * (self.site_works / 100))

	info_id = fields.Many2one('building.read',ondelete='cascade')
	tnt_id = fields.Many2one('building.read',ondelete='cascade')
