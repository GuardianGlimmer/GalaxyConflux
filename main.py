import os
import discord
import gccfg
import gcloader
from gcutility import sent_message
from GCSports import genname, spawnsplayer

client = gccfg.client

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    #load config jsons and get discord channels and roles
    gcloader.generate_cmd_map()
    gcloader.generate_spell_map()
    gcloader.generate_fish_map()
    gcloader.generate_misc_map()
    gcloader.generate_cosmetic_map()
    await gcloader.generate_channel_map()
    await gcloader.generate_role_map()

@client.event
async def on_message(message):

    # do not respond to self messages
    if message.author == client.user:
        return

    #message.content = message.content.lower()
    # respond command messages
    if message.content.startswith(gccfg.cmd_prefix):
        # get first word (the command name)
        term = (message.content.split(" ")[0]).lower()

        # get command fucntion from command map
        cmd_fn = gccfg.cmd_map.get(term)
        if cmd_fn != None:
          await cmd_fn(message)
'''
        else:
            response = "I'm not sure I understood that... So sorry!"
            await sent_message(msg, response)
            pass
'''

# read token file
#f = open("token")
#token = f.readline().strip()

# connect to discord

client.run('OTA2NzMyMzg3MDEzMDk5NTUy.GUe0Yb.v_6CjqyI4A9U_n5J-tTXYx2-yEZr5cECzjMZyY')
