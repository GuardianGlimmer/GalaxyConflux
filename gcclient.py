import discord
import gccmd
from tinydb import TinyDB, Query
from tinydb.operations import increment
import jsons
from discord.utils import get
#from discord.exe import commands

#bot = commands.Bot(command_prefix = '~')

#sets up the database
GCplayers = TinyDB('D:\GalaxyConflux Master\GCplayers.json')

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
      await message.channel.send(response)
      
    if message.content.startswith(gccmd.cmd_prfx + 'database'):
        response = GCplayers.all()
        await message.channel.send(response)

    if message.content.startswith('!harvest'):
        response = 'get fucked idiot'
        await message.channel.send(response)

    if message.content.startswith(gccmd.cmd_prfx + 'goto' + ' ' + 'mall'):
        member = message.author
        role = get(member.guild.roles, name="Mall")
        role2 = get(member.guild.roles, name="study hall")
        response = 'You begin walking to the Mall!'
        await member.remove_roles(role2)
        await member.add_roles(role)
        await message.channel.send(response)

    if message.content.startswith(gccmd.cmd_prfx + 'goto' + ' ' + 'study hall'):
        member = message.author
        role = get(member.guild.roles, name="study hall")
        role2 = get(member.guild.roles, name="Mall")
        response = 'You begin walking to the study hall!'
        await member.remove_roles(role2)
        await member.add_roles(role)
        await message.channel.send(response)
        

#Add token
client.run('')   

