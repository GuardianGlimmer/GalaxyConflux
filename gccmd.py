import gccfg
import gcdb
import random
import discord
import asyncio
from gcclasses import GCPlayer, GCFisher
import gcclasses

from gcutility import sent_message, update_member_role

funnything = True
fishers = {}
fishingresponses = ["you wiggle your legs as they hang off the boardwalk. what a lovely time", "You watch the hot dog vendor give away a free hot dog. how kind!", "you see a little girl carrying around a teddybear larger than her!"]
GCplayers = gcdb.GCplayers

# Define commands
'''
    Adds 1 to lofi when sent in the study channel
'''
async def study_cmd(msg):
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
	response = "You are {} % hungry.".format(player.hunger)
	await sent_message(msg, response)
'''
    Shows user what is for sale at the cafe
'''
async def menu_cmd(msg):
    if msg.channel.id == gccfg.location_map.get("mall").channel_id:
        response = "The man at the counter glares at you. He is wearing a chef's hat and his hands are shaking violently as he drinks from a teacup, full to the brim.\n" + "strawberry cupcake: 5 money.\n" + "strawberry: 1 money.\n" + "cupcake: 3 money\n"
        await sent_message(msg, response)
    #TODO: add a response when players are in the wrong channel

''' 
    Buys food for user if they have the funds
'''
async def order_cmd(msg):
    # Setup Necessary Variables
    foodNames = ["strawberry cupcake", "strawberry", "cupcake"]  # the food items. Their order matches with their prices and responses in the other lists. Same indexes.
    prices = [15, 10, 5]  # Food/Prices/Descriptions should be defined at the base of a file, defining each time something runs is a little slow
    foodResponses = ["You recieve a pink cupcake. You're thinking that the fact its strawberry just because its pink is offensive to you until you bite down and discover the TRUE strawberry at the core, hidden. The strawberry is frozen for some reason and is making the cupcake soggy.", "Its a strawberry. You insert it into the inside of your mouth -where you eat it. Yum!",
                     "Its a brown cupcake. Tastes pretty good but its on the dry side. It could use some strawberries."]
	foodValues = [25, 15, 5]
    order = msg.content.split(' ', 1)[1] # splits the text into a list of two strings at the first " "

    # Ensure food exists
    if order in foodNames:
        # Check price
        cost = prices[foodNames.index(order)]  # matchin up the values via index.
		filling = foodValues[foodNames.index(order)]
        wallet = gcdb.getPlayerAttribute(msg.author.id, 'money')
		stomach = gcdb.setPlayerAttribute(msg.author.id, 'hunger')
        if wallet - cost >= 0:
            # Subtract cost and send response if they can afford it
            gcdb.setPlayerAttribute(msg.author.id, 'money', wallet - cost)
			if stomach - filling <= 0:
				gcdb.setPlayerAttribute(msg.author.id, 'hunger', 0)
			else:
				gcdb.setPlayerAttribute(msg.author.id, 'hunger', stomach - filling)
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
        response = "i dont know that location!"
        await sent_message(msg, response)

    # player already in location
    elif found_location.id == player.location:
        response = "You are already here"
        await sent_message(msg, response)

    # vaild desired location
    else:
        # Tell them they're moving
        response = 'You begin walking to ' + found_location.full_name + ". it will take 5 seconds"
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
    if msg.channel.id == gccfg.location_map.get("mall").channel_id:
        player = GCPlayer(msg.author.id)

        # make a random amount of money beween 1 and 5
        pay = random.randrange(1, 5)

        # add pay to player's money total
        player.money += pay
        player.persist()

        response = "you work long and hard at the mall to earn some cash. you made " + str(pay) + " cash!"
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
        response = "you focus REALLY hard, and feel a breeze whip around you! ... but nothing really happened... so close..."
    elif currentLofi >= 10000:
        response = "you spin in place, really believing this time it will work!!! \n you fall over into your chair, having only **transformed** your hair into a big mess"
    elif currentLofi >= 1000:
        response = "you clasp your hands and look up to the sky, the moon reflected in your big eyes. you feel tingly!!! \n .... its just because you have been sitting too long..."
    elif currentLofi >= 100:
        response = "you grab your pen and poirouette around the room! you jump off your bed ready to take flight and- \n you fall onto the conveniently placed beanbag. nope, cant fly yet."
    else:
        response = "you spin around your room, your beautiful Guardian Garb flowing around you, those bad guys better watch out!!! \n... ok time to stop playing pretend and get out of this cheap cosplay gear."

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
		response = "sorry, but you cant fish here! try going to the boardwalk."
	else:
		player = GCPlayer(msg.author.id)
		if msg.author.id not in fishers.keys():
			fishers[msg.author.id] = GCFisher()
		fisher = fishers[msg.author.id]
		if fisher.fishing == True:
			response = "You are already fishing."
			await sent_message(msg, response)
		if gcdb.setPlayerAttribute(msg.author.id, 'hunger') >= 100:
			response = "You are too hungry to fish right now."
			await sent_message(msg, response)
		else:
			stomach = gcdb.setPlayerAttribute(msg.author.id, 'hunger')
			gcdb.setPlayerAttribute(msg.author.id, 'hunger', stomach + 15)
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
					response = "you feel a pull on your line! **~REEL NOW!**"
					await sent_message(msg, response)
					await asyncio.sleep(5)
					
					if fisher.bite != False:
						response = "The fish got away...\nBut you still got " + str(fisher.reward / 2) + " Lofi!"
						await sent_message(msg, response)
						player.lofi += int(fisher.reward / 2)
						fisher.stop()
						player.persist()
						break
					else:
						response = "you reel in a cute little fish, carefully unhooking it and healing its wounds with your magic before throwing it back. \nYou gained " + str(fisher.reward + 50) + " Lofi!"
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
		response = "Sorry, but you cant fish here! try going to the boardwalk."
		await sent_message(msg, response)
	elif fisher.bite != True:
		response = "You havn't caught anything yet..."
		await sent_message(msg, response)
	else:
		fisher.bite = False
		response = "You grip your rod and pull with all your might!"
		await sent_message(msg, response)
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
