import pandas as pd
import re

# this is a class that will wrap around the data-frame for a player, along with it's dictionary of statistics
class PlayerData:
    def __init__(self) -> None:
        self.generalFantasyAttrDict = {}
        self.gamesDF = pd.DataFrame()
        self.dictLabels = ['player_name', 'player_team', 'player_pos', 'player_price', 'player_avail', 'games_played', 'avg_fantasy_pts', 
                           'total_fantasy_pts', 'last_wk_fantasy_pts', '3_wk_avg', '5_wk_avg', 'high_score', 'low_score', 'owned_by', 
                           '$/point', 'round-rank', 'season_rank']
        self.floatLabels = ['player_price', 'avg_fantasy_pts', '3_wk_avg', '5_wk_avg', 'owned_by', '$/point']
        self.intLabels = ['games_played', 'total_fantasy_pts', 'last_wk_fantasy_pts', 'high_score', 'low_score', 'round_rank', 'season_rank']
        self.playerGameDataLabels = ['minutes', 'goals', 'assists', 'clean-sheets', 'penalty-saves', 'penalties-earned', 'penalty-misses', 'goals-against', 'saves', 'yellow-cards', 
                          'red-cards', 'own-goals', 'tackles', 'passes', 'key-passes', 'crosses', 'big-chances-created', 'clearances', 'blocked-passes', 'interceptions',
                          'recovered-balls', 'error-leading-to-goals', 'own-goal-assists', 'shots', 'was-fouled']
        
    # takes HTML content from MLS Fantasy player page, loads it into this PlayerData instance
    def parseData(self, htmlContent):
        # getting data from tables
        
        playerName = (htmlContent.find("p", {"class":"profile-name"}).get_text()).strip()
        self.generalFantasyAttrDict.update({"player_name" : playerName})
        
        playerTeam = (htmlContent.find("p", {"class":"player-team"}).get_text()).strip()
        self.generalFantasyAttrDict.update({"player_team" : playerTeam})
        
        playerPosPriceStringArray = (htmlContent.find("p", {"class":"player-pos"}).get_text()).strip()    
        playerPosPriceStringArray = playerPosPriceStringArray.split("|")
        
        playerPosPriceStringArray[0] = playerPosPriceStringArray[0].split()[0]
        playerPosPriceStringArray[1] = playerPosPriceStringArray[1].split()[-1]
        
        playerPos = (playerPosPriceStringArray[0])
        self.generalFantasyAttrDict.update({"player_pos" : playerPos})
        playerPrice = playerPosPriceStringArray[1][0:-1]
        
        playerPrice = float(playerPrice) * 1000000 # converting to millions
        self.generalFantasyAttrDict.update({"player_price" : playerPrice})
        
        # getting if player is playing by asking for a needed class
        
        playerAvail = (htmlContent.find("i", {"class" : "playing"})) != None
        self.generalFantasyAttrDict.update({"player_avail" : str(playerAvail)})
            
        generalFantasyStatLabels = htmlContent.find_all("p", {"class" : "pl-stat-label"})
        
        for i in range(len(generalFantasyStatLabels)):
            generalFantasyStatLabels[i] = generalFantasyStatLabels[i].get_text()
        
        generalFantasyStats = htmlContent.find_all("p", {"class" : "pl-stat-data"})
        
        # replacing element references with their corresponding texts
        for i in range(len(generalFantasyStatLabels)):
            generalFantasyStats[i] = generalFantasyStats[i].get_text()
            
            generalFantasyStatLabels[i] = generalFantasyStatLabels[i].replace(" ", "_")
            generalFantasyStatLabels[i] = generalFantasyStatLabels[i].lower()
            
            # replacing current # round rank with just a generic name
            generalFantasyStatLabels[-2] = self.dictLabels[-2]
            
            if generalFantasyStatLabels[i] in self.floatLabels:
                # just manually calculating this value instead of using MLS database
                if generalFantasyStatLabels[i] == '$/point':
                    generalFantasyStats[i] = playerPrice / generalFantasyStats[2] # index 2 corresponds to points
                else:
                    generalFantasyStats[i] = float(generalFantasyStats[i])
            elif generalFantasyStatLabels[i] in self.intLabels:
                if generalFantasyStatLabels[i] == 'last_wk_fantasy_pts':
                    generalFantasyStats[i] = -1 # -1 will be interpreted as a NULL when loading into the database 
                else:
                    generalFantasyStats[i] = int(generalFantasyStats[i])
        
        # updating dictionary with label names and corresponding values
        for i in range(len(generalFantasyStatLabels)):
            self.generalFantasyAttrDict.update({generalFantasyStatLabels[i] : generalFantasyStats[i]})
            
        # now extracting player match data and storing it
        # gameTables[0] holds fixture, and gameTables[1] holds corresponding data
        tables = htmlContent.find_all("div", {"class": "table-body"})
        
        # getting all fixtures and fixture IDs
        roundIDs = tables[0].find_all("div", {"class" : "round-id"})
        opponents = tables[0].find_all("div", {"class" : "fixture-opponent"})
        points = tables[0].find_all("div", {"class" : "points"})
        
        
        # removing last row ('all' row) and getting text
        roundIDs = roundIDs[:-1]
        opponents = opponents[:-1]
        points = points[:-1]
        
        for i in range(len(roundIDs)):
            roundIDs[i] = (roundIDs[i].get_text()).strip()
            opponents[i] = (opponents[i].get_text()).strip()
            points[i] = (points[i].get_text()).strip()
        
        # getting associated values with elements and replacing them
        for i in range (len(roundIDs)):
            roundIDs[i] = int(roundIDs[i])
            
            tempOpponents = (opponents[i]).split("\n")
            opponents[i] = tempOpponents[1]
            
            # had to add a try-except statement since some of the players didn't have points posted
            try:
                points[i] = int(points[i])
            except:
                points[i] = 0
            
        # iterating through data rows, appending values
        # creating list via list comprehension with 25 arrays (for each data set) and 34 rows in each
        playerGameData = [[0 for x in range(34)] for y in range(25)]
        
        # now accessing second table's values, iterating through each row table
        rows = tables[1].find_all("div", {"class": "row-table"})
        rows.pop()
        
        # now using the rows to add values to the table
        for i in range(len(rows)):
            divsInRow = rows[i].find_all("div")
            
            for j in range(len(divsInRow)):
                # parsing out first paragraph's values in a row
                # https://www.geeksforgeeks.org/python-extract-numbers-from-string/
                parsedValue = (divsInRow[j].find("p")).get_text()
                temp = re.findall(r'\d+', parsedValue)
                res = list(map(int, temp))
                
                # in case there are no numbers
                if res == []:
                    parsedValue = '-'
                else:
                    parsedValue = res[0]
        
                playerGameData[j][i] = parsedValue
            
        self.gamesDF['round_id'] = roundIDs
        self.gamesDF['fixture_opponent'] = opponents
        self.gamesDF['points'] = points
        
        for i in range (len(playerGameData)):
            self.gamesDF[self.playerGameDataLabels[i]] = playerGameData[i]