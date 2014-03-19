__author__ = 'Grainier Perera'
from selenium.webdriver import Firefox, FirefoxProfile, PhantomJS, DesiredCapabilities
import time
from useragent_rotator import useragent
from proxy_rotator import proxy
from properties import google_prop


class ApplicationIndexer(object):

    def __init__(self, url, retries, acknowledgements):
        self.url = url
        self.attempt = 0
        self.retries = retries
        self.acknowledgements = acknowledgements

        # self.fp = FirefoxProfile()
        # self.fp.set_preference('permissions.default.stylesheet', 2)                     # Disable css
        # self.fp.set_preference('permissions.default.image', 2)                          # Disable images
        # self.fp.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')    # Disable Flash
        # self.fp.set_preference('general.useragent_rotator.override', self.get_random_user_agent())
        pass

    def get_scraped_apps(self, scroll_script):
        applications = self.get_applications_in_page(scroll_script)
        return applications
        pass

    def get_applications_in_page(self, scroll_script):
        applications = []
        driver = None
        try:
            desired_capabilities = dict(DesiredCapabilities.PHANTOMJS)
            desired_capabilities["phantomjs.page.settings.userAgent"] = useragent.get_random_agent(google_prop.user_agent_list_url)
            service_args = ['--load-images=no', '--proxy=%s' % (proxy.get_random_proxy(google_prop.proxy_list_url))]
            driver = PhantomJS(desired_capabilities=desired_capabilities, service_args=service_args)
            # driver = Firefox(firefox_profile=self.fp)
            driver.get(self.url)
            driver.execute_script(scroll_script)

            acknowledge = 0
            done = False
            while not done:
                scroll_finished = driver.execute_script("return window.scraperLoadCompleted")
                if scroll_finished:
                    if acknowledge == self.acknowledgements:
                        done = driver.execute_script("return window.scraperLoadCompleted")
                        pass
                    else:
                        acknowledge += 1
                        pass
                    pass
                else:
                    acknowledge = 0
                    pass
                time.sleep(5)  # Wait before retry
                pass

            product_matrix = driver.find_elements_by_class_name("card")
            for application in product_matrix:
                extracted_application = self.extract_application_data(application)
                # if extracted_application['app_price'] != -1:
                applications.append(extracted_application)
                #pass
                pass
            pass
        except Exception as e:
            if driver is not None:
                driver.quit()
                pass

            if self.attempt < self.retries:
                self.attempt += 1
                time.sleep(10)
                print 'retry : url [ ' + self.url + ' ] + | attempt [ ' + str(self.attempt) + ' ] | error [ ' + str(e) + ' ]'
                applications = self.get_applications_in_page(scroll_script)
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
        price_containers = card_content.find_elements_by_class_name('buy')
        author_url = application.find_element_by_class_name("subtitle").get_attribute("href")
        app_price = 0.0

        for price_container in price_containers:
            if '$' in price_container.text.lower():
                try:
                    app_price_string = price_container.text.replace('$', '')
                    app_price = float(app_price_string)
                    break
                    pass
                except Exception:
                    pass
                pass
            elif 'free' in price_container.text.lower():
                app_price = -1
                break
                pass
            pass

        extracted_data = {
            'app_id': app_id,
            'app_url': app_url,
            'app_price': app_price,
            'author_url': author_url
        }
        return extracted_data
        pass
    pass