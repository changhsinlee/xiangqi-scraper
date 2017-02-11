# Xiangqi scraper

Python 3.6 required.

## gameDataScraper.py

Scrapes xiangqi (chinese chess) data from playok.com into .txt files on the local machine by game. The .txt files are downloaded to a subfolder /data of where the script is. Modify the variables start and end to define the range of game logs to scrape. 

## gameDataParser.py

When put in the parent folder of /data where downloaded .txt files are, parses the .txt files to gameinfo.csv and moves.csv.

