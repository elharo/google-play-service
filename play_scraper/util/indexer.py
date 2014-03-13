__author__ = 'grainier'
from selenium.webdriver import Firefox, FirefoxProfile, PhantomJS
import time


class ApplicationIndexer(object):

    def __init__(self, url):
        self.url = url
        self.attempt = 0
        self.retries = 5
        self.acknowledgements = 2
        # self.fp = FirefoxProfile()
        # self.fp.set_preference('permissions.default.stylesheet', 2)                     # Disable css
        # self.fp.set_preference('permissions.default.image', 2)                          # Disable images
        # self.fp.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')    # Disable Flash
        pass

    def get_scraped_apps(self):
        applications = self.get_applications_in_page()
        return applications
        pass

    def get_applications_in_page(self):
        applications = []
        driver = None
        try:
            scroll_script = open("util/js_scripts/scroll_page.js").read()
            driver = PhantomJS(service_args=['--load-images=no'])
            # driver = Firefox(firefox_profile=self.fp)                                 # TODO : used in testing
            driver.get(self.url)
            driver.execute_script(scroll_script)

            acknowledge = 0
            done = False
            while not done:
                time.sleep(5)                                                           # Wait for the script
                scroll_finished = driver.execute_script("return window.scraperLoadCompleted")
                if scroll_finished:
                    if acknowledge == self.acknowledgements:
                        done = driver.execute_script("return window.scraperLoadCompleted")
                        pass
                    else:
                        acknowledge += 1
                        pass
                    pass
                pass

            product_matrix = driver.find_elements_by_class_name("card")
            for application in product_matrix:
                extracted_application = self.extract_application_data(application)
                if extracted_application['app_price'].lower() != "free":
                    applications.append(extracted_application)
                    pass
                pass
            pass
        except Exception as e:
            if driver is not None:
                driver.quit()
                pass

            if self.attempt < self.retries:
                self.attempt += 1
                time.sleep(10)
                print 'retry : url [ ' + self.url + ' ] + | attempt [ ' + str(self.attempt) + ' ]'
                applications = self.get_applications_in_page()
                pass
            else:
                print('fail : url [ ' + self.url + ' ] | error [ ' + str(e) + ' ]')
                pass
            pass
        return applications
        pass

    @staticmethod
    def extract_application_data(application):
        app_id = application.get_attribute("data-docid")                            # ID of the application
        card_content = application.find_element_by_class_name("card-content")
        app_url = card_content.find_element_by_xpath("a").get_attribute("href")     # URL of the application
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