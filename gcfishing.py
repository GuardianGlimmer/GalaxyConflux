import gccfg
import gcdb
import random
import discord
import asyncio
from gcclasses import GCPlayer
from gcclasses import GCFisher
from gcclasses import GCItem

funnything = True
fishers = {}
legendaryFish = ["Shy Frog", "Strawberry Squid"]
RareFish = ["Northeastern Stingray"]
UncommonFish = ["Bubble Fish"]
CommonFish = ["Glittering Fish", "Sweet Shrimp"]


def generate_fish(author_id):
	id = 0
	rarity = random.randrange(1, 100)
	if rarity >= 99:
		Choice = legendaryFish
	elif rarity >= 80:
		Choice = RareFish
	elif rarity >= 70:
		Choice = UncommonFish
	else:
		Choice = CommonFish
	selection = random.choice(Choice)
	while gcdb.getItemData(id):
			id += 1
	spawned = generate_item(author_id, selection, "fish")
	name = spawned
	return name

def generate_item(owner, name, itemtype1):
	id = 0
	while gcdb.getItemData(id):
		id += 1
	spawned = GCItem(
		id = id,
		name = name,
		ownerid = owner,
		itemtype = itemtype1,
		adorner = 0,
		equipper = 0,
		level = 1,
		xp = 0,
		known_spells = []
		
			)
	return spawned.name