from RiotAPI import RiotAPI
import datetime
import numpy as np
import time
import os
from Engine import *
import RiotConsts as Consts

X = np.zeros(shape=(0,2), dtype=float)
Y = np.zeros(shape=(0,1), dtype=float)

def fileExist(f):
    return os.path.isfile(f)

# User configuration settings **********

playerName = ''
region=Consts.REGIONS['']
apikey = ''

# **************************************

xfile = 'xdata.npy'
yfile = 'ydata.npy'

api = RiotAPI(apikey, region)
result = api.get_summoner_by_name(playerName)
playerID = result[playerName]['id']
result = api.get_summoner_by_id(playerID)
totalGames = result['totalGames']
if (totalGames == 0):
    print('No ranked games this season for this user.')
    exit()
elif (totalGames < 100):
    print('This user have less than 100 ranked games.')
    print('For better AI performance you must have')
    print('at least 100 games.')
    exit()
gameList = result['matches']
totalRequests = requestCounter = 2
print('Total games online:', totalGames)

if fileExist(xfile) and fileExist(yfile):
    X = np.load(xfile)
    Y = np.load(yfile)
else:
    print('Donloading information...')
    for game in gameList:
        timeStamp = game['timestamp']
        matchID = game['matchId']
        result = api.get_match_by_id(matchID)
        participantIdentities = result['participantIdentities']
        participantId = 0
        for participant in participantIdentities:
            if participant['player']['summonerName'] == playerName:
                participantId = participant['participantId']
        participants = result['participants']
        winner = False
        for participant in participants:
            if participant['participantId'] == participantId:
                winner = participant['stats']['winner']
        dateTime = datetime.datetime.fromtimestamp(timeStamp/1000.0)
        X = np.append(X, [[dateTime.weekday(), dateTime.hour]], axis=0)
        Y = np.append(Y, [[winner]], axis=0)
        requestCounter += 1
        totalRequests += 1
        if requestCounter >= 10:
            time.sleep(10)
            requestCounter = 0
        if totalRequests >= 500:
            time.sleep(600)
            totalRequests = 0
    np.save(xfile, X)
    np.save(yfile, Y)
    print('Complete.')

print('Total games in database:', len(Y))

engine = Engine(xfile, yfile)
engine.run()
