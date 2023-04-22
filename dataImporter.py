from selenium import webdriver
from selenium.webdriver.common.by import By
from getpass import getpass

class MLSData:
    def __init__(self) -> None:
        self.fantasyPlayerIDs = []
        
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
    # extracts player IDs from a given webpage and returns a dictionary
    def extractPlayerFantasyData(self):
        generalFantasyAttrDict = {}
        
        # getting data from tables
        playerName = (self.driver.find_element(By.CLASS_NAME, "profile-name")).text
        generalFantasyAttrDict.update({"player_name" : playerName})
        
        playerTeam = (self.driver.find_element(By.CLASS_NAME, "player-team")).text
        generalFantasyAttrDict.update({"player_team" : playerTeam})
        
        playerPosPriceStringArray = ((self.driver.find_element(By.CLASS_NAME, "player-pos")).text).split(" | ")
        
        playerPos = playerPosPriceStringArray[0]
        generalFantasyAttrDict.update({"player_pos" : playerPos})
        
        playerPrice = playerPosPriceStringArray[1]
        playerPrice = float(playerPrice[2:len(playerPrice) - 1])
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
        
        # updating dictionary with label names and corresponding values
        for i in range(len(generalFantasyStatLabels)):
            generalFantasyAttrDict.update({generalFantasyStatLabels[i] : generalFantasyStats[i]})
            
        return generalFantasyAttrDict
            
    # calls on needed functions to get all our MLS Fantasy data  
    def extractMLSFantasyData(self, email, password) -> None:
        self.extractFantasyIDs(email, password)
        
        for i in self.fantasyPlayerIDs:
            fantasyData.driver.get("https://fantasy.mlssoccer.com/#stats-center/player-profile/" + str(i))
            self.driver.implicitly_wait(1) 
            print(self.extractPlayerFantasyData())
        

if __name__ == "__main__":
    email = input("Enter your MLS Fantasy Account email: ")
    password = getpass("Enter your MLS Fantasy Account password (won't display your input): ")
    
    fantasyData = MLSData()  
    fantasyData.extractMLSFantasyData(email, password)