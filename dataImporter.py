from selenium import webdriver
from selenium.webdriver.common.by import By

# Fantasy IDs correspond to the ID that the MLS Fantasy Website assigned to it
playerFantasyIDs = []

email = input("Enter your MLS Fantasy email: ")
password = input("Enter your MLS Fantasy password: ")

driver = webdriver.Firefox()
driver.get("https://fantasy.mlssoccer.com/#login_gigya")

# https://stackoverflow.com/questions/27112731/selenium-common-exceptions-nosuchelementexception-message-unable-to-locate-ele

driver.maximize_window() # For maximizing window

# tells the driver to wait for the page to load so we can properly extract elements
driver.implicitly_wait(5) 

# sending password and email and logging into MLS Fantasy
emailInput = driver.find_element(By.ID, "gigya-textbox-141263563588013010")
emailInput.send_keys(email)
passwordInput = driver.find_element(By.CLASS_NAME, "gigya-input-password")
passwordInput.send_keys(password)
loginButton = driver.find_element(By.CLASS_NAME, "gigya-input-submit")
loginButton.click()

# now getting Stats Centre webpage and clicking load more (a maximum of) 20 times to make sure we're getting all the needed players
driver.get("https://fantasy.mlssoccer.com/#stats-center")

for i in range(20):
    driver.implicitly_wait(1)
    try:
        loadMoreButton = driver.find_element(By.CLASS_NAME, "load-more")
    # once we the load button disappears (no more players to load)
    except Exception:
        break  
        
    loadMoreButton.click()

# now getting all player IDs
driver.implicitly_wait(5) 

# only retrieves players currently on screen (have to traverse through page)
playersRows = driver.find_elements(By.CLASS_NAME, "js-player-modal")

for i in playersRows:
    playerFantasyIDs.append(int(i.get_attribute('data-player_id')))

"""
Extracting all MLS Fantasy IDs, then will search MLS website for each players data (given fantasy ID), and then put it in a database.

Might want to log out of website later.
"""