__author__ = 'grainier'
import os
import contextlib
from selenium.webdriver import Firefox, FirefoxProfile, Chrome, ChromeOptions
import time
import redis
import pickle


class ApplicationIndexer(object):

    def __init__(self, url):
        self.url = url
        self.fp = FirefoxProfile()
        self.fp.set_preference('permissions.default.stylesheet', 2)  # Disable css
        self.fp.set_preference('permissions.default.image', 2)  # Disable images
        self.fp.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')  # Disable Flash

        self.co = ChromeOptions()
        self.co.add_argument("start-maximized")
        pass

    def run(self):
        applications = self.get_applications_in_page()
        self.persist_in_redis(applications)
        pass

    def get_applications_in_page(self):
        applications = []
        # with contextlib.closing(Firefox(firefox_profile=self.fp)) as driver:
        with contextlib.closing(Chrome()) as driver:
            driver.get(self.url)
            driver.execute_script(
                "scraperLoadCompleted = false;" +
                "var interval = null, previousDocHeight = 0;" +
                "interval = setInterval(function () {" +
                "if (previousDocHeight < document.body.scrollHeight) {" +
                "window.scrollTo(0, Math.max(document.documentElement.scrollHeight," +
                "document.body.scrollHeight, document.documentElement.clientHeight));" +
                "document.getElementById('show-more-button').click();" +
                "previousDocHeight = document.body.scrollHeight;" +
                "} else {" +
                "clearInterval(interval);" +
                "scraperLoadCompleted = true;"
                "}" +
                "}, 5000);"
            )

            # Wait for the script to complete
            done = False
            while not done:
                time.sleep(2)
                done = driver.execute_script(
                    "return scraperLoadCompleted"
                )
                pass

            product_matrix = driver.find_elements_by_class_name("card")
            for application in product_matrix:
                applications.append(self.extract_application_data(application))
                pass
            pass
        return applications
        pass

    @staticmethod
    def extract_application_data(application):
        app_id = application.get_attribute("data-docid")  # ID of the application
        card_content = application.find_element_by_class_name("card-content")
        app_url = card_content.find_element_by_xpath("a").get_attribute("href")  # URL of the application
        price_container = card_content.find_element_by_class_name("price")
        app_price = price_container.find_element_by_xpath("span").text
        extracted_data = {
            'app_id': app_id,
            'app_url': app_url,
            'app_price': app_price
        }
        return extracted_data
        pass

    @staticmethod
    def persist_in_redis(applications):
        r_server = redis.Redis("localhost", "6379")
        for application in applications:
            if application['app_price'].lower() != "free":
                serialized_data = pickle.dumps(application)
                r_server.set(application['app_id'], serialized_data)
                ## TODO : Remove below line later
                r_server.sadd('set_priority_x', application['app_id'])
                pass
            pass
        pass