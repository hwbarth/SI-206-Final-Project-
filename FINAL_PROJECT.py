'''
FINAL PROJECT:

Golfing Brothers

Harrison Barth
Kagan Shetterly

SI 206

April 26, 2022

Golf Leaderboard API:
https://rapidapi.com/sportcontentapi/api/golf-leaderboard-data

PGA Tour player statistics:
https://www.pgatour.com/stats.html

'''

import sqlite3
import os
import matplotlib.pyplot as plt
import numpy as np
#from asyncore import write
#from xml.sax import parseString
from bs4 import BeautifulSoup
import requests
import csv
import unittest

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def getGolfLeaderBoard():
    
    pass

def getAvgDrivingDistance(cur, conn):
    site = requests.get("https://www.pgatour.com/stats.html")

    f = site.text

    soup = BeautifulSoup(f, "html.parser")

    
    tableSeeAll = soup.find_all("a", class_ = "see-all")
    
    seeAllLink = tableSeeAll[3]["href"]

    link = "https://www.pgatour.com/" + str(seeAllLink)
    opened = requests.get(link)

    soup2 = BeautifulSoup(opened.text, "html.parser")

    drivingTable = soup2.find("table", class_ = "table-styled")

    rows = drivingTable.find_all("tr")   

    drivingDict = {}

    cur.execute('''
    DROP TABLE IF EXISTS Driving
    ''')

    cur.execute('''
    CREATE TABLE Driving (name TEXT, distance REAL)
    ''')



    for row in rows:
        
        player_name = row.find("td", class_ = "player-name")

        #playerName = player_name.find("a").string
        '''
        if (type(player_name) != None):
            playerName = player_name.find("a")

            print(playerName)
        '''
        name1 = ""
        drivingDistance = 0
   
        #print(player_name)
        if player_name != None:
            name = player_name.find("a")
            #print(name.string)
            name1 = str(name.string)
        

        driving_distance = row.find_all("td")

        if driving_distance != None:
            if len(driving_distance) > 5:
                #print(driving_distance[4].string)
                drivingDistance = float(driving_distance[4].string)
        

        
        if drivingDistance != 0 and name1 != "":
            
            cur.execute('''
            INSERT INTO Driving (name, distance)
            VALUES (?, ?)
            ''', (name1, drivingDistance))
            print(name1)
            print(drivingDistance)
    conn.commit()
            
    
    #drivingTableSeeAll


def getGreensInRegPct(cur, conn):
    site = requests.get("https://www.pgatour.com/stats.html")

    f = site.text

    soup = BeautifulSoup(f, "html.parser")

    
    tableSeeAll = soup.find_all("a", class_ = "see-all")
    
    seeAllLink = tableSeeAll[5]["href"]

    link = "https://www.pgatour.com/" + str(seeAllLink)
    opened = requests.get(link)

    soup2 = BeautifulSoup(opened.text, "html.parser")

    greensPctTable = soup2.find("table", class_ = "table-styled")
    #print(greeensPctTable)


    rows = greensPctTable.find_all("tr")   

    

    cur.execute('''
    DROP TABLE IF EXISTS GreensInReg
    ''')

    cur.execute('''
    CREATE TABLE GreensInReg (name TEXT, percentage REAL)
    ''')



    for row in rows:
        
        player_name = row.find("td", class_ = "player-name")

        #playerName = player_name.find("a").string
        '''
        if (type(player_name) != None):
            playerName = player_name.find("a")

            print(playerName)
        '''
        name1 = ""
        greensReg = 0
   
        #print(player_name)
        if player_name != None:
            name = player_name.find("a")
            #print(name.string)
            name1 = str(name.string)
            print(name1)

        greens_reg = row.find_all("td")

        if greens_reg != None:
            if len(greens_reg) > 5:
                #print(driving_distance[4].string)
                greensReg = float(greens_reg[4].string)
        

        
        if greensReg != 0 and name1 != "":
            
            cur.execute('''
            INSERT INTO GreensInReg (name, percentage)
            VALUES (?, ?)
            ''', (name1, greensReg))
            print(name1)
            print(greensReg)
    conn.commit()




    

def getStrokesGainedOffTee():
    pass

def getScrablingPct():
    pass

def getStrokesGainedPutting():
    pass





def main():
    dbname = "GolfingBrothers.db"
    cur, conn = setUpDatabase(dbname)

    getGreensInRegPct(cur, conn)


    #getAvgDrivingDistance(cur, conn)





main()







