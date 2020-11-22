from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import json
import os

opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
opt.add_argument("--start-maximized")
# Pass the argument 1 to allow and 2 to block
opt.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 1, 
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 1, 
    "profile.default_content_setting_values.notifications": 1 
  })

# driver = webdriver.Chrome(chrome_options=opt,service_log_path='NUL')
driver = None
URL = "https://teams.microsoft.com"

if(os.path.isfile('./creds.local.json')):
    credFile = open("./creds.local.json")
    CREDS = json.loads(credFile.read())
else:
    credFile = open("./creds.json")
    CREDS = json.loads(credFile.read())

driver = webdriver.Chrome(chrome_options=opt,service_log_path='NUL')
driver.get(URL)
WebDriverWait(driver,10000).until(EC.visibility_of_element_located((By.TAG_NAME,'body')))
currentUrl = driver.current_url
print(currentUrl)
if("login.microsoftonline.com" in currentUrl):
    time.sleep(1)
    emailinput = driver.find_element_by_name('loginfmt')
    emailinput.click()
    emailinput.send_keys(CREDS['email'])
    driver.find_element_by_id('idSIButton9').click()
    time.sleep(1)
    passwordinput = driver.find_element_by_id('i0118')
    passwordinput.click()
    passwordinput.send_keys(CREDS['passwd'])
    driver.find_element_by_id('idSIButton9').click()
    time.sleep(1)
    driver.find_element_by_id('idSIButton9').click()
    time.sleep(5)
    driver.find_element_by_class_name('use-app-lnk').click()
time.sleep(10)
driver.find_element_by_id('app-bar-ef56c0de-36fc-4ef8-b417-3d82ba9d073c').click()
time.sleep(35)
driver.find_element_by_name("Working Week").click()
driver.find_element_by_name('Day').click()
time.sleep(1)
while True:
    elements  = driver.find_elements_by_class_name('node_modules--msteams-bridges-components-calendar-event-card-dist-es-src-renderers-event-card-renderer-event-card-renderer__cardBody--1kiA0')
    for els in elements:
        els.click()
        subject = driver.find_element_by_class_name('node_modules--msteams-bridges-components-calendar-grid-dist-es-src-renderers-peek-renderer-peek-meeting-header-peek-meeting-header__subject--24TzV')
        if "Canceled" not in subject.text :
            timestring = driver.find_element_by_class_name('node_modules--msteams-bridges-components-calendar-grid-dist-es-src-renderers-peek-renderer-peek-meeting-header-peek-meeting-header__date--3K2O_').text
            if "-" in timestring:
                timearray = timestring.split(' - ')
                startdatetime = datetime.strptime(timearray[0],'%d %b %Y %H:%M')
                endtime = datetime.strptime(startdatetime.strftime('%d %b %Y')+" "+timearray[1],"%d %b %Y %H:%M")
                if(datetime.now() > startdatetime and datetime.now() < endtime):
                    joinbutton = driver.find_element_by_class_name('node_modules--msteams-bridges-components-calendar-grid-dist-es-src-renderers-peek-renderer-peek-meeting-header-peek-meeting-header__joinButton--3G-er')
                    joinbutton.click()
                    time.sleep(5)
                    mutebutton = driver.find_element_by_id('preJoinAudioButton')
                    mutebutton.click()
                    time.sleep(1)
                    driver.find_element_by_xpath('//*[@data-tid="prejoin-join-button"]').click()
                    difference = (startdatetime - endtime)
                    nowtostartfidd = (startdatetime - datetime.now())
                    differencesec = difference.total_seconds - nowtostartfidd.total_seconds
                    time.sleep(int(differencesec))
                    driver.find_element_by_id('hangup-button').click()
                    time.sleep(10)
                    driver.find_element_by_id('app-bar-ef56c0de-36fc-4ef8-b417-3d82ba9d073c').click()
                    time.sleep(35)
                    driver.find_element_by_name("Working Week").click()
                    driver.find_element_by_name('Day').click()
                    time.sleep(60)
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(0.5)