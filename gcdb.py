from tinydb import TinyDB, where
from tinydb.operations import increment, subtract, add, set

GCplayers = TinyDB("./GCplayers.json")

def getPlayerAttribute(userid, attr):
    data = GCplayers.search(where('id') == userid)
    if len(data) == 1:
        return(data[0][attr])
    else:
        print("Failed to retrieve {} for player {}".format(attr, str(userid)))
        return False

def setPlayerAttribute(userid, attr, value):
    try:
        GCplayers.update(set(attr, value), where('id') == userid)
        return True
    except:
        print("Failed to set {} to {} for player {}".format(attr, str(value), str(userid)))
        return False

def createEntry(userid):
    GCplayers.insert({'id': userid, 'lofi': 0, 'money': 0, })