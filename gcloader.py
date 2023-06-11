import discord
import json
import os
import importlib
from pprint import pprint

from gcclasses import GCLocation
from gcclasses import GCSpell
from gcclasses import GCFish
from gcclasses import GCMisc
from gcclasses import GCCosmetic
from gcclasses import GCFood
from gcclasses import GCCasting
import gccfg


def generate_cmd_map():
	gccfg.cmd_map = {}

	# grab command json
	f = open(os.path.join('json_cfg', 'cmd_cfg.json'))
	cmd_json = json.load(f)
	f.close()

	for element in cmd_json:
		element = cmd_json[element]

		function_name = element["function"]

		#get command fucntion from gccmd unless cmd_cfg.json specifies a differernt module file
		module_name = element.get("module", "gccmd")

		# get command function
		temp = importlib.__import__(module_name, fromlist=[function_name])
		cmd_fn = getattr(temp, function_name)

		# bind command names and funtions to cmd_map
		for command_name in element["command_names"]:
			gccfg.cmd_map.update({gccfg.cmd_prefix + command_name: cmd_fn})

	#pprint(gccfg.cmd_map)


async def generate_channel_map():
	gccfg.location_map = {}
	guild = gccfg.client.guilds[0]

	# grab command json
	f = open(os.path.join('json_cfg', 'location_cfg.json'), encoding="utf8")
	location_json = json.load(f)
	f.close()

	# construct GCLocation objects and map to location id
	for location_id in location_json:
		location_obj = GCLocation(location_id,
		                          _json_entry=location_json[location_id])
		gccfg.location_map.update({location_id: location_obj})

	# quick and dirty add missing channel feature
	if (gccfg.construct_mising_channels == True):
		for location in gccfg.location_map:
			location = gccfg.location_map[location]
			if location.channel_id == None:
				channel = await guild.create_text_channel(location.id)
				print(f"created channel for {location.id}")
				location.channel_id = channel.id

	#pprint(gccfg.location_map)


async def generate_role_map():
	guild = gccfg.client.guilds[0]

	# map location ids to roles
	for location in gccfg.location_map:
		location = gccfg.location_map[location]

		role = discord.utils.get(guild.roles, name=location.role_name)

		if role != None:
			gccfg.role_map.update({location.id: role})
		else:
			#quick and dirty add missing roles feature
			if (gccfg.construct_mising_roles == True):
				role = await guild.create_role(name=location.role_name)
				gccfg.role_map.update({location.id: role})
				print(f"created role {role.name}")

	# get other roles
	for role_name in ["School Girl"]:
		role = discord.utils.get(guild.roles, name=role_name)

		if role != None:
			gccfg.role_map.update({role_name: role})
		else:
			#quick and dirty add missing roles feature
			if (gccfg.construct_mising_roles == True):
				role = await guild.create_role(name=role_name)
				gccfg.role_map.update({role_name: role})
				print(f"created role {role.name}")

	#print(gccfg.role_map)


def generate_spell_map():
	gccfg.spell_map = {}

	# grab spell json
	f = open(os.path.join('json_cfg', 'spell_cfg.json'), encoding="utf8")
	spells_json = json.load(f)
	f.close()

	# construct GCLocation objects and map to location id
	for spell_name in spells_json:
		spell_obj = GCSpell(spell_name, json_entry=spells_json[spell_name])
		gccfg.spells.append(spell_obj)
		for alias in spell_obj.aliases:
			gccfg.spell_map.update({alias: spell_obj})


def generate_fish_map():
	gccfg.fish_map = {}

	f = open(os.path.join('json_cfg', 'fish_cfg.json'), encoding='utf8')
	fish_json = json.load(f)
	f.close()

	for fish_id in fish_json:
		fish_obj = GCFish(fish_id, json_entry=fish_json[fish_id])
		gccfg.fish_map.update({fish_id: fish_obj})


def generate_misc_map():
	gccfg.misc_map = {}

	f = open(os.path.join('json_cfg', 'miscitem_cfg.json'), encoding='utf8')
	misc_json = json.load(f)
	f.close()

	for misc_id in misc_json:
		misc_obj = GCMisc(misc_id, json_entry=misc_json[misc_id])
		gccfg.misc_map.update({misc_id: misc_obj})


def generate_cosmetic_map():
	gccfg.cosmetic_map = {}

	f = open(os.path.join('json_cfg', 'cosmetics_cfg.json'), encoding='utf8')
	cosmetic_json = json.load(f)
	f.close()

	for cosmetic_id in cosmetic_json:
		cosmetic_obj = GCCosmetic(cosmetic_id, json_entry=cosmetic_json[cosmetic_id])
		gccfg.cosmetic_map.update({cosmetic_id: cosmetic_obj})


def generate_food_map():
	gccfg.food_map = {}

	f = open(os.path.join('json_cfg', 'food_cfg.json'), encoding='utf8')
	food_json = json.load(f)
	f.close()

	for food_id in food_json:
		food_obj = GCFood(food_id, json_entry=food_json[food_id])
		gccfg.food_map.update({food_id: food_obj})


def generate_casting_map():
	gccfg.casting_map = {}

	f = open(os.path.join('json_cfg', 'casting_cfg.json'), encoding='utf8')
	casting_json = json.load(f)
	f.close()

	for casting_id in casting_json:
		casting_obj = GCCasting(casting_id, json_entry=casting_json[casting_id])
		gccfg.casting_map.update({casting_id: casting_obj})
	print(gccfg.casting_map)