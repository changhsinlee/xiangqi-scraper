#! python3
# gameDataParser.py -
# Parsing game data downloaded from playok.com to data objects in python

import os, re
import pandas as pd

# set working directory to where data is
dataPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
os.makedirs(dataPath, exist_ok=True)
os.chdir(dataPath)

# Load data as string
# dataFileName = '57390689.txt'
gameInfoData = []

for dataFileName in os.listdir('.'):
    gameFile = open(dataFileName)
    gameContent = gameFile.readlines()
    # print(gameContent)

    # Record game information
    currentGameInfo = {}
    currentGameInfo['gameID'] = dataFileName.split('.')[0]

    # PlayerIDs and ELOs
    idEloRegex = re.compile(r'''
        (\S+)            # color
        (\s+)            # spaces
        (\S+)            # playerID
        ([^\d]+)         # not number
        (\d{1,4})        # ElO (1-4 digits number)
        ''', re.VERBOSE)
       
    redInfo = idEloRegex.search(gameContent[1])
    blackInfo = idEloRegex.search(gameContent[2])
    currentGameInfo['redID'] = redInfo.group(3)
    currentGameInfo['redELO'] = redInfo.group(5)
    currentGameInfo['blackID'] = blackInfo.group(3)
    currentGameInfo['blackELO'] = blackInfo.group(5)

    # Game Result
    resultRegex = re.compile(r'(\d{1}-\d{1})')
    gameResult = resultRegex.search(gameContent[3]).group(1)
    if gameResult == '1-0': 
        currentGameInfo['winner'] = 'red'
    elif gameResult == '0-1':
        currentGameInfo['winner'] = 'black'
    else:
        currentGameInfo['winner'] = 'NA'

    # Parse game moves from line 7 and on, save into a separate variable
    moveRegex = re.compile(r'(\w\d[\.+]\d)')
    gameMoves = []
    for moveString in gameContent[7:]:
        gameMoves += moveRegex.findall(moveString)

    # Split list into odd (black moves) and even (red moves)
    blackMoves = gameMoves[1:][::2]
    redMoves = gameMoves[::2]

    # TODO: parse datetime

    gameFile.close()

    gameInfoData.append(currentGameInfo)
    
    # print(currentGameInfo)
    # print(blackMoves)
    # print(redMoves)

# Save gameInfo into a dataframe
gameInfo = pd.DataFrame(gameInfoData)[['gameID', 'blackID', 'blackELO', 'redID', 'redELO', 'winner']]
print(gameInfo)

# Save moveInfo into a dataframe