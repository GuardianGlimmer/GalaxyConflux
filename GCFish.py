import gccfg
import gcdb
import random
import discord
import asyncio
from gcclasses import GCPlayer
from gcclasses import GCFisher

funnything = True
fishers = {}
'''
    Casts a line into the sea
'''
async def cast_cmd(msg):
    	if msg.channel.id != gccfg.location_map.get("the-boardwalk").channel_id:
      		response = "sorry, but you cant fish here! try going to the boardwalk."
    	else:
      		player = GCPlayer(msg.author.id)
      		if msg.message.author.id not in fishers.keys():
			fishers[cmd.message.author.id] = EWFisher()
		fisher = fishers[msg.message.author.id]
		prompts = random.randomrandint(1, 10)
      		reward = prompts * random.randint(10, 20)
      		while funnything = True:
        		if prompts > 0:
				await asyncio.sleep(10)
				response = random.choice("you wiggle your legs as they hang off the boardwalk. what a lovely time", "You watch the hot dog vendor give away a free hot dog. how kind!", "you see a little girl carrying around a teddbear larger than her!")
				await sent_message(msg, response)
				prompts -= 1
				  
        		else:
				fisher.bite = True
				response = "you feel a pull on your line! **~REEL NOW!**"
				awaut sent_message(msg, response)
				await asyncio.sleep(6)
			
			  	#missing a reel gives half the reward
          			if fisher.bite != False:
					response = "the fish got away... but you still got " + str(reward / 2) + " lofi!"
				    	player.lofi += (reward / 2)
				#getting a reel gets you the full reward + 50 bonus
          			else:
					response = "you reel in a cute little fish, carefully unhooking it and healing its wounds with your magic before throwing it back. \n you gained " + str(reward + 50) + "Lofi!"
   					player.lofi += (reward + 50)
 '''
    Lets users reel in fish
 '''
async def reel_cmd(msg):
	player = GCPlayer(msg.author.id)
      	if msg.message.author.id not in fishers.keys():
		fishers[cmd.message.author.id] = EWFisher()
	fisher = fishers[msg.message.author.id]
	if msg.channel.id != gccfg.location_map.get("the-boardwalk").channel_id:
      		response = "sorry, but you cant fish here! try going to the boardwalk."
	elif fisher.bite != True:
		response = "you havn't caught anything yet..."
		await sent_message(msg, response)
    	else:
		fisher.bite = False
		response = "you grip your rod and pull with all your might!"
		await sent_message(msg, response)