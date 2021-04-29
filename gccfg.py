#not to many thing should be imported here to avoid circular imports
import discord

# create client here so that its global
client = discord.Client()

cmd_prefix = "~"

# maps that get setup in gcloader later
cmd_map = {}
location_map = {}
role_map = {}

# options to make bot automatically setup channels and roles
# needs more testing and polishing and should not be use on main server yet
# very convienent for test server where channel and roles can be created and deleted without consequence
construct_mising_channels = False
construct_mising_roles = False 
