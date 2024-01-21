#!/usr/bin/env python3
"""Implements tips auto submitting on kicktipp.com"""

import logging
import random
import subprocess
import sys
import time
import yaml

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

BASE_URL = "https://www.kicktipp.co.uk"
COMMUNITY_URL = "cominghome2020"
ADD_TIPS_URL = "spielleiter/tippsnachtragen"
NUMBER_MATCHDAYS = 38
TIPPER_ID_2_1_BOT = "46952968"   # 2:1 bot
TIPPER_ID_7_6_BOT = "50360538"   # random bot
TIPP_SAISON_ID = "1670602"
CREDS_FILE = "creds-secret.yaml"

RANDOM_RESULTS = []

logger = logging.getLogger("")

def init_logging():
    """Init logging module"""
    log_level = logging.INFO
    logger.setLevel(log_level)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

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
                                check=True,
                                text=True)
    except FileNotFoundError as fnfe:
        print("Install sops first: ", fnfe)
        sys.exit(1)
    except subprocess.CalledProcessError as cpe:
        print("Could not decrypt credential file: ", cpe, cpe.stderr)
        sys.exit(1)
    except: # pylint: disable=bare-except
        sys.exit(1)

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

def init_global_random_array():
    """Initialize random results array

    distrbution:
    27% - 1    goals
    20% - 2    goals
    15% - 0,3  goals
    10% - 4    goals
    5%  - 5    goals
    3%  - 6,7  goals
    1%  - 8,9  goals
    """
    global RANDOM_RESULTS
    RANDOM_RESULTS = RANDOM_RESULTS + [0] * 15
    RANDOM_RESULTS = RANDOM_RESULTS + [1] * 27
    RANDOM_RESULTS = RANDOM_RESULTS + [2] * 20
    RANDOM_RESULTS = RANDOM_RESULTS + [3] * 15
    RANDOM_RESULTS = RANDOM_RESULTS + [4] * 10
    RANDOM_RESULTS = RANDOM_RESULTS + [5] * 5
    RANDOM_RESULTS = RANDOM_RESULTS + [6] * 3
    RANDOM_RESULTS = RANDOM_RESULTS + [7] * 3
    RANDOM_RESULTS = RANDOM_RESULTS + [8] * 1
    RANDOM_RESULTS = RANDOM_RESULTS + [9] * 1

def make_tips_2_1(driver):
    """Loop through all matchdays and submit results 2:1 for 2_1_bot"""
    ext_url=f"{BASE_URL}/{COMMUNITY_URL}/{ADD_TIPS_URL}?tipperId={TIPPER_ID_2_1_BOT}"
    for i in range(NUMBER_MATCHDAYS):
        match_day = i+1
        driver.get(f"{ext_url}&tippsaisonId={TIPP_SAISON_ID}")
        driver.get(f"{ext_url}")
        driver.get(f"{ext_url}&tippsaisonId={TIPP_SAISON_ID}&spieltagIndex="+str(match_day))

        for cell in driver.find_elements(by=By.XPATH,
                                         value="//input[contains(@name, 'heimTippString')]"):
            cell.clear()
            cell.send_keys(2)
        for cell in driver.find_elements(by=By.XPATH,
                                         value="//input[contains(@name, 'gastTippString')]"):
            cell.clear()
            cell.send_keys(1)
        time.sleep(2)

        submit_button = driver.find_element(by=By.NAME, value="submitbutton")
        submit_button.click()
        logger.info("Submitted tips for match day %d/%d",
                    match_day,
                    NUMBER_MATCHDAYS)
        time.sleep(3)

def make_random_tips(driver):
    """Loop through all matchdays and submit random results for 7_6_bot"""
    ext_url=f"{BASE_URL}/{COMMUNITY_URL}/{ADD_TIPS_URL}?tipperId={TIPPER_ID_7_6_BOT}"
    for i in range(NUMBER_MATCHDAYS):
        match_day = i+1
        driver.get(f"{ext_url}&tippsaisonId={TIPP_SAISON_ID}")
        driver.get(f"{ext_url}")
        driver.get(f"{ext_url}&tippsaisonId={TIPP_SAISON_ID}&spieltagIndex="+str(match_day))

        table = driver.find_element(by=By.ID, value="tippsnachtragenSpiele")
        for cell in table.find_elements(by=By.XPATH, value="//input[@inputmode='numeric']"):
            rand = random.randint(0, 99)
            cell.clear()
            cell.send_keys(RANDOM_RESULTS[rand])
        time.sleep(2)

        submit_button = driver.find_element(by=By.NAME, value="submitbutton")
        submit_button.click()
        logger.info("Submitted tips for match day %d/%d",
                    match_day,
                    NUMBER_MATCHDAYS)
        time.sleep(3)

def main() -> int:
    """Entry point"""
    init_logging()
    logger.info("Starting auto recording")

    try:
        driver = init_web_driver()
        logger.info("Web driver initialized")

        login(driver)
        logger.info("Got web credentials")

        random_bot = True
        if random_bot:
            init_global_random_array()
            logger.info("Random results generated")

            make_random_tips(driver)
            logger.info("Auto tipping 'random' performed")
        else:
            make_tips_2_1(driver)
            logger.info("Auto tipping '2:1' performed")

        time.sleep(3)
        logger.info("Success")
    except: # pylint: disable=bare-except
        logger.error("Failed")
    finally:
        if driver:
            driver.quit()
        logger.info("Exiting gracefully")

if __name__ == '__main__':
    sys.exit(main())
