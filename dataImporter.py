from selenium import webdriver
from selenium.webdriver.common.by import By

email = input("Enter your MLS Fantasy email: ")
password = input("Enter your MLS Fantasy password: ")

driver = webdriver.Firefox()
driver.get("https://fantasy.mlssoccer.com/#login_gigya")

# https://stackoverflow.com/questions/27112731/selenium-common-exceptions-nosuchelementexception-message-unable-to-locate-ele

driver.maximize_window() # For maximizing window

# tells the driver to wait 2 seconds for the page to load so we can properly extract elements
driver.implicitly_wait(5) 

# sending password and email and logging into MLS Fantasy
emailInput = driver.find_element(By.ID, "gigya-textbox-141263563588013010")
emailInput.send_keys(email)
passwordInput = driver.find_element(By.CLASS_NAME, "gigya-input-password")
passwordInput.send_keys(password)
loginButton = driver.find_element(By.CLASS_NAME, "gigya-input-submit")
loginButton.click()

# now getting Stats Centre webpage
driver.get("https://fantasy.mlssoccer.com/#stats-center")

"""
Current plan. Will load all player names from a file, and then will load their stats from the MLS website.

Or could get player data from MLS Fantasy website.
"""