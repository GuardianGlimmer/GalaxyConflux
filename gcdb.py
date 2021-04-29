from tinydb import TinyDB, where
from tinydb.operations import increment, subtract, add, set


GCplayers = TinyDB("./database/GCplayers.json")

'''
    Retrieves a single passed attribute for a particular player
'''
def getPlayerAttribute(userid, attr):
    data = GCplayers.search(where('id') == userid)
    if len(data) == 1:
        return(data[0][attr])
    else:
        print("Failed to retrieve {} for player {}".format(attr, str(userid)))
        return False

'''
    Changes the attribute in the database for a particular player
'''
def setPlayerAttribute(userid, attr, value):
    try:
        GCplayers.update(set(attr, value), where('id') == userid)
        return True
    except:
        print("Failed to set {} to {} for player {}".format(attr, str(value), str(userid)))
        return False

'''
    Creates a new "Row" in the database for a passed 
    GCUser class. Careful. Don't wanna give someone 
    multiple entries.
'''
def createEntry(gcuser):
    GCplayers.insert({'id': gcuser.userid,
                      'location': gcuser.location,
                      'purity': gcuser.purity,
                      'lofi': gcuser.lofi,
                      'money': gcuser.money})

'''
    Returns the disctionary of a player's stored data,
    if there are multiple or no entries, it returns 
    false.
'''
def getPlayerData(userid):
    data = GCplayers.search(where('id') == userid)
    if len(data) == 1:
        return (data[0])
    else:
        return False

