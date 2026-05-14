from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# OPEN CHROME
driver = webdriver.Chrome()

# OPEN WEBSITE
driver.get("http://localhost:5500/index.html")

# WAIT PAGE LOAD
time.sleep(10)


print("Test Passed")

# CLOSE BROWSER
driver.quit()