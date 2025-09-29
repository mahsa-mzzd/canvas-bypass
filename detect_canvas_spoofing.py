#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

# Set Chrome options
options = Options()

# Set path to ChromeDriver using Service
service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=options)

# Open the local HTML test file
driver.get("http://localhost:8000/index.html")

# Wait for JavaScript to execute and for you to inspect the page
time.sleep(10)  # Increased delay to 10 seconds

# Get test result from the page title set by our JS
result_text = driver.title
spoofing_detected = "Detected" in result_text
print("Canvas fingerprinting protection active:", spoofing_detected)

# Close the browser
driver.quit()
