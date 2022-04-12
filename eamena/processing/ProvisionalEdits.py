from django.contrib.auth.models import User
from arches.app.models import models

def get_provisional_edits_by_user(username):

	uid = 0
	if not(username is None):
		try:
			uid = int(User.objects.get(username=username).pk)
		except:
			return models.TileModel.objects.none()
	return models.TileModel.objects.filter(provisionaledits__has_key=str(uid))

def apply_provisional_edits(tile, overwrite=False, username=None):

	uid = 0
	if not(username is None):
		try:
			uid = int(User.objects.get(username=username).pk)
		except:
			uid = -1 # Use an invalid number so nothing will be returned

	data = tile.data
	dirty = False
	users = tile.provisionaledits.keys()
	for userkey in users:
		user = int(str(userkey))
		if uid != 0:
			if user != uid:
				continue
		changes = tile.provisionaledits[str(user)]
		if not('value' in changes):
			continue
		if not('action' in changes):
			continue
		if changes['action'] != 'create':
			if not(overwrite & (changes['action'] == 'update')):
				continue
		for id_uuid in changes['value'].keys():
			id = str(id_uuid)
			if id in data:
				if overwrite==False:
					continue
			value = changes['value'][id]
			data[id] = value
			dirty = True
	if dirty:
		tile.data = data
		tile.provisionaledits = None
		tile.save()

	return dirty

