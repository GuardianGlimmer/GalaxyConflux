import discord
import gccmd

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    message.content = message.content.lower()

    if message.content.startswith(gccmd.cmd_prfx):
        message.content = message.content.replace(gccmd.cmd_prfx, '', 1)
        term = message.content.split(" ")[0]

        if term in gccmd.cmd_dict:
            await gccmd.cmd_dict[term](message)

#Add token
client.run('')

