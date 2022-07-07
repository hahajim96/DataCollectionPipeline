# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 14:23:37 2022

@author: hjimbrow
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time


class sold_house_scraper:
    # TODO: STILL NEED TO RETHINK HOW THIS CLASS IS GOING TO BE STRUCTURED
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install())
    )  # create a drive class variable

    def __init__(self, URL):
        self.URL = URL

        self.driver.get(self.URL)  # move into the homepage

    def load_and_accept_cookies(self) -> webdriver.Chrome:
        """
        Open right move and accept the cookies
        
        Returns
        -------
        driver: webdriver.Chrome
            This driver is already in the rightmove webpage
        """

        time.sleep(3)
        try:

            accept_cookies_button = self.driver.find_element_by_xpath(
                "/html/body/div[1]/div[2]/div[4]/div[2]/div/button"
            )
            accept_cookies_button.click()
            time.sleep(1)
        except:
            print("Cookies have been accepted")
            pass
        return self.driver

    def move_into_sold_house_page(self) -> webdriver.Chrome:
        """
        from the home page move into the sold house page

        Returns
        -------
        driver: webdriver.Chrome
            This driver is already in the rightmove webpage

        """

        try:
            sold_houses = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    By.XPATH,
                    '//*[@id="seo-globalHeader"]/div/div[1]/nav/div[4]/div/ul[1]/div/li[1]/a',
                )
            )

            sold_houses.click()
        except:
            print("moves into sold houses page")
