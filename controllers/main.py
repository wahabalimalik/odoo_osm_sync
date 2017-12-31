# -*- coding: utf-8 -*-

from odoo import http
import requests,json
from bs4 import BeautifulSoup
from osmapi import OsmApi
import logging
import numpy as np
from shapely.geometry import Point, shape
from shapely.geometry.polygon import Polygon
import pyproj
from shapely.ops import transform
from functools import partial

_logger = logging.getLogger(__name__)

#####################################################
# DOMAIN,PORT,USERNAME,PASSWORD should be enter 
# in Yaml file in future.
#####################################################
DOMAIN = "localhost"
PORT = "8069"
USERNAME = u"dsmw1o1"
PASSWORD = u"Loveodoo"
headers = {'Content-Type': 'application/json'}

def dispatch_rpc(category,data):
	requests.post(
	'http://%s:%s/details/%s/' %(DOMAIN,PORT,category),
	headers=headers,
	data=json.dumps(data)
	)

class Osm(http.Controller):

	############################################
	# Creating Owner on OSM
	############################################
	@http.route('/details/owner', type='json', auth="none")
	def create_owner(self, **kw):

		#####################################################
		# Assign values to local variables
		#####################################################

		bus_ids = http.request.params['bus_ids']

		owner = http.request.params['name']
		citizen = http.request.params['citizen']
		vrn = http.request.params['vrn']
		assess = http.request.params['assess']
		branch = http.request.params['branch']
		tax = http.request.params['tax']
		tin = http.request.params['tin']
		efd = http.request.params['efd']
		valued = http.request.params['valued']
		tenants_id = http.request.params['tenants_id']

		#####################################################
		# Getting building boarder nodes
		#####################################################

		r = requests.get(
			'http://www.openstreetmap.org/api/0.6/way/%s/full'
			%(bus_ids)
			)

		response = BeautifulSoup(r.text)

		nodes = response.osm.findAll("node")

		lat = 0
		lon = 0

		for x in nodes:
			lat = lat + float(x['lat'])
			lon = lon + float(x['lon'])
		lat = lat / len(nodes)
		lon = lon / len(nodes)

		#####################################################
		# Conneting to OSM through api
		#####################################################

		MyApi = OsmApi(username = USERNAME, password = PASSWORD)

		#####################################################
		# Info about changeset
		#####################################################

		MyApi.ChangesetCreate({u"comment": u"Adding One of the Owner of building"})
		
		#####################################################
		# Create Node
		#####################################################

		MyApi.NodeCreate(
			{
				u"lon":lon, 
				u"lat":lat, 
				u"tag": {
					u"owner":u"%s" %(owner),
					u"citizen":u"%s" %(citizen),
					u"vrn":u"%s" %(vrn),
					u"assess":u"%s" %(assess),
					u"branch":u"%s" %(branch),
					u"tax":u"%s" %(tax),
					u"tin":u"%s" %(tin),
					u"efd":u"%s" %(efd),
					u"valued":u"%s" %(valued),
					u"tenants_id":u"%s" %(tenants_id),
				}
			})

	############################################
	# Creating Tenant on OSM
	############################################
	@http.route('/details/tenant', type='json', auth="none")
	def create_tenant(self, **kw):

		#####################################################
		# Assign values to local variables
		#####################################################

		bus_ids = http.request.params['bus_ids']

		tenant = http.request.params['tenant']
		citizen = http.request.params['citizen']
		rent = http.request.params['rent']
		vrn = http.request.params['vrn']
		assess = http.request.params['assess']
		branch = http.request.params['branch']
		tax = http.request.params['tax']
		tin = http.request.params['tin']
		efd = http.request.params['efd']
		valued = http.request.params['valued']

		#####################################################
		# Getting building boarder nodes
		#####################################################

		r = requests.get(
			'http://www.openstreetmap.org/api/0.6/way/%s/full'
			%(bus_ids)
			)

		response = BeautifulSoup(r.text)

		nodes = response.osm.findAll("node")

		lat = 0
		lon = 0

		for x in nodes:
			lat = lat + float(x['lat'])
			lon = lon + float(x['lon'])
		lat = lat / len(nodes)
		lon = lon / len(nodes)

		#####################################################
		# Conneting to OSM through api
		#####################################################

		MyApi = OsmApi(username = USERNAME, password = PASSWORD)

		#####################################################
		# Info about changeset
		#####################################################

		MyApi.ChangesetCreate({u"comment": u"Adding One of the Tenant of building"})
		
		#####################################################
		# Create Node
		#####################################################
		
		MyApi.NodeCreate(
			{
				u"lon":lon, 
				u"lat":lat, 
				u"tag": {
					u"tenant":u"%s" %(tenant),
					u"citizen":u"%s" %(citizen),
					u"rent":u"%s" %(rent),
					u"vrn":u"%s" %(vrn),
					u"assess":u"%s" %(assess),
					u"branch":u"%s" %(branch),
					u"tax":u"%s" %(tax),
					u"tin":u"%s" %(tin),
					u"efd":u"%s" %(efd),
					u"valued":u"%s" %(valued),
				}
			})

	############################################
	# ADDING Building  on OSM
	############################################
	@http.route('/details/build_info', type='json', auth="none")
	def create_building_information(self, **kw):

		#####################################################
		# Assign values to local variables
		#####################################################

		bus_ids = http.request.params['bus_ids']

		property_name = http.request.params['property_name']
		ward = http.request.params['ward']
		sub_ward = http.request.params['sub_ward']
		street = http.request.params['street']
		plot_no = http.request.params['plot_no']
		post_code_no = http.request.params['post_code_no']
		user = http.request.params['user']
		tenure = http.request.params['tenure']
		owner = http.request.params['owner']
		address = http.request.params['address']
		walls = http.request.params['walls']
		roof = http.request.params['roof']
		ceiling = http.request.params['ceiling']
		floor = http.request.params['floor']
		windows = http.request.params['windows']
		doors = http.request.params['doors']
		state = http.request.params['state']
		services = http.request.params['services']
		discription = http.request.params['discription']
		room_counts = http.request.params['room_counts']
		fixture_and_fittng = http.request.params['fixture_and_fittng']
		brif_dis = http.request.params['brif_dis']
		main_building = http.request.params['main_building']
		out_building = http.request.params['out_building']
		site_work = http.request.params['site_work']
		condition = http.request.params['condition']
		depreciation = http.request.params['depreciation']

		#####################################################
		# Getting building boarder nodes
		#####################################################

		r = requests.get(
			'http://www.openstreetmap.org/api/0.6/way/%s/full'
			%(bus_ids)
			)

		response = BeautifulSoup(r.text)

		nodes = response.osm.findAll("node")

		lat = 0
		lon = 0

		for x in nodes:
			lat = lat + float(x['lat'])
			lon = lon + float(x['lon'])
		lat = lat / len(nodes)
		lon = lon / len(nodes)

		#####################################################
		# Conneting to OSM through api
		#####################################################

		MyApi = OsmApi(username = USERNAME, password = PASSWORD)

		#####################################################
		# Info about changeset
		#####################################################

		MyApi.ChangesetCreate(
			{
				u"comment": u"Adding Building related Information"
			})
		
		#####################################################
		# Create Node
		#####################################################
		
		MyApi.NodeCreate(
			{
				u"lon":lon, 
				u"lat":lat, 
				u"tag": {
					u"property_name":u"%s" %(property_name),
					u"ward":u"%s" %(ward),
					u"sub_ward":u"%s" %(sub_ward),
					u"street":u"%s" %(street),
					u"plot_no":u"%s" %(plot_no),
					u"post_code_no":u"%s" %(post_code_no),
					u"user":u"%s" %(user),
					u"tenure":u"%s" %(tenure),
					u"owner":u"%s" %(owner),
					u"address":u"%s" %(address),
					u"state":u"%s" %(state),
					u"discription":u"%s" %(discription),
					u"roof":u"%s" %(roof),
					u"ceiling":u"%s" %(ceiling),
					u"walls":u"%s" %(walls),
					u"windows":u"%s" %(windows),
					u"doors":u"%s" %(doors),
					u"floor":u"%s" %(floor),
					u"room_counts":u"%s" %(room_counts),
					u"fixture_and_fittng":u"%s" %(fixture_and_fittng),
					u"brif_dis":u"%s" %(brif_dis),
					u"main_building":u"%s" %(main_building),
					u"out_building":u"%s" %(out_building),
					u"site_work":u"%s" %(site_work),
					u"services":u"%s" %(services),
					u"condition":u"%s" %(condition),
					u"depreciation":u"%s" %(depreciation),
				}
			})

	############################################
	# Retriving results
	############################################
	@http.route('/details/business', type='json', auth="none")
	def osm_overpass(self, **kw):
		_logger.info('Receive info for id : %s' %(http.request.params["bus_ids"]))

		##########################################
		# Assign Variables
		##########################################

		bus_ids = http.request.params["bus_ids"]
		street = http.request.params["street"]
		name = http.request.params["name"]
		building = http.request.params["building"]
		levels = http.request.params["levels"]
		material = http.request.params["material"]
		shop = http.request.params["shop"]
		types = http.request.params["types"]
		amenity = http.request.params["amenity"]
		
		bus_ids = int(str(bus_ids).replace(',',''))

		##########################################
		# Creating polygon
		##########################################

		query = "[timeout:10][out:json];way(%s);(._;>;);out body;" %(bus_ids)
		
		r = requests.get(
			"http://overpass-api.de/api/interpreter?data=%s" %(query)
			)

		data = json.loads(r.text)
		cordinates = []

		for y in [x['nodes'] for x in data['elements'] if x["type"] == 'way'][0]:
			cordinates.append([(x['lat'], x['lon'] )for x in data['elements'] if x["id"] == y][0])
		
		building_polygon = np.array(cordinates)

		##########################################
		# Calculate area of polygon
		##########################################

		geom = {
			'type': 'Polygon',
			'coordinates': [building_polygon]
			}

		s = shape(geom)

		proj = partial(
			pyproj.transform, pyproj.Proj(init='epsg:4326'),
			pyproj.Proj(init='epsg:3857')
			)

		s_new = transform(proj, s)
		projected_area = transform(proj, s).area
		
		##########################################
		# Retrive nodes near Cordinates
		##########################################

		min_lat = building_polygon.min(axis=0)[0]
		min_lon = building_polygon.min(axis=0)[1]
		max_lat = building_polygon.max(axis=0)[0]
		max_lon = building_polygon.max(axis=0)[1]

		data = """[timeout:10][out:json];
		node(%s,%s,%s,%s);
		(._;>;);
		out;""" %(min_lat,min_lon,max_lat,max_lon,)

		_logger.info('Sending request for nodes near building')

		r = requests.get(
			"http://overpass-api.de/api/interpreter?data=%s" %(data)
			)
		
		_logger.info('Receive all nodes near building')
		
		##########################################
		# Filter data and assign requried data 
		# to keys in dictionary.
		##########################################

		data = json.loads(r.text)
		data = data['elements']
		polygon = Polygon(cordinates)
		row_data = []
		len_tup = 0

		for x in data:
			if 'tags' in x and polygon.contains(Point(float(str(x['lat'])),float(str(x['lon'])))):
				
				_logger.info('looping through data')
				
				row_data.append((0,len_tup,{

					##########################################
					# Constant fields for all nodes
					##########################################

					'types' : str(x['type'] if 'type' in x else "Nr"),
					'bus_ids' : str(x['id'] if 'id' in x else "Nr"),
					'lat' : str(x['lat'] if 'lat' in x else "Nr"),
					'lon' : str(x['lon'] if 'lon' in x else "Nr"),
					'name' : str(x['tags']['name'] if 'name' in x['tags'] else "Nr"),
					'shop' : str(x['tags']['shop'] if 'shop' in x['tags'] else "Nr"),
					'amenity' : str(x['tags']['amenity'] if 'amenity' in x['tags'] else "Nr"),

					##########################################
					# Nodes fields only for Tenants
					##########################################

					'tenant' : str(x['tags']['tenant'] if 'tenant' in x['tags'] else "Nr"),
					'rent' : str(x['tags']['rent'] if 'rent' in x['tags'] else "Nr"),

					##########################################
					# Nodes fields only for Owner
					##########################################

					'tenants_id' : str(x['tags']['tenants_id'] if 'tenants_id' in x['tags'] else "Nr"),

					##########################################
					# Nodes fields common for Owner and Tenant
					##########################################
					'citizen' : str(x['tags']['citizen'] if 'citizen' in x['tags'] else "Nr"),
					'vrn' : str(x['tags']['vrn'] if 'vrn' in x['tags'] else "Nr"),
					'assess' : str(x['tags']['assess'] if 'assess' in x['tags'] else "Nr"),
					'branch' : str(x['tags']['branch'] if 'branch' in x['tags'] else "Nr"),
					'tax' : str(x['tags']['tax'] if 'tax' in x['tags'] else "Nr"),
					'tin' : str(x['tags']['tin'] if 'tin' in x['tags'] else "Nr"),
					'efd' : str(x['tags']['efd'] if 'efd' in x['tags'] else "Nr"),
					'valued' : str(x['tags']['valued'] if 'valued' in x['tags'] else "Nr"),

					##########################################
					# Nodes fields common for Owner and Building 
					# Information
					###################################

					'owner' : str(x['tags']['owner'] if 'owner' in x['tags'] else "Nr"),

					##########################################
					# Nodes fields only for Building Information
					##########################################

					'property_name':str(x['tags']['property_name'] if 'property_name' in x['tags'] else "Nr"), 
					'ward':str(x['tags']['ward'] if 'ward' in x['tags'] else "Nr"), 
					'sub_ward':str(x['tags']['sub_ward'] if 'sub_ward' in x['tags'] else "Nr"),
					'street':str(x['tags']['street'] if 'street' in x['tags'] else "Nr"), 
					'plot_no':str(x['tags']['plot_no'] if 'plot_no' in x['tags'] else "Nr"), 
					'post_code_no':str(x['tags']['post_code_no'] if 'post_code_no' in x['tags'] else "Nr"),
					'user':str(x['tags']['user'] if 'user' in x['tags'] else "Nr"), 
					'tenure':str(x['tags']['tenure'] if 'tenure' in x['tags'] else "Nr"),
					'address':str(x['tags']['address'] if 'address' in x['tags'] else "Nr"), 
					'state':str(x['tags']['state'] if 'state' in x['tags'] else 'complete'), 
					'discription':str(x['tags']['discription'] if 'discription' in x['tags'] else "Nr"), 
					'roof':str(x['tags']['roof'] if 'roof' in x['tags'] else "none"), 
					'ceiling':str(x['tags']['ceiling'] if 'ceiling' in x['tags'] else "none"),
					'walls':str(x['tags']['walls'] if 'walls' in x['tags'] else "none"), 
					'windows':str(x['tags']['windows'] if 'windows' in x['tags'] else "none"), 
					'doors':str(x['tags']['doors'] if 'doors' in x['tags'] else 'none'), 
					'floor':str(x['tags']['floor'] if 'floor' in x['tags'] else 'none'), 
					'room_counts':str(x['tags']['room_counts'] if 'room_counts' in x['tags'] else "Nr"), 
					'fixture_and_fittng':str(x['tags']['fixture_and_fittng'] if 'fixture_and_fittng' in x['tags'] else "Nr"), 
					'brif_dis':str(x['tags']['brif_dis'] if 'brif_dis' in x['tags'] else "Nr"), 
					'main_building':str(x['tags']['main_building'] if 'main_building' in x['tags'] else "Nr"), 
					'out_building':str(x['tags']['out_building'] if 'out_building' in x['tags'] else "Nr"), 
					'site_work':str(x['tags']['site_work'] if 'site_work' in x['tags'] else "Nr"), 
					'services':str(x['tags']['services'] if 'services' in x['tags'] else "none"),
					'condition':str(x['tags']['condition'] if 'condition' in x['tags'] else "Nr"), 
					'depreciation':str(x['tags']['depreciation'] if 'depreciation' in x['tags'] else 0), 
				}))

				len_tup = len_tup +1

		_logger.info('Pushing data to table')

		##########################################
		# Adding all info into res
		##########################################

		res = {
			'bus_ids' : bus_ids,
			'street' : street,
			'name' : name,
			'building' : building,
			'levels' : levels,
			'material' : material,
			'shop' : shop,
			'types' : types,
			'amenity' : amenity,
			'area' : projected_area,
			'info_data' : row_data
		}

		##########################################
		# Delete privous record of Building Nodes
		##########################################

		http.request.env['building.read'].sudo().search([]).unlink()

		##########################################
		# Adding new record of Building Nodes
		##########################################
		res = http.request.env['building.read'].sudo().create(res)
		
		return res.id