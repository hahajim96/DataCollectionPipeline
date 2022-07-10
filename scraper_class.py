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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select


class house_scraper:
    # TODO: STILL NEED TO RETHINK HOW THIS CLASS IS GOING TO BE STRUCTURED
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install())
    )  # create a drive class variable

    def __init__(self, URL):
        self.URL = URL

        self.driver.get(self.URL)  # move into the homepage
        self.driver.maximize_window()  # maximise window

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
            accept_cookies_button = WebDriverWait(house_scraper.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/div[2]/div[4]/div[2]/div/button")
                )
            )

            accept_cookies_button.click()
        except Exception as e:
            print("Cookies have not been accepted")
            print("Error message: {}".format(e))
        return house_scraper.driver

    def move_into_sold_house_page(self) -> webdriver.Chrome:
        """
        from the home page move into the sold house page

        Returns
        -------
        driver: webdriver.Chrome
            This driver is already in the rightmove webpage

        """
        self.driver.implicitly_wait(4)
        try:

            element_present = self.driver.find_element(By.LINK_TEXT, "House Prices")
            ActionChains(self.driver).move_to_element(element_present).perform()

            sub_sold_houses = self.driver.find_element(
                By.LINK_TEXT, "Sold house prices"
            )
            self.driver.implicitly_wait(2)
            ActionChains(self.driver).move_to_element(sub_sold_houses).click().perform()

            print("Moved into sold house page")
        except Exception as e:
            print("Unable to move into sold houses page")
            print(e)
        return self.driver

    def search_postcode(self, postcode: str) -> webdriver.Chrome:
        """
        search for postcode of sold houses

        Returns
        -------
        driver: webdriver.Chrome
            This driver is already in the rightmove webpage

        """
        time.sleep(3)
        try:
            postcodeDriver = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "searchLocation"))
            )

            postcodeDriver.send_keys(postcode)
            self.driver.implicitly_wait(1)
            postcodeDriver.send_keys(Keys.RETURN)
        except Exception as e:
            print("has not worked")
            print("Error message: {}".format(e))
        return self.driver

    def scrape_sold(self, class_to_scrape="propertyCard"):

        """
        Function to scrape website property details 

        Returns
        -------
        List: List of property details 

        """

        try:

            select = Select(
                self.driver.find_element(By.XPATH, '//*[@id="currentPage"]')
            )
            self.driver.implicitly_wait(2)

            select_type = Select(
                self.driver.find_element(
                    By.XPATH,
                    '//*[@id="content"]/div[2]/div[2]/div[4]/div[1]/div[3]/div[3]/div[2]/select',
                )
            )
            select_type.select_by_index(1)  # select only residential

            prop_list = []

            for page in range(0, len(select.options)):
                select.select_by_index(page)
                select_type.select_by_index(1)  # select only residential
                print("Scraping Page {}".format(page))

                prop = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located(
                        (By.CLASS_NAME, class_to_scrape)
                    )
                )

                prop_text = [details.text for details in prop]

                prop_list.extend(prop_text)
        except Exception as e:
            print("has not worked")
            print("Error message: {}".format(e))
        return prop_list


if __name__ == "__main__":
    # implement functions only when script is run
    cursor = house_scraper("https://www.rightmove.co.uk")
    cursor.load_and_accept_cookies()
    cursor.move_into_sold_house_page()
    cursor.search_postcode("G42")
    detail_list = cursor.scrape_sold()
