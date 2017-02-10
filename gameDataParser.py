#! python3
# gameDataParser.py -
# Parsing game data downloaded from playok.com to data objects in python

import os, re

# set working directory to where data is
dataPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
os.makedirs(dataPath, exist_ok=True)
os.chdir(dataPath)

# Load data as string
dataFileName = '57390680.txt'

gameFile = open(dataFileName)
gameContent = gameFile.readlines()
# print(gameContent)

# Record player information: for each gameid, get red and black player id and elo
gameInfo = {}
gameInfo['gameID'] = dataFileName.split('.')[0]

# Find player information in the game
idEloRegex = re.compile(r'''
    (\S+)            # color
    (\s+)            # spaces
    (\S+)            # playerID
    ([^\d]+)         # not number
    (\d{1,4})        # ElO (1-4 digits number)
    ''', re.VERBOSE)

# PlayerIDs and ELOs
redInfo = idEloRegex.search(gameContent[1])
blackInfo = idEloRegex.search(gameContent[2])

gameInfo['redID'] = redInfo.group(3)
gameInfo['redELO'] = redInfo.group(5)
gameInfo['blackID'] = blackInfo.group(3)
gameInfo['blackELO'] = blackInfo.group(5)

# Game Result
resultRegex = re.compile(r'(\d{1}-\d{1})')
gameResult = resultRegex.search(gameContent[3]).group(1)
if gameResult == '1-0': 
    gameInfo['winner'] = 'red'
elif gameResult == '0-1':
    gameInfo['winner'] = 'black'
else:
    gameInfo['winner'] = 'NA'

# TODO: datetime, event

# TODO: Save moves into a separate variable

gameFile.close()

print(gameInfo)
