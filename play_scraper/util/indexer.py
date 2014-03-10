from properties import google_prop

__author__ = 'grainier'
import contextlib
from selenium.webdriver import Firefox, FirefoxProfile
import time
import redis
import pickle


class ApplicationIndexer(object):

    def __init__(self, url):
        # initialize ApplicationIndexer
        self.url = url
        self.fp = FirefoxProfile()
        self.fp.set_preference('permissions.default.stylesheet', 2)  # Disable css
        self.fp.set_preference('permissions.default.image', 2)  # Disable images
        self.fp.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')  # Disable Flash
        pass

    def run(self):
        applications = self.get_applications_in_page()
        self.persist_in_redis(applications)
        pass

    def get_applications_in_page(self):
        applications = []
        with contextlib.closing(Firefox(firefox_profile=self.fp)) as driver:
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
                "}, 4000);"
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

    def persist_in_redis(self, applications):
        r_server = redis.Redis(google_prop.redis_host, google_prop.redis_port)
        for application in applications:
            if application['app_price'].lower() != "free":
                application_key = google_prop.application_index_prefix + application['app_id']
                serialized_data = pickle.dumps(application)
                r_server.set(application_key, serialized_data)
                r_server.srem(google_prop.not_updated_set_key, application_key)
                pass
            pass
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
    pass