from arches.app.models import models
from arches.app.models.concept import Concept, get_preflabel_from_valueid, get_valueids_from_concept_label

class SummaryGenerator:

	def __init__(self):

		self._properties = []
		self._cached_summaries = {}

	def find_concepts(self, nodeid):

		ret = []
		node = models.Node.objects.get(nodeid=nodeid)

		if 'rdmCollection' in node.config:
			conceptid = node.config['rdmCollection']
			if not(conceptid is None):
				for item in Concept().get_e55_domain(conceptid):
					valueobj = get_preflabel_from_valueid(item['id'], 'en')
					valueid = valueobj['id']
					label = get_preflabel_from_valueid(valueid, 'en')
					ret.append({'valueid': valueid, 'conceptid': item['conceptid'], 'label': label['value']})
		return ret

	def find_objects(self, graph_id, identifier_id):

		ret = {}
		for item in models.TileModel.objects.filter(resourceinstance__graph_id=graph_id, nodegroup_id=identifier_id):
			id = str(item.resourceinstance_id)
			value = {'id': id}
			if item.data:
				if isinstance(item.data, (dict)):
					if identifier_id in item.data:
						value['label'] = item.data[identifier_id]
			ret[id] = value
		return ret

	def add_property(self, label, uuid):

		self._properties.append([str(uuid), str(label)])
		self._cached_summaries = {}

	def get_summaries(self):

		if len(self._cached_summaries) > 0:
			return self._cached_summaries

		ret = {}
		for prop in self._properties:
			k = prop[0]
			label = prop[1]
			for tile in models.TileModel.objects.filter(data__icontains=k): # , nodegroup_id='34cfea2e-c2c0-11ea-9026-02e7594ce0a0'):
				rid = str(tile.resourceinstance_id)
				if not(rid in ret):
					ri = models.ResourceInstance.objects.get(resourceinstanceid=rid)
					ret[rid] = {'Date': ri.createdtime.strftime("%Y-%m-%d")}
				data = tile.data[k]
				if isinstance(data, (list)):
					if len(data) == 0:
						continue
					data = data[0]
				if isinstance(data, (dict)):
					if 'resourceId' in data:
						data = data['resourceId']
				ret[rid][label] = data

		self._cached_summaries = ret
		return ret

