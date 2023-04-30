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
        self.dateSubstring = str(date.today()) + "_data"
        self.dataFolder = "./" + self.dateSubstring
        
        try:
            os.mkdir(self.dataFolder)
        # just preventing program from breaking whenever the folder has already been created
        except:
            pass
            # FIXME will need to remove files from here
        
    # extracts the MLS Fantasy website IDs of the players
    
    # FIXME -- use Beautifulsoup to extract IDs, will be faster and will consistently get all the players
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

        print("Player rows " + str(playersRows))

        for i in playersRows:
            self.fantasyPlayerIDs.append(int(i['data-player_id']))
            
    # extracts player IDs from a given webpage and returns a dictionary, and a Pandas data frame that contains game info
    def extractPlayerFantasyData(self):
        htmlContent = BeautifulSoup(self.driver.page_source, 'html.parser')
        player = PlayerData()
        parsedCorrectly = False # to handle errors with page loading
        
        
        # will wait an additional period of time if there is an error with parsing
        # temporary solution before coming up with more elegant solution
        while not parsedCorrectly:
            try:
                player.parseData(htmlContent)
                parsedCorrectly = True
            except Exception:
                print("Did not parse correctly. Waiting 0.5 seconds more for page to load.")
                time.sleep(0.5)
            
        return player
            
    # calls on needed functions to get all our MLS Fantasy data  
    def extractMLSFantasyData(self, email, password) -> None:
        self.extractFantasyIDs(email, password)
        
        for i in self.fantasyPlayerIDs:
            fantasyData.driver.get("https://fantasy.mlssoccer.com/#stats-center/player-profile/" + str(i)) 
            time.sleep(0.5)
            
            player = self.extractPlayerFantasyData()
            
            # writing individual file player data
            fptr = open(self.dateSubstring + "\\" + str(i) + "$" + self.dateSubstring + ".csv", "w")
            player.gamesDF.to_csv(fptr)
            fptr.close()
            
            self.generalTable.appendListEntry(i, player.generalFantasyAttrDict)
    
        # now writing general table to a file after appending all the other data
        generalDF = self.generalTable.createDF()
        fptr = open(self.dateSubstring + "\\" + "general$" + self.dateSubstring + ".csv", "w")
        generalDF.to_csv(fptr)
        fptr.close()
            
if __name__ == "__main__":
    email = input("Enter your MLS Fantasy Account email: ")
    password = getpass("Enter your MLS Fantasy Account password (won't display your input): ")
    
    
    fantasyData = DataImporter()  
    
    start = time.time()
    fantasyData.extractMLSFantasyData(email, password)
    end = time.time()
    
    totalTime = end - start
    
    print("Parsed %s players in %s seconds." % (str(len(fantasyData.fantasyPlayerIDs)), str(totalTime)))