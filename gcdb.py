from tinydb import TinyDB, where
from tinydb.operations import increment, subtract, add, set


GCplayers = TinyDB("./database/GCplayers.json")
GCenemies = TinyDB("./database/GCenemies.json")
GCitems = TinyDB("./database/GCitems.json")
GCteams = TinyDB("./database/GCteams.json")
GCsplayers = TinyDB("./database/GCsportsplayers.json")


'''
	Retrieves a single passed attribute for a particular player
'''
def getPlayerAttribute(userid, attr):
	data = GCplayers.search(where('id') == userid)
	if len(data) == 1:
		return(data[0][attr])
	else:
		print("Failed to retrieve {} for player {}".format(attr, str(userid)))
		return False

'''
	Changes the attribute in the database for a particular player
'''
def setPlayerAttribute(userid, attr, value):
	try:
		GCplayers.update(set(attr, value), where('id') == userid)
		return True
	except:
		print("Failed to set {} to {} for player {}".format(attr, str(value), str(userid)))
		return False

'''
	Creates a new "Row" in the database for a passed 
	GCUser class. Careful. Don't wanna give someone 
	multiple entries.
'''
def createEntry(gcuser):
	GCplayers.insert({'id': gcuser.userid,
					  'location': gcuser.location,
					  'purity': gcuser.purity,
					  'lofi': gcuser.lofi,
					  'money': gcuser.money})

'''
	Returns the disctionary of a player's stored data,
	if there are multiple or no entries, it returns 
	false.
'''
def getPlayerData(userid):
	data = GCplayers.search(where('id') == userid)
	if len(data) == 1:
		return (data[0])
	else:
		return False

'''
	Removes specified row from enemy db
'''
def deletePlayer(userid):
	deleted_ids = GCplayers.remove(where("id") == userid)
	if len(deleted_ids) < 1:
		print("Failed to remove enemy with id {}".format(str(userid)))
	elif len(deleted_ids) > 1:
		print("Removed {} enemies with id {}".format(str(len(deleted_ids)), str(userid)))

'''
	Retrieves a single passed attribute for a particular enemy
'''
def getEnemyAttribute(id, attr):
	data = GCenemies.search(where('id') == id)
	if len(data) == 1:
		return (data[0][attr])
	else:
		print("Failed to retrieve {} for player {}".format(attr, str(id)))
		return False

'''
	Changes an attribute in the database for a particular enemy
'''
def setEnemyAttribute(id, attr, value):
	try:
		GCenemies.update(set(attr, value), where('id') == id)
		return True
	except:
		print("Failed to set {} to {} for player {}".format(attr, str(value), str(id)))
		return False

'''
	Creates a new "Row" in the database for a passed 
	GCEnemy class. Should only be called on creation 
	of new enemy
'''
def createEnemyEntry(gcenemy):
	GCenemies.insert({'id': gcenemy.id,
					  'name': gcenemy.name,
					  'location': gcenemy.location,
					  'size': gcenemy.size,
					  'hp': gcenemy.hp,
					  'attacks': gcenemy.attacks})

'''
	Returns the dictionary of a enemy's stored data,
	if there are multiple or no entries, it returns 
	false.
'''
def getEnemyData(id):
	data = GCenemies.search(where('id') == id)
	if len(data) == 1:
		return (data[0])
	else:
		return False

'''
	Return list of all enemies with matching key/value
	pairs.
'''
def findEnemies(key, value):
	data = GCenemies.search(where(key) == value)
	if len(data) >= 1:
		return (data)
	else:
		return False

'''
	Removes specified row from enemy db
'''
def deleteEnemy(id):
	deleted_ids = GCenemies.remove(where("id") == id)
	if len(deleted_ids) < 1:
		print("Failed to remove enemy with id {}".format(str(id)))
	elif len(deleted_ids) > 1:
		print("Removed {} enemies with id {}".format(str(len(deleted_ids)), str(id)))

'''
	ITEM DATABASE COMMANDS START HERE
'''

def getItemData(id):
	data = GCitems.search(where('id') == id)
	#print(len(data))
	if len(data) >= 1:
		return (data[0])
	else:
		return False

def createItem(gcitem):
	GCitems.insert({'id': gcitem.id,
					'name': gcitem.name,
					'ownerid': gcitem.ownerid,
					'itemtype': gcitem.itemtype,
					'adorner': gcitem.adorner,
					'equipper': gcitem.equipper,
					'level': gcitem.level,
					'xp': gcitem.xp,
					'known_spells': gcitem.known_spells,
					
	})
	
def finditems(key, value):
	data = GCitems.search(where(key) == value)
	if len(data) >= 1:
		return (data)
	else:
		return False

def getItemAttribute(id, attr):
	data = GCitems.search(where('id') == id)
	if len(data) == 1:
		return (data[0][attr])
	else:
		print("Failed to retrieve {} for item {}".format(attr, str(id)))
		return False

def setItemAttribute(id, attr, value):
	try:
		GCitems.update(set(attr, value), where('id') == id)
		return True
	except:
		print("Failed to set {} to {} for item {}".format(attr, str(value), str(id)))
		return False


'''
	TEAM DATABASE COMMANDS START HERE
'''

def getTeamData(id):
	data = GCteams.search(where('id') == id)
	#print(len(data))
	if len(data) >= 1:
		return (data[0])
	else:
		return False

def createTeamEntry(gcteam):
	GCteams.insert({'id': gcteam.id,
					'name': gcteam.name,
					'emoji': gcteam.emoji,
					'wins': gcteam.wins,
					'losses': gcteam.losses,
					'pizzaz': gcteam.pizzaz
	})

def findteam(key, value):
	data = GCteams.search(where(key) == value)
	if len(data) >= 1:
		return(data)
	else:
		return False
		
def getTeamAttribute(id, attr):
	data = GCteams.search(where('id') == id)
	if len(data) == 1:
		return (data[0][attr])
	else:
		print("Failed to retrieve {} for item {}".format(attr, str(id)))
		return False

def setTeamAttribute(id, attr, value):
	try:
		GCteams.update(set(attr, value), where('id') == id)
		return True
	except:
		print("Failed to set {} to {} for item {}".format(attr, str(value), str(id)))
		return False


'''
	DATABASE FOR SPORTS PLAYERS
'''

def getSPlayerData(id):
	data = GCsplayers.search(where('id') == id)
	#print(len(data))
	if len(data) >= 1:
		return (data[0])
	else:
		return False

def createSPlayerEntry(gcsplayer):
	GCsplayers.insert({'id': gcsplayer.id,
					'teamid': gcsplayer.teamid,
					'name': gcsplayer.name,
					'wins': gcsplayer.wins,
					'losses': gcsplayer.losses,
					'power': gcsplayer.power,
					'determination': gcsplayer.determination,
					'spirit': gcsplayer.spirit,
					'chill': gcsplayer.chill,
					'goonery': gcsplayer.goonery,
					'cringe': gcsplayer.cringe
	})

def findSPlayer(key, value):
	data = GCsplayers.search(where(key) == value)
	if len(data) >= 1:
		return(data)
	else:
		return False
		
def getSPlayerAttribute(id, attr):
	data = GCsplayers.search(where('id') == id)
	if len(data) == 1:
		return (data[0][attr])
	else:
		print("Failed to retrieve {} for item {}".format(attr, str(id)))
		return False

def setSPlayerAttribute(id, attr, value):
	try:
		GCsplayers.update(set(attr, value), where('id') == id)
		return True
	except:
		print("Failed to set {} to {} for item {}".format(attr, str(value), str(id)))
		return False
