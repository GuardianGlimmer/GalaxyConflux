import discord 

import gccfg
import gcdb

from tinydb import Query


GCplayers = gcdb.GCplayers

class GCPlayer:
    # setup default values
    def __init__(
        self,
        userid = 0,
        location = "downtown",
        purity = "pure",
        lofi = 0,
        money = 0
    ):
        # Check for and possibly load saved data
        SavedData = gcdb.getPlayerData(userid)
        if SavedData:
            self.userid = userid
            self.location = SavedData["location"]
            self.purity = SavedData["purity"]
            self.lofi = SavedData["lofi"]
            self.money = SavedData["money"]
            self.new = False
        # Or initialize from given values
        else:
            self.userid = userid
            self.location = location
            self.purity = purity
            self.lofi = lofi
            self.money = money
            self.persist()
            self.new = True

    def persist(self):
        User = Query()
        GCplayers.upsert({
            'id': self.userid,
            'location': self.location,
            'purity': self.purity,
            'lofi': self.lofi,
            'money': self.money
        },
        User.id == self.userid
        )
        print("UPSERT")
        """
        # Grab existing data
        SavedData = gcdb.getPlayerData(self.userid)

        # Iterate through all saved values
        for key in SavedData:
            if SavedData[key] != self.key:
                # Only Bother with changed values
                gcdb.setPlayerAttribute(self.userid, key, self.key)"""


class GCLocation:
    def __init__(self, _id, _json_entry = None):
        self.id = _id
        self.role_name = _json_entry.get("role_name")
        self.full_name = _json_entry.get("full_name")
        self.names = _json_entry.get("location_names")
        self.look_txt = _json_entry.get("look_txt")

        #attempt to get channel id for location
        self.channel_id = None
        channel_found = False
        guild = gccfg.client.guilds[0]
        for channel in guild.channels:
            if channel_found == False:  
                if type(channel) == discord.TextChannel:
                    if channel.name == self.id:
                        self.channel_id = channel.id
                        channel_found = True

        self.print_missing_data()

    def is_alias(self, alias):
        if alias in self.names:
            return True
        else:
            return False 

    
    def print_missing_data(self):
        #print info about missing data incase something is missing from location_cfg.json
        if (self.names == None):
            print(f"{self.id} location has no alias names")
        if (self.full_name == None):
            print(f"{self.id} location has no full name")
        if (self.look_txt == None):
            print(f"{self.id} location has no look text")
        if (self.channel_id == None):
            print(f"there is no #{self.id} channel")
            
            
class GCFisher:
    Fishing = False
    bite = False
	fishing_id = 0
    prompts = 0
    reward = 0
    
    def stop(self): 
		self.fishing = False
		self.bite = False
        self.fishing_id = 0
        self.prompts = 0
        self.reward = 0
