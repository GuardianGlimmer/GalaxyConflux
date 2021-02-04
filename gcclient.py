import discord
import gccmd
from tinydb import TinyDB, Query
from tinydb.operations import increment, subtract
import jsons
from discord.utils import get


#sets up the database
GCplayers = TinyDB("C:\\Users\\frost\\Desktop\\GalaxyConflux-main\\GCplayers.json")

client = discord.Client()



'''
class gcplayer:
  _id = ""
  loc = "study hall"
  purity = 'pure'
  lofi = 0

  def __init__(self, _id):
    self.id = _id
    ID = Query()
    result = GCplayers.search(ID.id == _id)

    if result == None:
i shou      GCplayers.insert({'id': _id, 'location' : 'study hall', 'purity' : 'pure', 'lofi' : 0})
                       
  def save(self):
      p_data = {
        'lofi' : self.lofi,
        'loc' : self.loc,
        'purity' : self.purity,
      }
      GCplayers.update({p_data}, self.id == _id)
'''


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    
@client.event


async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(gccmd.cmd_prfx + 'register'):
        GCplayers.insert({'id': message.author.id, 'location' : 'study hall', 'purity' : 'pure', 'lofi' : 0})
        
    if message.content.startswith(gccmd.cmd_prfx + gccmd.study) and message.channel.id == gccmd.study_hall:
        ID = Query()
        GCplayers.update(increment('lofi'), ID.id == message.author.id)
        response = "You work on your homework while vibing to some nice LoFi beats!"
        await message.channel.send(response)
  
    if message.content.startswith(gccmd.cmd_prfx + gccmd.lofi):
      Lofi = Query()
      response = GCplayers.search(Lofi.id == message.author.id)
      if (int(response) < 0):
        response += ". You feel stressed."
      elif (int(response) > 100):
        response += ". You're so chill that the fridge feels like a radiator."
      await message.channel.send(response)
      
    if message.content.startswith(gccmd.cmd_prfx + 'database'):
        response = GCplayers.all()
        await message.channel.send(response)

    if message.content.startswith('!harvest'):
        response = "you harvest your organs and hold you brain in your hands. It is squishy and wet, as a good, smart girl's brain is. You put it back before you rubb all the memories out of it."
        ID = Query()
        GCplayers.update(subtract('lofi', 10), ID.id == message.author.id)
        await message.channel.send(response)

    if message.content.startswith(gccmd.cmd_prfx + 'goto'):
        locationsList = ["mall", "study hall", "moonlight cafe"] #List of all locations
        member = message.author #The user
        location = message.content[6:] #the input with the command removed. Hopefully only the location name
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
                await member.add_roles(role)
        response = 'You begin walking to the ' + ' ' + location
        await message.channel.send(response)
    
    if message.content.startswith(gccmd.com_prfx + 'menu'):
      #member = message.author
      #role = get(member.guild.roles, name="moonlight cafe")
      #if (role not in message.author.roles): #This is just to make sure they're actually in the cafe
      #  await message.channel.send("You look into the sky and daze off like an idiot.")
      response = "The man at the counter glares at you. He is wearing a chef's hat and his hands are shaking violently as he drinks from a teacup, full to the brim.\n"+ "Strawberry cupcake: 5 lofi.\n"+ "Strawberry: 1 lofi.\n"+ "Cupcake: 3 lofi\n"
      await message.channel.send(response)
      
    if message.content.startswith(gccmd.com_prfc + 'order'):
      #member = message.author
      #role = get(member.guild.roles, name="moonlight cafe")
      #if (role not in message.author.roles): #This is just to make sure they're actually in the cafe
      #  await message.channel.send("You look into the sky and daze off like an idiot.")
      
      foodNames = ["Strawberry Cupcake", "Strawberry", "Cupcake"] #the food items. Their order matches with their prices and responses in the other lists. Same indexes.
      prices = [5,1,3]
      foodResponses = ["You recieve a pink cupcake. You're thinking that the fact its strawberry just because its pink is offensive to you until you bite down and discover the TRUE strawberry at the core, hidden. The strawberry is frozen for some reason and is making the cupcake soggy.", "Its a strawberry. You insert it into the inside of your mouth -where you eat it. Yum!", "Its a brown cupcake. Tastes pretty good but its on the dry side. It could use some strawberries."]
      order = message.content.replace("~menu ","",1) #maybe this is a better way of removing the command? If it works. The 1 is so it only removes that phrase once.
      if (order in foodNames):
        cost = prices[foodNames.index(order)] #matchin up the values via index.
        ID = Query()
        GCplayers.update(subtract('lofi', cost), ID.id == message.author.id)
        response = foodResponses[foodNames.index(order)]
      else:
        response = "Whats that supposed to be? Go bake it yourself, kid!"
      await message.channel.send(response)
        

#Add token
client.run('')   

