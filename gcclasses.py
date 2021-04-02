import gcdb

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
            gcdb.createEntry(self)
            self.new = True

    def persist(self):
        # Grab existing data
        SavedData = gcdb.getPlayerData(self.userid)

        # Iterate through all saved values
        for key in SavedData:
            if SavedData[key] != self.key:
                # Only Bother with changed values
                gcdb.setPlayerAttribute(self.userid, key, self.key)