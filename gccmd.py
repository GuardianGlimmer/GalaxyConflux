import gccfg
import gcdb
import random
import discord
import asyncio
from gcclasses import GCPlayer, GCFisher, GCEnemy
import gcclasses
import gcfighting
import gccfg
import shlex

from gcutility import sent_message, update_member_role

funnything = True
fishers = {}
fishingresponses = ["You wiggle your legs as they hang off the boardwalk. What a lovely time.", "You watch the hot dog vendor give away a free hot dog. How kind!", "You see a little girl carrying around a teddybear larger than her!", "You breifly stare at the sky, one of the clouds looks like a bunny! Cute.", "A gentle ocean breeze swirls by, bringing the light salty smell of the ocean with it.", "Peering into the horizon you see somebody kayak by.", "The smell of kettlecorn and cotton candy stands wafts from the boardwalk.", "You can hear the faint beep and boops from the boardwalks arcade.", "You see a boy contemplating and skipping rocks.", "You start thinking about stocks... Wait why are you thinking about that? That's grownup stuff.", "You think about numbers going down. What? Why would they do that?"]
GCplayers = gcdb.GCplayers

# Define commands
'''
	Adds 1 to lofi when sent in the study channel
'''
async def study_cmd(msg):
	'''
	response = "What are you doing studying? Schools out for the summer!"
	await sent_message(msg, response)
	'''
	#check if player is in proper channel
	if msg.channel.id == gccfg.location_map.get("study-hall").channel_id:
		#add 1 lofi
		player = GCPlayer(msg.author.id)
		player.lofi += 1
		player.persist()
	#TODO: add a response when players are in the wrong channel

'''
	Shows user their current lofi
'''
async def lofi_cmd(msg):
	player = GCPlayer(msg.author.id)
	response = "You have {} lofi.".format(player.lofi)
	await sent_message(msg, response)

'''
	Shows user their current money
'''
async def money_cmd(msg):
	player = GCPlayer(msg.author.id)
	response = "You have {} currency.".format(player.money)
	await sent_message(msg, response)

'''
	Shows user their current hunger
'''
async def hunger_cmd(msg):
	player = GCPlayer(msg.author.id)
	response = "You are {}% hungry.".format(player.hunger)
	print(player.hunger)
	await sent_message(msg, response)
	print("hungerlol")
'''
	Shows user what is for sale at the cafe
'''
async def menu_cmd(msg):
	if msg.channel.id == gccfg.location_map.get("moonlight-cafe").channel_id:
		response = "The man at the counter glares at you. He is wearing a chef's hat and his hands are shaking violently as he drinks from a teacup, full to the brim.\n" + "strawberry cupcake: 15 money.\n" + "blueberry: 5 money.\n" + "cupcake: 10 money\n"
		await sent_message(msg, response)
	#TODO: add a response when players are in the wrong channel

''' 
	Buys food for user if they have the funds
'''
async def order_cmd(msg):
	# Setup Necessary Variables
	player = GCPlayer(msg.author.id)
	foodNames = ["strawberry cupcake", "blueberry", "cupcake"]  # the food items. Their order matches with their prices and responses in the other lists. Same indexes.
	prices = [15, 5, 10]  # Food/Prices/Descriptions should be defined at the base of a file, defining each time something runs is a little slow
	foodResponses = ["You recieve a pink cupcake. You're thinking that the fact its strawberry just because it's pink is offensive to you until you bite down and discover the TRUE strawberry at the core, hidden. The strawberry is frozen for some reason and is making the cupcake soggy.", "It's a blueberry. You insert it into the inside of your mouth -where you eat it. Yum!",
					 "It is a brown cupcake. Tastes pretty good but it's on the dry side. It could use some strawberries."]
	foodValues = [25, 10, 15]
	order = msg.content.split(' ', 1)[1] # splits the text into a list of two strings at the first " "

	# Ensure food exists
	if order in foodNames:
		# Check price
		cost = prices[foodNames.index(order)]  # matchin up the values via index.
		filling = foodValues[foodNames.index(order)]
		wallet = gcdb.getPlayerAttribute(msg.author.id, 'money')
		stomach = gcdb.getPlayerAttribute(msg.author.id, 'hunger')
		if wallet - cost >= 0:
			# Subtract cost and send response if they can afford it
			player.money= (wallet - cost)
			if stomach - filling <= 0:
				player.hunger = 0
				player.persist()
				response = foodResponses[foodNames.index(order)]
				await sent_message(msg, response)
			else:
				player.hunger = (stomach - filling)
				player.persist()
				response = foodResponses[foodNames.index(order)]
				await sent_message(msg, response)
		else:
			# Tell them if they're a broke ass bitch
			response = "Now just how do you plan to pay for that? You only gave me {} money!".format(wallet)
			await sent_message(msg, response)
	else:
		# Tell them the food doesn't exist
		response = "Whats that supposed to be? Go bake it yourself, kid!"
		await sent_message(msg, response)

'''
	Moves the user to target location
'''
async def goto_cmd(msg):
	# Setup necessary variables
	member = msg.author #The user
	player = GCPlayer(msg.author.id)
	desired_location = msg.content.split(' ', 1)[1] #the input with the command removed. Hopefully only the location name

	# check if desired location is a real location
	found_location = None
	for location in gccfg.location_map:
		location = gccfg.location_map[location]
		if location.is_alias(desired_location):
			found_location = location

	
	# location not found
	if found_location == None:
		response = "I dont know that location!"
		await sent_message(msg, response)

	# player already in location
	elif found_location.id == player.location:
		response = "You are already here."
		await sent_message(msg, response)

	# vaild desired location
	else:
		# Tell them they're moving
		response = 'You begin walking to ' + found_location.full_name + ". It will take 5 seconds."
		await sent_message(msg, response)

		#wait 5 seconds
		await asyncio.sleep(5)

		# change database location
		player = GCPlayer(msg.author.id)
		player.location =  found_location.id
		player.persist()

		# update member roles
		await update_member_role(member)


'''
	Allows people to look where they are
'''
async def look_cmd(msg):
	response = None

	#get player location
	player = GCPlayer(msg.author.id)
	current_location = gccfg.location_map.get(player.location)

	if (current_location != None):
		response = current_location.look_txt
	else:
		response = "You are sitting in front of your parents' PC. There's a cup with some hot brew you made that you can't recall if it was tea or coffee, but it's gotten cold so who cares. You have bags under your eyes. You've been looking at this PC for way too long."
	await sent_message(msg, response)
	
'''
	Pays user per command, if done in mall
'''
async def work_cmd(msg):
	if msg.channel.id == gccfg.location_map.get("the-mall").channel_id:
		player = GCPlayer(msg.author.id)

		# make a random amount of money beween 1 and 5
		pay = random.randrange(1, 5)

		# add pay to player's money total
		player.money += pay
		player.persist() 

		response = "You work long and hard at the mall to earn some cash. You made " + str(pay) + " cash!"
		await sent_message(msg, response)
	
	#TODO: add a response when players are in the wrong channel

'''
	Allows the user to see their transformation into a magical girl
'''
async def transform_cmd(msg): #In the future I'll turn it into a tag, for now it is just hard to unlock flavor text
	
	player = GCPlayer(msg.author.id)
	currentLofi = player.lofi
	
	if currentLofi >= 1000000:
		response = "Epic orchestral music starts to sound. You summon the power of friendship and love and scream your magical girl name with all your soul. Your regular student clothes begin to disappear to reveal a super cute outfit without ever showing anything NSFW to the camera. People around you are hypnotized by this transformation, you notice that thanks to the 'Damns' and 'Holy fucks' they let out. You are a magical girl now, go kick some bad guy's ass!"  
	elif currentLofi >= 100000:
		response = "You focus REALLY hard, and feel a breeze whip around you! ... but nothing really happened... so close..."
	elif currentLofi >= 10000:
		response = "You spin in place, really believing this time it will work!!! \n You fall over into your chair, having only **transformed** your hair into a big mess."
	elif currentLofi >= 1000:
		response = "You clasp your hands and look up to the sky, the moon reflected in your big eyes. You feel tingly!!! \n .... It's just because you have been sitting too long..."
	elif currentLofi >= 100:
		response = "You grab your pen and poirouette around the room! You jump off your bed ready to take flight and- \n you fall onto the conveniently placed beanbag. Nope, can't fly yet."
	else:
		response = "You spin around your room, your beautiful Guardian Garb flowing around you, those bad guys better watch out!!! \n... Ok time to stop playing pretend and get out of this cheap cosplay gear."

	await sent_message(msg, response)

'''
	Return the entire database as text for debugging
'''
async def db_cmd(msg):
	response = str(GCplayers.all())
	await sent_message(msg, response)

	
'''
	Returns all location names
'''
async def map_cmd(msg):
	#TODO: generate list from location_map
	response = "mall, study hall, cafe, downtown, boardwalk"
	await sent_message(msg, response)

'''
	Casts a line into the sea
'''
async def cast_cmd(msg):
	if msg.channel.id != gccfg.location_map.get("the-boardwalk").channel_id:
		response = "Sorry, but you cant fish here! Try going to the boardwalk."
	else:
		player = GCPlayer(msg.author.id)
		stomach = gcdb.getPlayerAttribute(msg.author.id, 'hunger')
		if msg.author.id not in fishers.keys():
			fishers[msg.author.id] = GCFisher()
		fisher = fishers[msg.author.id]
		if fisher.fishing == True:
			response = "You are already fishing."
			await sent_message(msg, response)
		elif stomach >= 100:
			response = "You are too hungry to fish right now."
			await sent_message(msg, response)
		else:
			player.hunger = stomach + 10
			print(gcdb.getPlayerAttribute(msg.author.id, 'hunger'))
			player.persist()
			fisher.fishing = True
			fisher.prompts = random.randrange(1, 10)
			fisher.reward = fisher.prompts * random.randrange(10, 20)
			response = "You take one of the free fishing lines and cast it out into the gentle waves."
			await sent_message(msg, response)
			await asyncio.sleep(15)
			
			while funnything is True:
				if fisher.prompts > 0:
					response = random.choice(fishingresponses)
					await sent_message(msg, response)
					fisher.prompts -= 1
					await asyncio.sleep(15)
					continue
				else:
					fisher.bite = True
					response = "You feel a pull on your line! **~REEL NOW!**"
					await sent_message(msg, response)
					await asyncio.sleep(5)
					
					if fisher.bite != False:
						response = "The fish got away...\nBut you still got " + str(int(fisher.reward / 2)) + " Lofi!"
						await sent_message(msg, response)
						player.lofi += int(fisher.reward / 2)
						fisher.stop()
						player.persist()
						break
					else:
						response = "You reel in a cute little fish, carefully unhooking it and healing its wounds with your magic before throwing it back. \nYou gained " + str(fisher.reward + 50) + " Lofi!"
						await sent_message(msg, response)
						player.lofi += int(fisher.reward + 50)
						fisher.stop()
						player.persist()
						break
				
'''
	Lets users reel in fish
'''
async def reel_cmd(msg):
	player = GCPlayer(msg.author.id)
	if msg.author.id not in fishers.keys():
		fishers[msg.author.id] = GCFisher()
	fisher = fishers[msg.author.id]
	if msg.channel.id != gccfg.location_map.get("the-boardwalk").channel_id:
		response = "Sorry, but you cant fish here! Try going to the boardwalk."
		await sent_message(msg, response)
	elif fisher.bite != True:
		response = "You havn't caught anything yet..."
		await sent_message(msg, response)
	else:
		fisher.bite = False
		response = "You grip your rod and pull with all your might!"
		await sent_message(msg, response)

		'''
	Spawn an enemy
'''
async def spawn_enemy(msg):
	id = 0
	while gcdb.getEnemyData(id):
		id += 1
	spawned = GCEnemy(
		id = id,
		name = "generic",
		location = "downtown",
		size = random.randrange(1,5)
	)

	response = "Spawned " + spawned.name + " with id " + str(spawned.id) + " and " + str(spawned.attacks) + " for attacks."
	await msg.channel.send('*' + str(msg.author.display_name) + ':* ' + response)

'''
	Return enemies in user's current district
'''
async def lookout_cmd(msg):
	user_data = GCPlayer(userid = msg.author.id)
	enemies = gcdb.findEnemies("location", user_data.location)

	response = "In " + user_data.location + " you see: \n"
	if enemies:
		for enemy_data in enemies:
			response += "\nA size {} {}. ID: {}".format(str(enemy_data["size"]), enemy_data["name"], enemy_data["id"])

	await msg.channel.send('*' + str(msg.author.display_name) + ':* ' + response)

'''
	Initiate combat sequence
'''
async def fight(msg):
	target_id = int(msg.content.split(' ', 1)[1])
	enemy_data = gcdb.getEnemyData(target_id)

	response = ""
	if enemy_data:
		enemy = GCEnemy(id = target_id)
		player = GCPlayer(userid = msg.author.id)
		if enemy.location != player.location:
			response = "That enemy is not present here."
		else:
			await gcfighting.initiate_combat(enemy, player, msg)
			return
	else:
		response = "No enemy with id {} exists".format(target_id)

	await msg.channel.send('*' + str(msg.author.display_name) + ':* ' + response)

'''
	Fill in with whatever to test certain functionality
'''
async def test(msg):
	player = GCPlayer(userid = msg.author.id)
	player.lofi -= 1
	player.money += 1
	player.persist()

'''
	List all spells available for players to learn
'''
async def list_spells(msg):
	# compile all user usable spell names
	player_spell_names = []
	for spell in gccfg.spells:
		if gccfg.spell_user_player in spell.users:
			player_spell_names.append(spell.name)

	# Build and send response
	response = "Currently learnable spells are: \n"
	for name in player_spell_names:
		response += "\n" + name

	await msg.channel.send('*' + str(msg.author.display_name) + ':* ' + response)

'''
	List all spells known by player
'''
async def known_spells(msg):
	# compile all user usable spell names
	player = GCPlayer(userid = msg.author.id)
	player_spells = []
	for spell_name in player.known_spells:
		if spell_name in gccfg.spell_map:
			player_spells.append(gccfg.spell_map[spell_name])

	# Build and send response
	response = "Currently known spells are: \n"
	for spell in player_spells:
		response += "\nName: {} | Cost: {}".format(spell.name, spell.cost)

	await msg.channel.send('*' + str(msg.author.display_name) + ':* ' + response)

'''
	add spell to player's known spells
'''
async def learn_spell(msg):
	target_spell_name = msg.content.split(' ', 1)[1]

	if target_spell_name in gccfg.spell_map:
		spell = gccfg.spell_map[target_spell_name]
		player = GCPlayer(userid = msg.author.id)
		player.known_spells.append(spell.name)
		player.persist()
		response = "You have successfully learned {}".format(spell.name)
	else:
		response = "{} isn't a real spell dummy. Try {}{}".format(target_spell_name, gccfg.cmd_prefix, "listspells")

	await msg.channel.send('*{}:* {}'.format(msg.author.display_name, response))

'''
	Queue a spell for the current fight is user is in one and can queue
'''
async def queue_spell(msg):
	# Parse target spell and get player
	target_spell_name = shlex.split(msg.content)[1]
	player = GCPlayer(userid = msg.author.id)

	# Ensure spell exists and is known
	if (target_spell_name in gccfg.spell_map and gccfg.spell_map[target_spell_name].name in player.known_spells):
		spell = gccfg.spell_map[target_spell_name].new_copy()
		# Check for fight and ensure player participation
		if player.location in gccfg.fights:
			fight = gccfg.fights[player.location]
			if player.userid in fight.player_ids:
				# TODO - add point system
				if player.lofi > spell.cost:
					if spell.cost <= fight.pts_remaining[player.userid]:
						response = ""

						# Parse target for targeted spells
						if spell.type == gccfg.spell_type_heal_target:
							mentions = msg.mentions
							if len(mentions) == 1:
								spell.target_id = mentions[0].id
								if spell.target_id not in fight.player_ids:
									response = "The target must be fighting with you!"
							if len(mentions) < 1:
								response = "You need to mention a target!"
							if len(mentions) > 1:
								response = "This spell can only target one player"

						if response != "":
							await msg.channel.send('*{}:* {}'.format(msg.author.display_name, response))
							return

						player.lofi -= int(spell.cost)
						fight.pts_remaining[player.userid] -= int(spell.cost)
						fight.player_queue.append(spell)

						# Build list of enemy names for flavortext
						enemy_names = ""
						enemy_number = 0
						for enemy_id in fight.enemy_ids:
							enemy_number += 1
							enemy = GCEnemy(id = enemy_id)
							if enemy_number > 1 and enemy_number == len(fight.enemy_ids):
								enemy_names += ", and {} id: {}".format(enemy.name, enemy.id)
							elif enemy_number > 1:
								enemy_names += ", {} id: {}".format(enemy.name, enemy.id)
							else:
								enemy_names += "{} id: {}".format(enemy.name, enemy.id)

						response = "Successfully queued {} against {} for {} lofi".format(spell.name, enemy_names, spell.cost)

						player.persist()
					else:
						response = "You only have {} points remaining! that spell costs {}.".format(fight.pts_remaining[player.userid], spell.cost)
				else:
					response = "You only have {} lofi! You need {} to queue that.".format(player.lofi, spell.cost)
			else:
				response = "You are not participating in the present fight."
		else:
			response = "There are no fights to attack for here."
	else:
		response = "You don't know that spell."

	await msg.channel.send('*{}:* {}'.format(msg.author.display_name, response))