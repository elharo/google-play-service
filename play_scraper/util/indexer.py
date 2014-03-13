from encodings.punycode import selective_find

__author__ = 'grainier'
import contextlib
from selenium.webdriver import Firefox, FirefoxProfile, PhantomJS
import time


# TODO : Firefox Driver should only be used in testing
class ApplicationIndexer(object):

    def __init__(self, url):
        self.url = url
        self.attempt = 0
        self.retries = 5
        self.fp = FirefoxProfile()
        self.fp.set_preference('permissions.default.stylesheet', 2)                     # Disable css
        self.fp.set_preference('permissions.default.image', 2)                          # Disable images
        self.fp.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')    # Disable Flash
        pass

    def get_scraped_apps(self):
        applications = self.get_applications_in_page()
        return applications
        pass

    def get_applications_in_page(self):
        applications = []
        try:
            # with contextlib.closing(Firefox(firefox_profile=self.fp)) as driver:
            with contextlib.closing(PhantomJS(service_args=['--load-images=no'])) as driver:
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

                done = False
                while not done:
                    # Wait for the script to complete
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
        except Exception as e:
            if self.attempt < self.retries:
                self.attempt += 1
                time.sleep(5)
                applications = self.get_applications_in_page()
            else:
                print 'retry : url [ ' + self.url + ' ] + | attempt [ ' + str(self.attempt) + ' ]'
            print('fail : url [ ' + self.url + ' ] | error [ ' + e + ' ]')
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