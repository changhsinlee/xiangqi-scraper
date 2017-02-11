#! python3
# gameDataParser.py -
# Parsing game data downloaded from playok.com to data objects in python

import os, re
import pandas as pd

# set working directory to where data is
dataPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
os.makedirs(dataPath, exist_ok=True)
os.chdir(dataPath)

gameInfoData = []
moveData = []

for dataFileName in os.listdir('.'):
    gameFile = open(dataFileName)
    gameContent = gameFile.readlines()

    # Parse game information
    # gameID
    currentGameInfo = {}
    currentGameInfo['gameID'] = dataFileName.split('.')[0]

    # Parse playerIDs and ELOs
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

    # Parse game result
    resultRegex = re.compile(r'([01]-[01])')
    gameResult = resultRegex.search(gameContent[3]).group(1)
    if gameResult == '1-0': 
        currentGameInfo['winner'] = 'red'
    elif gameResult == '0-1':
        currentGameInfo['winner'] = 'black'
    else:
        currentGameInfo['winner'] = 'NA'
        
    # Parse datetime
    timeRegex = re.compile(r'(20\d{2}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})')
    currentGameInfo['game_datetime'] = timeRegex.search(gameContent[4]).group(1)
    
    # Add to gameinfo list
    gameInfoData.append(currentGameInfo)
    
    # Parse game moves from line 7 and on, save into a separate variable
    moveRegex = re.compile(r'(\w\d[\.+-=]\d)')
    gameMoves = []
    for moveString in gameContent[7:]:
        gameMoves += moveRegex.findall(moveString)

    # Split list into odd (black moves) and even (red moves)
    blackMoves = gameMoves[1:][::2]
    redMoves = gameMoves[::2]

    # Parse moves
    movesData = []
    for movenum in range(len(redMoves)):
        currentMove = {}
        currentMove['gameID'] = dataFileName.split('.')[0]
        currentMove['movenum'] = movenum + 1
        currentMove['side'] = 'red'
        currentMove['move'] = redMoves[movenum]
        moveData.append(currentMove)
    
    for movenum in range(len(blackMoves)):
        currentMove = {}
        currentMove['gameID'] = dataFileName.split('.')[0]
        currentMove['movenum'] = movenum + 1
        currentMove['side'] = 'black'
        currentMove['move'] = blackMoves[movenum]
        moveData.append(currentMove)
    
    gameFile.close()

    
    # print(currentGameInfo)
    

    
    # print(blackMoves)
    # print(redMoves)

# Save gameInfo into a dataframe
gameInfo = pd.DataFrame(gameInfoData)[['gameID', 'game_datetime', 'blackID', 'blackELO', 'redID', 'redELO', 'winner']]
print(gameInfo)

# Save moves into a dataframe
moves = pd.DataFrame(moveData)[['gameID','side','movenum','move']]
print(moves)

# Save dataframe into .csv
csvPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data_csv')
os.makedirs(csvPath, exist_ok=True)
os.chdir(csvPath)
gameInfo.to_csv('gameinfo.csv')
moves.to_csv('moves.csv')