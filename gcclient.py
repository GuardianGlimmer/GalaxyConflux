import discord
import gccmd
import gcdb
from tinydb import TinyDB
from discord.utils import get
import random

#sets up the database
GCplayers = TinyDB("./GCplayers.json")

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    message.content = message.content.lower()
    if message.content.startswith(gccmd.cmd_prfx + 'register'):
        if gcdb.getPlayerAttribute(message.author.id, 'id'):
            await message.channel.send('*' + str(message.author.displayname) + ':*' + ' you already registered')
        else:
            gcdb.createEntry(message.author.id)
            await message.channel.send('*' + str(message.author.display_name) + ':* ' + 'You registered!')
    if message.content.startswith(gccmd.cmd_prfx + gccmd.study) and message.channel.id == gccmd.study_hall:
        currentLofi = int(gcdb.getPlayerAttribute(message.author.id, 'lofi'))
        gcdb.setPlayerAttribute(message.author.id, 'lofi', currentLofi + 1)
        #response = "You work on your homework while vibing to some nice LoFi beats!"
        #await message.channel.send(response)
  
    if message.content.startswith(gccmd.cmd_prfx + gccmd.lofi):
      response = "You have {} lofi.".format(gcdb.getPlayerAttribute(message.author.id, 'lofi'))
      await message.channel.send('*' + str(message.author.display_name) + ':* ' + str(response))
      
    if message.content.startswith(gccmd.cmd_prfx + 'database'):
        response = GCplayers.all()
        await message.channel.send('*' + str(message.author.display_name) + ':* ' + response)

    if message.content.startswith(gccmd.cmd_prfx + 'map'):
        response = "mall, study hall, cafe, downtown"
        await message.channel.send('*' + str(message.author.display_name) + ':* ' + response)

    '''if message.content.startswith('!harvest'):
        #response = "you harvest your organs and hold you brain in your hands. It is squishy and wet, as a good, smart girl's brain is. You put it back before you rubb all the memories out of it."
        ID = Query()
        GCplayers.update(set('lofi', 10), ID.id == message.author.id)
        await message.channel.send(response)'''


#It is removing the role when the wrong input is given
    if message.content.startswith(gccmd.cmd_prfx + 'goto'):
        locationsList = ["mall", "study hall", "cafe", "downtown"] #List of all locations
        member = message.author #The user
        location = message.content[6:] #the input with the command removed. Hopefully only the location name
        if location not in locationsList:
            response = "i dont know that location!"
        else:       
            role = get(member.guild.roles, name=location) #This should hopefully be the same as just: name="Mall". But they can enter mall or Mall.
            roles = []
            print(roles)
            for r in message.author.roles:
                roles.append(r.name) #list of their roles.
            print(roles)
            for i in range (len(locationsList)): #I dont know if 'For loops' are okay with a bot. But it should be fine cus asyncio...?
                print(i)
                print((locationsList[i]))
                if (locationsList[i] in roles): #finding which location role the user has.
                    print('yay!')
                    role2 = get(member.guild.roles, name=locationsList[i])
                    i = len(locationsList)
                    await member.remove_roles(role2)
                    print('removed' + str(role2))
                    await member.add_roles(role)
                    print('added' + str(role))
            response = 'You begin walking to the ' + ' ' + location
        await message.channel.send('*' + str(message.author.display_name) + ':* ' + response)
        
    if message.content.startswith(gccmd.cmd_prfx + 'menu') and message.channel.id == gccmd.moonlight_cafe:
      response = "The man at the counter glares at you. He is wearing a chef's hat and his hands are shaking violently as he drinks from a teacup, full to the brim.\n"+ "strawberry cupcake: 5 money.\n"+ "strawberry: 1 money.\n"+ "cupcake: 3 money\n"
      await message.channel.send('*' + str(message.author.display_name) + ':* ' + response)
      
    if message.content.startswith(gccmd.cmd_prfx + 'work') and message.channel.id == 798059805172170782:
        pay = random.randrange(1, 5)
        total = pay + gcdb.getPlayerAttribute(message.author.id, 'money')
        response = "you work long and hard at the mall to earn some cash. you made " + str(pay) + " cash!"
        gcdb.setPlayerAttribute(message.author.id, 'money', total)
        await message.channel.send('*' + str(message.author.display_name) + ':* ' + response)
        
    if message.content.startswith(gccmd.cmd_prfx + 'order') and message.channel.id == gccmd.moonlight_cafe:
      foodNames = ["strawberry cupcake", "strawberry", "cupcake"] #the food items. Their order matches with their prices and responses in the other lists. Same indexes.
      prices = [15,10,5]  # Food/Prices/Descriptions should be defined at the base of a file, defining each time something runs is a little slow
      foodResponses = ["You recieve a pink cupcake. You're thinking that the fact its strawberry just because its pink is offensive to you until you bite down and discover the TRUE strawberry at the core, hidden. The strawberry is frozen for some reason and is making the cupcake soggy.", "Its a strawberry. You insert it into the inside of your mouth -where you eat it. Yum!", "Its a brown cupcake. Tastes pretty good but its on the dry side. It could use some strawberries."]
      order = message.content[7:]
      print(order)
      if order in foodNames:
        cost = prices[foodNames.index(order)] #matchin up the values via index.
        wallet = gcdb.getPlayerAttribute(message.author.id, 'money')
        if wallet - cost >= 0:
            gcdb.setPlayerAttribute(message.author.id, 'money', wallet - cost)
            response = foodResponses[foodNames.index(order)]
            await message.channel.send('*' + str(message.author.display_name) + ':* ' + response)
        else:
            response = "Now just how do you plan to pay for that? You only gave me {} money!".format(wallet)
            await message.channel.send('*' + str(message.author.display_name) + ':* ' + response)
      else:
        response = "Whats that supposed to be? Go bake it yourself, kid!"
        await message.channel.send('*' + str(message.author.display_name) + ':* ' + response)

#Add token
client.run('')

