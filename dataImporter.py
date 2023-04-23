from selenium import webdriver
from selenium.webdriver.common.by import By
from getpass import getpass
import pandas as pd

class MLSData:
    def __init__(self) -> None:
        self.fantasyPlayerIDs = []
        self.floatLabels = ['player_price', 'avg_fantasy_pts', '3_wk_avg', '5_wk_avg', 'owned_by', '$/point']
        self.intLabels = ['games_played', 'total_fantasy_pts', 'last_wk_fantasy_pts', 'high_score', 'low_score', 'rd_8_rank', 'season_rank']
        
    # extracts the MLS Fantasy website IDs of the 
    def extractFantasyIDs(self, email, password) -> None:
        self.driver = webdriver.Firefox()
        self.driver.get("https://fantasy.mlssoccer.com/#login_gigya")

        # https://stackoverflow.com/questions/27112731/selenium-common-exceptions-nosuchelementexception-message-unable-to-locate-ele

        self.driver.maximize_window() # For maximizing window

        # tells the driver to wait for the page to load so we can properly extract elements
        self.driver.implicitly_wait(5) 

        # sending password and email and logging into MLS Fantasy
        emailInput = self.driver.find_element(By.ID, "gigya-textbox-141263563588013010")
        emailInput.send_keys(email)
        passwordInput = self.driver.find_element(By.CLASS_NAME, "gigya-input-password")
        passwordInput.send_keys(password)
        loginButton = self.driver.find_element(By.CLASS_NAME, "gigya-input-submit")
        loginButton.click()

        # now getting Stats Centre webpage and clicking load more (a maximum of) 20 times to make sure we're getting all the needed players
        self.driver.get("https://fantasy.mlssoccer.com/#stats-center")

        for i in range(20):
            self.driver.implicitly_wait(1)
            try:
                loadMoreButton = self.driver.find_element(By.CLASS_NAME, "load-more")
            # once we the load button disappears (no more players to load)
            except Exception:
                break  
                
            loadMoreButton.click()

        # now getting all player IDs
        self.driver.implicitly_wait(5) 

        # only retrieves players currently on screen (have to traverse through page)
        playersRows = self.driver.find_elements(By.CLASS_NAME, "js-player-modal")

        for i in playersRows:
            self.fantasyPlayerIDs.append(int(i.get_attribute('data-player_id')))
    # extracts player IDs from a given webpage and returns a dictionary, and a Pandas data frame that contains game info
    def extractPlayerFantasyData(self):
        generalFantasyAttrDict = {}
        gamesDF = pd.DataFrame()
        
        # getting data from tables
        playerName = (self.driver.find_element(By.CLASS_NAME, "profile-name")).text
        generalFantasyAttrDict.update({"player_name" : playerName})
        
        playerTeam = (self.driver.find_element(By.CLASS_NAME, "player-team")).text
        generalFantasyAttrDict.update({"player_team" : playerTeam})
        
        playerPosPriceStringArray = ((self.driver.find_element(By.CLASS_NAME, "player-pos")).text).split(" | ")
        
        playerPos = (playerPosPriceStringArray[0])[:-1]
        generalFantasyAttrDict.update({"player_pos" : playerPos})
        
        playerPrice = playerPosPriceStringArray[1]
        playerPrice = float(playerPrice[2:len(playerPrice) - 1]) * 1000000 # converting to millions
        generalFantasyAttrDict.update({"player_price" : playerPrice})
        
        # getting if player is playing by asking for a needed class
        try:
            self.driver.find_element(By.CLASS_NAME, "playing")
            playerAvail = True
        except Exception:
            playerAvail = False
        
        generalFantasyAttrDict.update({"player_avail" : str(playerAvail)})
            
        generalFantasyStatLabels = self.driver.find_elements(By.CLASS_NAME, "pl-stat-label")
        generalFantasyStats = self.driver.find_elements(By.CLASS_NAME, "pl-stat-data")
        
        # replacing element references with their corresponding texts
        for i in range(len(generalFantasyStatLabels)):
            generalFantasyStatLabels[i] = generalFantasyStatLabels[i].text
            generalFantasyStats[i] = generalFantasyStats[i].text
            
            generalFantasyStatLabels[i] = generalFantasyStatLabels[i].replace(" ", "_")
            generalFantasyStatLabels[i] = generalFantasyStatLabels[i].lower()
            
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
            generalFantasyAttrDict.update({generalFantasyStatLabels[i] : generalFantasyStats[i]})
            
        # now extracting player match data and storing it
        # gameTables[0] holds fixture, and gameTables[1] holds corresponding data
        gameTables = self.driver.find_elements(By.CLASS_NAME, "table-body")
        
        # getting all fixtures and fixture IDs
        roundIDs = gameTables[0].find_elements(By.CLASS_NAME, "round-id")
        opponents = gameTables[0].find_elements(By.CLASS_NAME, "fixture-opponent")
        points = gameTables[0].find_elements(By.CLASS_NAME, "points")
        
        # getting data from the actual statistics table
        dataRows = gameTables[1].find_elements(By.CLASS_NAME, 'row-table')
        dataRows.pop() # removing header row
        
        # revoing last row (overall row)
        roundIDs = roundIDs[:-1]
        opponents = opponents[:-1]
        points = points[:-1]
        
        # getting associated values with elements and replacing them
        for i in range (len(roundIDs)):
            roundIDs[i] = int(roundIDs[i].text)
            
            tempOpponents = (opponents[i].text).split("\n")
            opponents[i] = tempOpponents[1]
            
            points[i] = int(points[i].text)
            
        # iterating through data rows, appending values
        minutes = []
        goals = []
        assists = []
        cleanSheets = []
        penaltySaves = []
        penaltiesEarned = []
        penaltyMisses = []
        goalsAgainst = []
        saves = []
        yellowCards = []
        redCards = []
        ownGoals = []
        tackles = []
        passes = []
        keyPasses = []
        crosses = []
        bigChancesCreated = []
        clearances = []
        blockedPasses = []
        interceptions = []
        recoveredBalls = []
        errorLeadingToGoals = []
        ownGoalAssists = []
        shots = []
        wasFouled = []
        
        # array of arrays that holds the data for each specific game
        playerGameData = [minutes, goals, assists, cleanSheets, penaltySaves, penaltiesEarned, penaltyMisses, goalsAgainst, saves, yellowCards, 
                          redCards, ownGoals, tackles, passes, keyPasses, crosses, bigChancesCreated, clearances, blockedPasses, interceptions,
                          recoveredBalls, errorLeadingToGoals, ownGoalAssists, shots, wasFouled]
        
        playerGameDataLabels = ['minutes', 'goals', 'assists', 'clean-sheets', 'penalty-saves', 'penalties-earned', 'penalty-misses', 'goals-against', 'saves', 'yellow-cards', 
                          'red-cards', 'own-goals', 'tackles', 'passes', 'key-passes', 'crosses', 'big-chances-created', 'clearances', 'blocked-passes', 'interceptions',
                          'recovered-balls', 'error-leading-to-goals', 'own-goal-assists', 'shots', 'was-fouled']
        
        # iterating though each data row, appending values to playerGameData
        for i in range (len(dataRows)):
            # extracting all divs from with each 'row-table' element
            divs = dataRows[i].find_elements(By.TAG_NAME, "div")
            
            # going through each div in a given row, and appending all the values to each corresponding array element
            for j in range(len(divs)):
                # getting value and storing it in corresponding array (within first paragraph)
                statisticContainerElement = divs[j].find_element(By.TAG_NAME, "p")
                
                # getting the associated array and then appendign an element to it
                associatedArray = playerGameData[j]
                associatedArray.append(statisticContainerElement.text)
            
        gamesDF['round_id'] = roundIDs
        gamesDF['fixture_opponent'] = opponents
        gamesDF['points'] = points
        
        for i in range (len(playerGameData)):
            gamesDF[playerGameDataLabels[i]] = playerGameData[i]
            
        return generalFantasyAttrDict, gamesDF
            
    # calls on needed functions to get all our MLS Fantasy data  
    def extractMLSFantasyData(self, email, password) -> None:
        self.extractFantasyIDs(email, password)
        
        for i in self.fantasyPlayerIDs:
            fantasyData.driver.get("https://fantasy.mlssoccer.com/#stats-center/player-profile/" + str(i))
            self.driver.implicitly_wait(1) 
            playerFantasyDict, playerGamesDF = self.extractPlayerFantasyData()
            
            print(playerFantasyDict)
            print(playerGamesDF)
        

if __name__ == "__main__":
    email = input("Enter your MLS Fantasy Account email: ")
    password = getpass("Enter your MLS Fantasy Account password (won't display your input): ")
    
    fantasyData = MLSData()  
    fantasyData.extractMLSFantasyData(email, password)