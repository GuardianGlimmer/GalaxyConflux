import gcdb
import random
import discord
import asyncio
from tinydb import TinyDB
from gcclasses import GCPlayer

GCplayers = TinyDB("./GCplayers.json")

#this part defines commands
cmd_prfx = '~'
study = 'study'
bake = 'bake'
allow = 'allowance'
lofi = 'lofi'

# Define command prefixes
study_txt = 'study'
lofi_txt = 'lofi'
money_txt = 'money'
register_txt = 'register'
menu_txt = 'menu'
work_txt = 'work'
goto_txt = 'goto'
order_txt = 'order'
db_txt = 'database'
map_txt = 'map'

#this part assigns locations with their chanenl ID
study_hall_channel_id = 788095887884288052
moonlight_cafe_channel_id = 805464853967929344
mall_channel_id = 798059805172170782

#command responses
study_response = "You work on your homework while vibing to some nice LoFi beats!"
bake_response = 'you take a break to bake a nice batch of cookies.'
allow_response = 'What a good girl! here, have some allowance.'

# Define commands
'''
    Adds 1 to lofi when sent in the study channel
'''
async def study_cmd(msg):
    if msg.channel.id == study_hall_channel_id:
        currentLofi = int(gcdb.getPlayerAttribute(msg.author.id, 'lofi'))
        gcdb.setPlayerAttribute(msg.author.id, 'lofi', currentLofi + 1)

'''
    Shows user their current lofi
'''
async def lofi_cmd(msg):
    response = "You have {} lofi.".format(gcdb.getPlayerAttribute(msg.author.id, 'lofi'))
    await msg.channel.send('*' + str(msg.author.display_name) + ':* ' + str(response))

'''
    Shows user their current money
'''
async def money_cmd(msg):
    response = "You have {} currency.".format(gcdb.getPlayerAttribute(msg.author.id, 'money'))
    await msg.channel.send('*' + str(msg.author.display_name) + ':* ' + str(response))

'''
    Shows user what is for sale at the cafe
'''
async def menu_cmd(msg):
    if msg.channel.id == moonlight_cafe_channel_id:
        response = "The man at the counter glares at you. He is wearing a chef's hat and his hands are shaking violently as he drinks from a teacup, full to the brim.\n" + "strawberry cupcake: 5 money.\n" + "strawberry: 1 money.\n" + "cupcake: 3 money\n"
        await msg.channel.send('*' + str(msg.author.display_name) + ':* ' + response)

''' 
    Buys food for user if they have the funds
'''
async def order_cmd(msg):
    # Setup Necessary Variables
    foodNames = ["strawberry cupcake", "strawberry", "cupcake"]  # the food items. Their order matches with their prices and responses in the other lists. Same indexes.
    prices = [15, 10, 5]  # Food/Prices/Descriptions should be defined at the base of a file, defining each time something runs is a little slow
    foodResponses = ["You recieve a pink cupcake. You're thinking that the fact its strawberry just because its pink is offensive to you until you bite down and discover the TRUE strawberry at the core, hidden. The strawberry is frozen for some reason and is making the cupcake soggy.", "Its a strawberry. You insert it into the inside of your mouth -where you eat it. Yum!",
                     "Its a brown cupcake. Tastes pretty good but its on the dry side. It could use some strawberries."]
    order = msg.content.split(' ', 1)[1] # splits the text into a list of two strings at the first " "

    # Ensure food exists
    if order in foodNames:
        # Check price
        cost = prices[foodNames.index(order)]  # matchin up the values via index.
        wallet = gcdb.getPlayerAttribute(msg.author.id, 'money')
        if wallet - cost >= 0:
            # Subtract cost and send response if they can afford it
            gcdb.setPlayerAttribute(msg.author.id, 'money', wallet - cost)
            response = foodResponses[foodNames.index(order)]
            await msg.channel.send('*' + str(msg.author.display_name) + ':* ' + response)
        else:
            # Tell them if they're a broke ass bitch
            response = "Now just how do you plan to pay for that? You only gave me {} money!".format(wallet)
            await msg.channel.send('*' + str(msg.author.display_name) + ':* ' + response)
    else:
        # Tell them the food doesn't exist
        response = "Whats that supposed to be? Go bake it yourself, kid!"
        await msg.channel.send('*' + str(msg.author.display_name) + ':* ' + response)

'''
    Moves the user to target location
'''
async def goto_cmd(msg):
    # Setup necessary variables
    locationsList = ["mall", "study hall", "cafe", "downtown"] #List of all locations
    member = msg.author #The user
    location = msg.content.split(' ', 1)[1] #the input with the command removed. Hopefully only the location name

    # Check if they're going to a real place
    if location not in locationsList:
        # Tell them they're wrong
        response = "i dont know that location!"
        await msg.channel.send('*' + str(msg.author.display_name) + ':* ' + response)
    else:
        # Tell them they're moving
        response = 'You begin walking to the' + ' ' + location
        await msg.channel.send('*' + str(msg.author.display_name) + ':* ' + response + ". it will take 5 seconds")
        await asyncio.sleep(5)

        # Grab target role
        role = discord.utils.get(member.guild.roles, name=location) #This should hopefully be the same as just: name="Mall". But they can enter mall or Mall.

        # Grab current role names to search
        user_role_names = []
        for r in msg.author.roles:
            user_role_names.append(r.name) #list of their roles.

        # Ensure all existing Location Roles are removed
        for LocationName in locationsList: #I dont know if 'For loops' are okay with a bot. But it should be fine cus asyncio...?
            if (LocationName in user_role_names): #finding which location role the user has.
                role2 = discord.utils.get(member.guild.roles, name=LocationName)
                await member.remove_roles(role2)
                print('removed' + str(role2))

        # Always add target role
        await member.add_roles(role)
        print('added' + str(role))

'''
    Pays user per command, if done in mall
'''
async def work_cmd(msg):
    if msg.channel.id == mall_channel_id:
        pay = random.randrange(1, 5)
        total = pay + gcdb.getPlayerAttribute(msg.author.id, 'money')
        response = "you work long and hard at the mall to earn some cash. you made " + str(pay) + " cash!"
        gcdb.setPlayerAttribute(msg.author.id, 'money', total)
        await msg.channel.send('*' + str(msg.author.display_name) + ':* ' + response)

'''
    Setup the user's database entry if they have none
'''
async def register_cmd(msg):
    if GCPlayer(userid=msg.author.id).new:
        await msg.channel.send('*' + str(msg.author.display_name) + ':* ' + 'You registered!')
    else:
        await msg.channel.send('*' + str(msg.author.display_name) + ':*' + ' you already registered')

'''
    Return the entire database as text for debugging
'''
async def db_cmd(msg):
    response = str(GCplayers.all())
    await msg.channel.send('*' + str(msg.author.display_name) + ':* ' + response)

'''
    Returns all location names
'''
async def map_cmd(msg):
    response = "mall, study hall, cafe, downtown"
    await msg.channel.send('*' + str(msg.author.display_name) + ':* ' + response)

# Create cmd dictionary
cmd_dict = {
    study_txt : study_cmd,
    lofi_txt : lofi_cmd,
    money_txt : money_cmd,
    work_txt : work_cmd,
    goto_txt : goto_cmd,
    order_txt : order_cmd,
    menu_txt : menu_cmd,
    register_txt : register_cmd,
    db_txt : db_cmd,
    map_txt : map_cmd,
}