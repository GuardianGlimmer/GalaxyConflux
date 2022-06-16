import gccfg
import gcdb
import random
import discord
import asyncio
from gcclasses import GCItem, GCPlayer, GCFisher, GCEnemy, GCSportsTeam, GCSportsPlayer
import gcfighting
import gccfg
import shlex

def genname():
	with open ('firstnames.txt', 'r') as f:
		lines = f.readlines()
		firstname = random.choice(lines)[:-1]
	with open("lastnames.txt", 'r') as f:
		lasts = f.readlines()
		lastname = random.choice(lasts)[:-1]
	name = firstname + " " + lastname
	print(name)
	return name

def spawnsplayer(teamid): 
	id = 0
	print(str(id))
	while gcdb.getSPlayerData(id):
		id += 1
		print(id)
	spawned = GCSportsPlayer(
					id = id,
					teamid = teamid,
					name = str(genname()),
					wins = 0,
					losses = 0,
					power = int(random.randrange(0, 10)),
					determination = int(random.randrange(0, 10)),
					spirit = int(random.randrange(0, 10)),
					chill = int(random.randrange(0, 10)),
					goonery = int(random.randrange(0, 10)),
					cringe = int(random.randrange(0, 10))
			)
		
	response = "Spawned " + str(spawned.name) + " with id " + str(spawned.id) + " and teamid " + str(spawned.teamid)
	print(response)


def spawn_team(name, emoji):
		id = 0
		while gcdb.getTeamData(id):
			id += 1
		spawned = GCSportsTeam(
			id = id,
			name = str(name),
			emoji = str(emoji),
			wins = 0,
			losses = 0,
			pizzaz = int(random.randrange(0, 5))
		)
	
		response = "Spawned " + spawned.name + " with id " + str(spawned.id) + " and pizzaz " + str(spawned.pizzaz)
		print(response)

'''
spawn_team("Stillwater Smiles", "<:smiley:966455899516436621>")
spawn_team("Banff Bears", "<:bear:966456971689619527>")
spawn_team("Catalan Cacti", "<:cactus:966457555805147146>")
spawn_team("Charlotte Cybers", "<:mechanical_arm:966458085721915473>")
spawn_team("New Orleans Shrimp", "<:shrimp:966458890315247697>")
'''