from arches.app.models import models

class SummaryGenerator:

	def __init__(self):

		self._properties = [] # ['5297fa9f-8e16-11ea-a6a6-02e7594ce0a0', 'ID'], ['34cfe992-c2c0-11ea-9026-02e7594ce0a0', 'ID'], ['5297faa9-8e16-11ea-a6a6-02e7594ce0a0', 'Actor'], ['d2e1ab96-cc05-11ea-a292-02e7594ce0a0', 'Role'], ['34cfea8a-c2c0-11ea-9026-02e7594ce0a0', 'Actor'], ['34cfea43-c2c0-11ea-9026-02e7594ce0a0', 'Country']]
		self._cached_summaries = {}

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
					ret[rid] = {}
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

