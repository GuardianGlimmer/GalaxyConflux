import discord 

import gccfg
import gcdb

from tinydb import Query


GCplayers = gcdb.GCplayers
GCitems = gcdb.GCitems

class GCPlayer:
	# setup default values
	def __init__(
		self,
		userid = 0,
		location = "downtown",
		purity = "pure",
		lofi = 0,
		money = 0,
		hunger = 0,
		health = 100,
		level = 1,
		xp = 0,
		known_spells = []
	):
		# Check for and possibly load saved data
		SavedData = gcdb.getPlayerData(userid)
		if SavedData:
			self.userid = userid
			self.location = SavedData["location"]
			self.purity = SavedData["purity"]
			self.lofi = SavedData["lofi"]
			self.money = SavedData["money"]
			self.hunger = SavedData["hunger"]
			self.health = SavedData["health"]
			self.level = SavedData["level"]
			self.xp = SavedData["xp"]
			self.known_spells = SavedData["known_spells"]
			self.new = False
		# Or initialize from given values
		else:
			self.userid = userid
			self.location = location
			self.purity = purity
			self.lofi = lofi
			self.money = money
			self.hunger = hunger
			self.health = health
			self.level = level
			self.xp = xp
			self.known_spells = known_spells
			self.persist()
			self.new = True

	def persist(self):
		User = Query()
		GCplayers.upsert({
			'id': self.userid,
			'location': self.location,
			'purity': self.purity,
			'lofi': self.lofi,
			'money': self.money,
			'hunger': self.hunger,
			'health': self.health,
			'level': self.level,
			'xp': self.xp,
			'known_spells': self.known_spells
		},
		User.id == self.userid
		)
		print("UPSERT")
		"""
		# Grab existing data
		SavedData = gcdb.getPlayerData(self.userid)

		# Iterate through all saved values
		for key in SavedData:
			if SavedData[key] != self.key:
				# Only Bother with changed values
				gcdb.setPlayerAttribute(self.userid, key, self.key)
		"""

		""" Handle loss of health """
	def change_hp(self, amount, source):
		maxhp = int(100 + (self.level * 10))
		self.purity = "pure"
		self.health += amount
		if self.health > maxhp:
			self.health = maxhp
		if self.health <= 0:
			self.die(source)
		self.persist()

	""" 
		Handle everything that might happen on death, resetting to a hosopital
		losing some money, maybe some purity, etc
	"""
	def die(self, source):
		if source == gccfg.damage_source_combat:
			gccfg.fights[self.location].player_ids.remove(self.userid)
			# TODO: potential monster buffs for kills
		self.money -= gccfg.death_cost
		self.health = int(100 + (self.level * 10))
		# Lower purity tier or something?
		self.purity = "corrupted"
		self.location  = "study-hall"
		self.persist()

	def lvlup(self):
		if self.xp >= 500 * ((self.level ^ 2) * .5):
			self.level += 1
			self.xp = 0
			self.persist()

	def change_xp(self, amount):
		self.xp += amount
		print("added xp")
		self.lvlup()
		self.persist()

	def add_value(self, value, amount):
		self.value += amount
		print("added %s to %s" % (amount, value))
		self.lvlup()
		self.persist()
		
	def change_money(self, amount):
		self.money += amount
		print("added money")
		self.persist()


		
		
class GCEnemy:
	# Set default values
	def __init__(
			self,
			name = "",
			id = 0,
			location = "",
			size = 0,
			hp = 0,
			attacks = []
	):
		SavedData = gcdb.getEnemyData(id)
		if SavedData:
			self.id = id
			self.name = SavedData["name"]
			self.location = SavedData["location"]
			self.size = SavedData["size"]
			self.hp = SavedData["hp"]
			self.attacks = SavedData["attacks"]
		else:
			self.id = id
			self.name = name
			self.location = location
			self.size = size
			self.hp = self.SizeToHP(size) if hp == 0 else hp
			self.attacks = self.getAttacks(size) if attacks == [] else attacks
			gcdb.createEnemyEntry(self)

	""" Save new data to the database """
	def persist(self):
		# Grab existing data
		SavedData = gcdb.getEnemyData(self.id)

		# Iterate through all saved values
		for key in SavedData:
			if key != 'id' and SavedData[key] != getattr(self, key):
				# Only Bother with changed values
				gcdb.setEnemyAttribute(self.id, key, getattr(self, key))

	""" Return starting HP based on enemy size """
	def SizeToHP(self, size):
		return (size * 20)

	""" Grab 3 damage attacks at random """
	def getAttacks(self, size):
		attacks = []
		for spell in gccfg.spells:
			if spell.type == gccfg.spell_type_damage and gccfg.spell_user_enemy in spell.users:
				attacks.append(spell.name)
		return attacks

	def changeHp(self, amount):
		self.hp += amount
		if self.hp <= 0:
			self.die()
		else:
			self.persist()

	def die(self):
		gcdb.deleteEnemy(self.id)
		gccfg.fights[self.location].deceased_enemies.append(self.size)
		gccfg.fights[self.location].enemy_ids.remove(self.id)
		# TODO: distribute rewards to players left in fight?


class GCLocation:
	def __init__(self, _id, _json_entry = None):
		self.id = _id
		self.role_name = _json_entry.get("role_name")
		self.full_name = _json_entry.get("full_name")
		self.names = _json_entry.get("location_names")
		self.look_txt = _json_entry.get("look_txt")

		#attempt to get channel id for location
		self.channel_id = None
		channel_found = False
		guild = gccfg.client.guilds[0]
		for channel in guild.channels:
			if channel_found == False:  
				if type(channel) == discord.TextChannel:
					if channel.name == self.id:
						self.channel_id = channel.id
						channel_found = True

		self.print_missing_data()

	def is_alias(self, alias):
		if alias in self.names:
			return True
		else:
			return False 

	
	def print_missing_data(self):
		#print info about missing data incase something is missing from location_cfg.json
		if (self.names == None):
			print(f"{self.id} location has no alias names")
		if (self.full_name == None):
			print(f"{self.id} location has no full name")
		if (self.look_txt == None):
			print(f"{self.id} location has no look text")
		if (self.channel_id == None):
			print(f"there is no #{self.id} channel")
			
			
class GCFisher:
	fishing = False
	bite = False
	fishing_id = 0
	prompts = 0
	reward = 0
	
	def stop(self): 
		self.fishing = False
		self.bite = False
		self.fishing_id = 0
		self.prompts = 0
		self.reward = 0

class GCSpell:
	# Create the spell object
	def __init__(
			self,
			name = "",
			json_entry = None,
			aliases = [],
			type = "",
			power = 0,
			cost = 0,
			users = []
	):
		if json_entry:
			self.name = name
			self.aliases = json_entry.get("aliases")
			self.aliases.append(self.name)
			self.aliases.append(self.name.lower())
			self.type = json_entry.get("type")
			self.power = json_entry.get("power")
			self.cost = json_entry.get("cost")
			self.users = json_entry.get("users")
		else:
			self.name = name
			self.aliases = aliases
			self.type = type
			self.power = power
			self.cost = cost
			self.users = users

	# Returns a unique instance
	def new_copy(self):
		return (GCSpell(
			name = self.name,
			type = self.type,
			power = self.power,
			cost = self.cost,
			users = self.users
		))

class GCItem:
	# Set default values
	def __init__(
			self,
			name = "",
			id = 0,
			ownerid = 0,
			itemtype = '',
			adorner = 0,
			equipper = 0,
			level = 1,
			xp = 0,
			known_spells = []
		

	):
		SavedData = gcdb.getItemData(id)
		if SavedData:
			self.id = id
			self.name = SavedData['name']
			self.ownerid = SavedData['ownerid']
			self.itemtype = SavedData['itemtype']
			self.adorner = SavedData['adorner']
			self.equipper = SavedData['equipper']
			self.level = SavedData["level"]
			self.xp = SavedData["xp"]
			self.known_spells = SavedData["known_spells"]
			
		else:
			self.id = id
			self.name = name
			self.ownerid = ownerid
			self.itemtype = itemtype
			self.adorner = adorner
			self.equipper = equipper
			self.level = level
			self.xp = xp
			self.known_spells = known_spells
			gcdb.createItem(self)
	def persist(self):
		# Grab existing data
		SavedData = gcdb.getItemData(self.id)

		# Iterate through all saved values
		for key in SavedData:
			if key != 'id' and SavedData[key] != getattr(self, key):
				# Only Bother with changed values
				gcdb.setItemAttribute(self.id, key, getattr(self, key))

class GCSportsTeam:
	# Set default values
	def __init__(
			self,
			id = 0,
			name = "",
			emoji = "",
			wins = 0,
			losses = 0,
			pizzaz = 0
	):
		SavedData = gcdb.getTeamData(id)
		if SavedData:
			self.id = id
			self.name = SavedData["name"]
			self.emoji = SavedData["emoji"]
			self.wins = SavedData["wins"]
			self.losses = SavedData["losses"]
			self.pizzaz = SavedData["pizzaz"]
		else:
			self.id = id
			self.name = name
			self.emoji = emoji
			self.wins = wins
			self.losses = losses
			self.pizzaz = pizzaz
			gcdb.createTeamEntry(self)

	""" Save new data to the database """
	def persist(self):
		# Grab existing data
		SavedData = gcdb.getTeamData(self.id)

		# Iterate through all saved values
		for key in SavedData:
			if key != 'id' and SavedData[key] != getattr(self, key):
				# Only Bother with changed values
				gcdb.setTeamAttribute(self.id, key, getattr(self, key))

class GCSportsPlayer:
	# Set default values
	def __init__(
			self,
			id = 0,
			teamid = 0,
			name = "",
			wins = 0,
			losses = 0,
			power = 0,
			determination = 0,
			spirit = 0,
			chill = 0,
			goonery = 0,
			cringe = 0
	):
		SavedData = gcdb.getSPlayerData(id)
		if SavedData:
			self.id = id
			self.teamid = SavedData["teamid"]
			self.name = SavedData["name"]
			self.wins = SavedData["wins"]
			self.losses = SavedData["losses"]
			self.power = SavedData["power"]
			self.determination = SavedData['determination']
			self.spirit = SavedData['spirit']
			self.chill = SavedData['chill']
			self.goonery = SavedData['goonery']
			self.cringe = SavedData['cringe']
		else:
			self.id = id
			self.teamid = teamid
			self.name = name
			self.wins = wins
			self.losses = losses
			self.power = power
			self.determination = determination
			self.spirit = spirit
			self.chill = chill
			self.goonery = goonery
			self.cringe = cringe
			gcdb.createSPlayerEntry(self)

	""" Save new data to the database """
	def persist(self):
		# Grab existing data
		SavedData = gcdb.getSPlayerData(self.id)

		# Iterate through all saved values
		for key in SavedData:
			if key != 'id' and SavedData[key] != getattr(self, key):
				# Only Bother with changed values
				gcdb.setSPlayerAttribute(self.id, key, getattr(self, key))


class GCFish:
	# Create the spell object
	def __init__(
			self,
			name = "",
			json_entry = None,
			rarity = "",
			price = 0,
			description = "",
	):
		if json_entry:
			self.name = name
			self.rarity = json_entry.get("rarity")
			self.price = json_entry.get("price")
			self.description = json_entry.get("description")
		else:
			self.name = name
			self.rarity = rarity
			self.price = price
			self.description = description

class GCMisc:
	# Create the spell object
	def __init__(
			self,
			name = "",
			json_entry = None,
			type = "",
			price = 0,
			description = "",
	):
		if json_entry:
			self.name = name
			self.type = json_entry.get("type")
			self.price = json_entry.get("price")
			self.description = json_entry.get("description")
		else:
			self.name = name
			self.type = type
			self.price = price
			self.description = description
			
class GCCosmetic:
	def __init__(
		self,
		name = "",
		json_entry = None,
		type = "",
		price = 0,
		description = "",
		style = "",
		fashion = "",
		adorntxt = "",
	):
		if json_entry:
			self.name = name
			self.type = json_entry.get("type")
			self.price = json_entry.get("price")
			self.description = json_entry.get("description")
			self.price = json_entry.get("price")
			self.description = json_entry.get("description")
			self.style = json_entry.get("style")
			self.fashoin = json_entry.get("fashion")
			self.adorntxt = json_entry.get("adorntxt")
		else:
			self.name = name
			self.type = type
			self.price = price
			self.type = type
			self.price = price
			self.description = description
			self.style = style
			self.fashion = fashion
			self.adorntxt = adorntxt
	
