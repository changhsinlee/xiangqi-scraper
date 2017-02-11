#! python3
# chineseChessGameDataScraper.py -
# Downloads chinese chess (xiangqi) data from playok.com into .txt files
# example: http://www.playok.com/zh/game.phtml/57390680.txt?xq

import os, requests

# set working directory to where script is
dataPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
os.makedirs(dataPath, exist_ok=True)
os.chdir(dataPath)

start = 57385152
end = 57390690

gameList = list(range(start,end))

for gameID in gameList:
    # open corresponding page
    targetURL = f'http://www.playok.com/zh/game.phtml/{str(gameID)}.txt?xq'
    res = requests.get(targetURL)
    res.raise_for_status()
    
    # Save content of page into corresponding text file
    gameFileName = f'{str(gameID)}.txt'
    gameFile = open(gameFileName, 'wb')
    for chunk in res.iter_content(100000):
        gameFile.write(chunk)
        
    gameFile.close()
    print('Parsed gameid ' + str(gameID))

