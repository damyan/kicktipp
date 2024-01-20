#!/usr/bin/env python3
"""Implements tipps auto-submitting on kicktipp.com"""

# import random
import subprocess
import sys
import time
import yaml

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

BASE_URL = "https://www.kicktipp.co.uk"
COMMUNITY_URL = "cominghome2020"
ADD_TIPPS_URL = "spielleiter/tippsnachtragen"
NUMBER_MATCHDAYS = 38
TIPPER_ID = "46952968"
TIPP_SAISON_ID = "1670602"
CREDS_FILE = "creds-secret.yaml"

def init_web_driver():
    """Initialize web driver"""
    service = Service()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(BASE_URL + "/info/profile/login")
    driver.implicitly_wait(0.5)

    return driver

def get_creds() -> tuple[str, str]:
    """Decrypt credentials with SOPS

    return(string): username, if successfully decrypted, None else
    return(string): password, if successfully decrypted, None else
    """
    try:
        result = subprocess.run(['sops', '-d', CREDS_FILE],
                                capture_output=True,
                                text=True)
    except:
        return None, None

    creds = yaml.safe_load(result.stdout)

    return creds['user'], creds['pass']

def login(driver):
    """Login to web interface"""
    login_user, login_pass = get_creds()

    login_user_form = driver.find_element(by=By.ID, value="kennung")
    login_user_form.send_keys(login_user)

    login_pass_form = driver.find_element(by=By.ID, value="passwort")
    login_pass_form.send_keys(login_pass)

    submit_button = driver.find_element(by=By.NAME, value="submitbutton")
    submit_button.click()

# table = driver.find_element(by=By.ID, value="tippsnachtragenSpiele")
#for cell in table.find_elements(by=By.XPATH, value="//input[@inputmode='numeric']"):
    # rand = random.randint(0,9)
    # cell.clear()
    # cell.send_keys(rand)

def make_tipps_2_1(driver):
    """Loop through all matchdays and submit results 2:1 for the bot"""
    for i in range(NUMBER_MATCHDAYS+1):
        driver.get(
            f"{BASE_URL}/{COMMUNITY_URL}/{ADD_TIPPS_URL}?tipperId={TIPPER_ID}&tippsaisonId={TIPP_SAISON_ID}")
        driver.get(f"{BASE_URL}/{COMMUNITY_URL}/{ADD_TIPPS_URL}?tipperId={TIPPER_ID}")
        driver.get(f"{BASE_URL}/{COMMUNITY_URL}/{ADD_TIPPS_URL}?tipperId={TIPPER_ID}&tippsaisonId={TIPP_SAISON_ID}&spieltagIndex="+str(i))
        for cell in driver.find_elements(by=By.XPATH, value="//input[contains(@name, 'heimTippString')]"):
            cell.clear()
            cell.send_keys(2)
        for cell in driver.find_elements(by=By.XPATH, value="//input[contains(@name, 'gastTippString')]"):
            cell.clear()
            cell.send_keys(1)
        time.sleep(2)

        submit_button = driver.find_element(by=By.NAME, value="submitbutton")
        submit_button.click()
        time.sleep(3)

def main() -> int:
    """Entry point"""
    driver = init_web_driver()
    login(driver)
    make_tipps_2_1(driver)

    time.sleep(3)
    driver.quit()

if __name__ == '__main__':
    sys.exit(main())
