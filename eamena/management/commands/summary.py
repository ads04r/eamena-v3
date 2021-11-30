from django.contrib.auth.models import User
from django.http import HttpRequest
from arches.app.models import models
from arches.app.models.concept import Concept, get_preflabel_from_valueid, get_valueids_from_concept_label
from arches.app.views import search
from django.core.management.base import BaseCommand
from eamena.bulk_uploader import HeritagePlaceBulkUploadSheet, GridSquareBulkUploadSheet
from eamena.statistics import SummaryGenerator
from geomet import wkt
import json, os, sys, logging, re, uuid, hashlib, datetime, warnings

logger = logging.getLogger(__name__)

def relations(graphid, role=None):

	if role is None:
		ret = models.ResourceInstance.objects.filter(graph_id=graphid).distinct()
	else:
		ret = models.ResourceInstance.objects.filter(graph_id=graphid, resxres_resource_instance_ids_to__resourceinstanceidfrom__tilemodel__data__icontains=role).distinct()
	return ret

def get_countries(sg):

	nodeid = '34cfea43-c2c0-11ea-9026-02e7594ce0a0'
	ret = {}
	for item in sg.find_concepts(nodeid):
		id = item['valueid']
		ret[id] = item
	return ret

def get_grid_squares(sg):

	grid_id = '77d18973-7428-11ea-b4d0-02e7594ce0a0'
	grid_id_id = 'b3628db0-742d-11ea-b4d0-02e7594ce0a0'
	return sg.find_objects(grid_id, grid_id_id)

def get_people(sg):

	p_id = 'e98e1cee-c38b-11ea-9026-02e7594ce0a0'
	p_id_id = 'e98e1cfe-c38b-11ea-9026-02e7594ce0a0'
	return sg.find_objects(p_id, p_id_id)

def get_summaries():

	gen = SummaryGenerator()

	grids = get_grid_squares(gen)
	people = get_people(gen)
	country_lookup = get_countries(gen)

	properties = [
		['5297fa9f-8e16-11ea-a6a6-02e7594ce0a0', 'ID'],
		['34cfe992-c2c0-11ea-9026-02e7594ce0a0', 'ID'],
		['5297faa9-8e16-11ea-a6a6-02e7594ce0a0', 'Actor'],
		['34cfea8a-c2c0-11ea-9026-02e7594ce0a0', 'Actor'],
		['d2e1ab96-cc05-11ea-a292-02e7594ce0a0', 'Role'],
		['40c49e8c-cc08-11ea-a292-02e7594ce0a0', 'Role'],
		['34cfea43-c2c0-11ea-9026-02e7594ce0a0', 'Country'],
		['61ad1129-c7f1-11ea-a292-02e7594ce0a0', 'Country'],
		['34cfea5d-c2c0-11ea-9026-02e7594ce0a0', 'Grid'],
		['61ad1121-c7f1-11ea-a292-02e7594ce0a0', 'Grid']
	]
	for prop in properties:
		gen.add_property(prop[1], prop[0])

	ret = {}
	sum = gen.get_summaries()

	for k in sum.keys():
		kk = str(k)
		item = sum[kk]
		if 'Grid' in item:
			if item['Grid'] in grids:
				id = item['Grid']
				item['Grid'] = grids[id]['label']
		if 'Actor' in item:
			if item['Actor'] in people:
				id = item['Actor']
				item['Actor'] = people[id]['label']
		if 'Country' in item:
			if item['Country'] in country_lookup:
				id = item['Country']
				item['Country'] = country_lookup[id]['label']
		ret[kk] = item
	return ret

class Command(BaseCommand):
	"""
	Command for extracting information useful for reporting purposes.

	"""

	def handle(self, *args, **options):

		marea = '270e5b36-4d18-4b6e-a7ee-c49e3d301620'
		eamena = 'b3c1325c-e837-46ab-9e71-514b42de3cba'

		summary = get_summaries()
		print(json.dumps(summary))

