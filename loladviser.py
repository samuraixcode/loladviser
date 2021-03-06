from RiotAPI import RiotAPI
import datetime
import numpy as np
import time
import os
from Engine import Engine
import RiotConsts as Consts
import pickle
import UserConfiguration as Conf

X = np.zeros(shape=(0,2), dtype=float)
Y = np.zeros(shape=(0,1), dtype=float)

def fileExist(f):
    return os.path.isfile(f)

gameRegister = []
if fileExist('greg'):
    infile = open('greg', 'rb')
    gameRegister = pickle.load(infile)
    infile.close()

playerName = Conf.USER['name']
region = Consts.REGIONS[Conf.USER['region']]
apikey = Conf.USER['api']

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
elif (totalGames < 29):
    print('This user have less than 29 ranked games.')
    print('For better AI performance you must have')
    print('at least 29 ranked games.')
    exit()

gameList = result['matches']

# Variable to watch for the request limit
counter = 2

if fileExist(xfile) and fileExist(yfile):
    X = np.load(xfile)
    Y = np.load(yfile)

newGames = totalGames-len(Y)
if newGames > 0:
    print('Downloading games data.', '[{} new]'.format(newGames))

for game in gameList:

    # Checking if the match is already in our database
    matchID = game['matchId']
    if matchID in gameRegister:
        continue

    result = api.get_match_by_id(matchID)
    counter += 1

    participantIdentities = ''
    try:
        # If there is an exception, we are over the request rate limit
        # and the last call didn't provide the information
        participantIdentities = result['participantIdentities']
    except:
        print('Downloading interrupted.')
        break

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
    gameRegister.append(matchID)

    np.save(xfile, X)
    np.save(yfile, Y)
    outfile = open('greg', 'wb')
    pickle.dump(gameRegister, outfile)
    outfile.close()

    if counter % 10 == 0:
        time.sleep(13)
    if counter % 500 == 0:
        time.sleep(603)

if totalGames-len(Y) == 0:
    print('Database up to date.')
else:
    print('Database not up to date.')
    print('Please restart the program.')
    print('NOTE: This can happen several times')
    print('until the data base is up to date.')
    print('The interruption occur because riot')
    print('have request rate limit.')
    print('There are {} games data left.'.format(totalGames-len(Y)))
    print('Exiting.')
    exit()

engine = Engine(xfile, yfile)
engine.run()
