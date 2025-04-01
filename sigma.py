from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
import base64
import time
import os
import re

def scrollToBottom():
    lastHeight = driver.execute_script('return document.body.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(3)
        newHeight = driver.execute_script('return document.body.scrollHeight')
        try:
            driver.find_element(By.CSS_SELECTOR, ".YstHxe input").click()
            time.sleep(3)
        except:
            pass
        if newHeight == lastHeight:
            break
        lastHeight = newHeight

query = "ripe single banana"
dirName = "ripe-banana"
imgCount = 200

cService = webdriver.ChromeService(executable_path="C:\\Users\\User\\chromedriver-win64\\chromedriver.exe")
chromeExecutablePath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
chromeOptions = Options()
chromeOptions.binary_location = chromeExecutablePath
driver = webdriver.Chrome(service=cService, options=chromeOptions)
driver.maximize_window()
driver.get('https://images.google.com/')
box = driver.find_element(By.NAME, "q")
box.send_keys(query)
box.send_keys(Keys.ENTER)

scrollToBottom()

if not os.path.exists(dirName):
    os.makedirs(dirName)

i = 0
imgIndex = 1
imgArr = driver.find_elements(By.CLASS_NAME, 'YQ4gaf')
print(f"Found {len(imgArr)} elements!")

while imgIndex <= imgCount:
    imgElement = imgArr[i+5]
    imgSrc = imgElement.get_attribute("src")
    
    if imgSrc:
        try:
            width = int(imgElement.get_attribute("naturalWidth"))
            height = int(imgElement.get_attribute("naturalHeight"))
            
            if width < 150 or height < 150:
                print(f"Skipping small image {width}x{height}")
                i += 1
                continue
            
            if imgSrc.startswith("https://encrypted-tbn0.gstatic.com/"):
                imgData = requests.get(imgSrc).content
            else:
                srcSeg = re.split(":|;|,", imgSrc)
                ext = srcSeg[1].split('/')[1]
                if not ext == "jpeg": 
                    i += 1
                    continue
                imgData = base64.b64decode(srcSeg[3])
            
            imgName = f"{dirName}/img-{imgIndex}.jpeg"
            with open(imgName, "wb") as f:
                f.write(imgData)
            print(f"{imgName} successfully written!")
            imgIndex += 1
        except Exception as e:
            print(f"Can't write!!!!: error {e} {imgSrc}")
    i += 1

driver.close()
