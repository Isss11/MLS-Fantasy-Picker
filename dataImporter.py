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

class DataImporter:
    def __init__(self) -> None:
        self.fantasyPlayerIDs = []
        self.generalTable = GeneralData()
        self.dateSubstring = "_" + str(date.today()) + "data"
        
    # extracts the MLS Fantasy website IDs of the 
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

        htmlContent = BeautifulSoup(self.driver.page_source, 'html.parser')
        player = PlayerData()
        
        player.parseData(htmlContent)
            
        return player
            
    # calls on needed functions to get all our MLS Fantasy data  
    def extractMLSFantasyData(self, email, password) -> None:
        self.extractFantasyIDs(email, password)
        
        for i in self.fantasyPlayerIDs:
            fantasyData.driver.get("https://fantasy.mlssoccer.com/#stats-center/player-profile/" + str(i)) 
            time.sleep(0.25)
            player = self.extractPlayerFantasyData()
            
            # writing individual file player data
            fptr = open(str(i) + self.dateSubstring + ".csv", "w")
            player.gamesDF.to_csv(fptr)
            fptr.close()
            
            self.generalTable.appendListEntry(i, player.generalFantasyAttrDict)
    
        # now writing general table to a file after appending all the other data
        generalDF = self.generalTable.createDF()
        fptr = open("general" + self.dateSubstring + ".csv", "w")
        generalDF.to_csv(fptr)
        fptr.close()
        
        
            
if __name__ == "__main__":
    email = input("Enter your MLS Fantasy Account email: ")
    password = getpass("Enter your MLS Fantasy Account password (won't display your input): ")
    
    
    fantasyData = DataImporter()  
    fantasyData.extractMLSFantasyData(email, password)