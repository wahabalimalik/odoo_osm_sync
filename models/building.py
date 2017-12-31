# -*- coding: utf-8 -*-

from odoo import models, fields, api
from ..controllers import main

class BuildInfo(models.Model):
	_name = 'build.info'
	_rec_name = 'bus_ids'

	#####################################################
	# Below varibles are building information
	# which we want to upload to OSM database.
	#####################################################

	bus_ids = fields.Many2one('building.read',string='Property Ref No #')
	
	property_name = fields.Char('Property Name')
	ward = fields.Char()
	sub_ward = fields.Char()
	street = fields.Char()
	plot_no = fields.Char()
	post_code_no = fields.Char()
	user = fields.Char()
	tenure = fields.Char()
	owner = fields.Char()
	address = fields.Char()
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
	floor = fields.Selection([
        ('tiles', 'Tiles'),
        ('stones', 'Stones'),
        ('terrazo', 'Terrazo'),
        ('treated_timber', 'Treated Timber'),
        ('cement', 'Cement'),
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
	state = fields.Selection([
        ('complete', 'Complete'),
        ('incomplete', 'Inomplete'),
        ])
	services = fields.Selection([
        ('electricity_water_telephone', 'Electricity, Water, Telephone,'),
        ('electricity_water', 'Electricity and Water'),
        ('telephone_electricity ', 'Telephone and electricity '),
        ('electricity_only', 'Electricity Only'),
        ('other', 'OTHERS'),
        ('none', 'NONE'),
        ])
	discription = fields.Text()
	room_counts = fields.Text('Room Count & Use')
	fixture_and_fittng = fields.Text('Fixture & Fitting')
	brif_dis = fields.Text('Brief description of Building')
	main_building = fields.Char()
	out_building = fields.Char()
	site_work = fields.Text()
	condition = fields.Text()
	depreciation = fields.Float()

	#####################################################
	# Below function is a dispatch data to dispatch_rpc() 
	# function where it will redirect to appropriate 
	# controller 
	#####################################################

	@api.multi
	def create_build_data(self):
		data = {
			"params": {
				"bus_ids" : self.bus_ids.bus_ids,
				"property_name" : self.property_name,
				"ward" : self.ward,
				"sub_ward" : self.sub_ward,
				"street" : self.street,
				"plot_no" : self.plot_no,
				"post_code_no" : self.post_code_no,
				"user" : self.user,
				"tenure" : self.tenure,
				"owner" : self.owner,
				"address" : self.address,
				"walls" : self.walls,
				"roof" : self.roof,
				"ceiling" : self.ceiling,
				"floor" : self.floor,
				"windows" : self.windows,
				"doors" : self.doors,
				"state" : self.state,
				"services" : self.services,
				"discription" : self.discription,
				"room_counts" : self.room_counts,
				"fixture_and_fittng" : self.fixture_and_fittng,
				"brif_dis" : self.brif_dis,
				"main_building" : self.main_building,
				"out_building" : self.out_building,
				"site_work" : self.site_work,
				"condition" : self.condition,
				"depreciation" : self.depreciation,
			}
		}
		main.dispatch_rpc(category = 'build_info' ,data = data)