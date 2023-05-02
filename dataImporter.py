from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from getpass import getpass
from bs4 import BeautifulSoup
import pandas as pd
from playerData import PlayerData
from generalData import GeneralData
import time
from datetime import date
import os

class DataImporter:
    def __init__(self) -> None:
        self.fantasyPlayerIDs = []
        self.generalTable = GeneralData()
        self.date = str(date.today())
        self.dateSubstring = self.date + "_data"
        self.dataFolder = "./" + self.dateSubstring
        self.generalFileName = self.dateSubstring + "\\" + "general$" + self.dateSubstring + ".csv"
        self.playerDataSets = []
        
        try:
            os.mkdir(self.dataFolder)
        # just preventing program from breaking whenever the folder has already been created
        except:
            pass
            # FIXME will need to remove files from here
        
    # extracts the MLS Fantasy website IDs of the players
    
    def extractFantasyIDs(self, email, password) -> None:
        self.driver = webdriver.Chrome()
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

        # now getting all player IDs
        time.sleep(5) # FIXME temporary solution

        # using BeautifulSoup to retrieve rows
        htmlContent = BeautifulSoup(self.driver.page_source, 'html.parser')
        
        playersRows = htmlContent.find_all("a", {"class" : "player-name"})

        for i in playersRows:
            self.fantasyPlayerIDs.append(int(i['data-player_id']))
            
        # FIXME -- this has been created to speed up testing for other parts of program, will remove later
        self.fantasyPlayerIDs = self.fantasyPlayerIDs[0:20]
            
    # extracts player IDs from a given webpage and returns a dictionary, and a Pandas data frame that contains game info
    def extractPlayerFantasyData(self):
        htmlContent = BeautifulSoup(self.driver.page_source, 'html.parser')
        player = PlayerData()
        parsedCorrectly = False # to handle errors with page loading
        
        
        # will wait an additional period of time if there is an error with parsing
        # temporary solution before coming up with more elegant solution
        # while not parsedCorrectly:
        #     try:
        player.parseData(htmlContent)
                # parsedCorrectly = True
            # except Exception:
            #     print("Did not parse correctly. Waiting 0.5 seconds more for page to load.")
            #     time.sleep(0.5)
            
        return player
            
    # calls on needed functions to get all our MLS Fantasy data  
    def extractMLSFantasyData(self, email, password) -> None:
        # clearing current data sets
        self.playerDataSets = []
        self.generalDF = []
        self.fantasyPlayerIDs = []
        
        self.extractFantasyIDs(email, password)
        
        # save fantasy IDs to a file
        fptr = open(self.dateSubstring + "\\" + "fantasyIDs$" + self.date + "_data" + ".csv", "w")
    
        for i in self.fantasyPlayerIDs:
            fptr.write(str(i) + ", ")
            
        fptr.close()
        
        for i in self.fantasyPlayerIDs:
            fantasyData.driver.get("https://fantasy.mlssoccer.com/#stats-center/player-profile/" + str(i)) 
            time.sleep(0.5)
            
            player = self.extractPlayerFantasyData()
            
            # writing individual file player data
            # FIXME - has issues with permissions in some cases
            fptr = open(self.dateSubstring + "\\" + str(i) + "$" + self.dateSubstring + ".csv", "w")
            player.gamesDF.to_csv(fptr)
            fptr.close()
            
            self.generalTable.appendListEntry(i, player.generalFantasyAttrDict)
            self.playerDataSets.append(player)
    
        # now writing general table to a file after appending all the other data
        self.generalDF = self.generalTable.createDF()
        fptr = open(self.generalFileName, "w")
        self.generalDF.to_csv(fptr)
        fptr.close()
     
    # loads all data, both general and player specific data frames   
    def loadData(self, date):
        # reading ID data to get IDs
        fptr = open(date + "_data\\" + "fantasyIDs$" + date + "_data" + ".csv", "r")
        stringIDs = fptr.read().split(", ")
        fptr.close()
        stringIDs = stringIDs[0:-1]
        
        # resetting player IDs currently loaded, and appending IDs to array
        self.fantasyPlayerIDs = []
        
        for i in stringIDs:
            self.fantasyPlayerIDs.append(int(i))
            
        # load general data frame
        fptr = open(self.generalFileName, "r")
        self.generalDF = pd.read_csv(fptr)
        fptr.close()
            
        for i in range(len(self.fantasyPlayerIDs)):            
            # writing individual file player data
            fptr = open(date + "_data\\" + str(self.fantasyPlayerIDs[i]) + "$" + date + "_data" + ".csv", "r")
            
            player = PlayerData()
            player.gamesDF = pd.read_csv(fptr)
            
            for j in range(len(player.dictLabels)):
                player.generalFantasyAttrDict[player.dictLabels[j]] = self.generalDF.iloc[i][player.dictLabels[j]]
            
            fptr.close()
            
            self.playerDataSets.append(player)
if __name__ == "__main__":
    # email = input("Enter your MLS Fantasy Account email: ")
    # password = getpass("Enter your MLS Fantasy Account password (won't display your input): ")
    
    fantasyData = DataImporter()  
    
    fantasyData.loadData("2023-05-01")
    
    # start = time.time()
    # fantasyData.extractMLSFantasyData(email, password)
    # end = time.time()
    
    # totalTime = end - start
    
    # print("Parsed %s players in %s seconds." % (str(len(fantasyData.fantasyPlayerIDs)), str(totalTime)))
    
    