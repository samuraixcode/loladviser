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

gameRegister = []
if fileExist('greg'):
    gameRegister = pickle.load('greg')

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
    print('at least 100 ranked games.')
    exit()

gameList = result['matches']

counter = 5

if fileExist(xfile) and fileExist(yfile):
    X = np.load(xfile)
    Y = np.load(yfile)

print('Donloading information.')

for game in gameList:

    matchID = game['matchId']
    if matchID in gameRegister:
        continue
    else:
        gameRegister.append(matchID)

    result = api.get_match_by_id(matchID)
    counter += 1

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

    timeStamp = game['timestamp']
    dateTime = datetime.datetime.fromtimestamp(timeStamp/1000.0)

    X = np.append(X, [[dateTime.weekday(), dateTime.hour]], axis=0)
    Y = np.append(Y, [[winner]], axis=0)

    if counter % 10 == 0:
        time.sleep(13)
    if counter % 500 == 0:
        time.sleep(603)

np.save(xfile, X)
np.save(yfile, Y)
pickle.dump(gameRegister, 'greg')
print('Complete.')

diffGames = len(Y)-totalGames
if diffGames == 0:
    print('Database up to date.')

engine = Engine(xfile, yfile)
engine.run()
