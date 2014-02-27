__author__ = 'Grainier Perera'

import os
import contextlib
from selenium.webdriver import Firefox, FirefoxProfile
import time
import redis
import pickle


def get_applications_in_page(url):
    applications = []
    fp = FirefoxProfile()
    fp.set_preference('permissions.default.stylesheet', 2)  # Disable css
    fp.set_preference('permissions.default.image', 2)  # Disable images
    fp.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')  # Disable Flash

    with contextlib.closing(Firefox(firefox_profile=fp)) as driver:
        driver.get(url)
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
            "}, 2000);"
        )

        # Wait for the script to complete
        done = False
        while not done:
            time.sleep(3)
            done = driver.execute_script(
                "return scraperLoadCompleted"
            )
            pass

        product_matrix = driver.find_elements_by_class_name("card")
        for application in product_matrix:
            applications.append(extract_application_data(application))
            pass
        pass
    return applications
    pass


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


def persist_in_redis(applications):
    r_server = redis.Redis("localhost", "6379")
    for application in applications:
        if application['app_price'].lower() != "free":
            serialized_data = pickle.dumps(application)
            r_server.set(application['app_id'], serialized_data)
            pass
        pass
    pass


def main():
    # applications = get_applications_in_page("https://play.google.com/store/apps/category/GAME/collection/topselling_paid")
    applications = get_applications_in_page("https://play.google.com/store/apps/collection/editors_choice")
    # applications = get_applications_in_page("https://play.google.com/store/apps/category/GAME/collection/topselling_paid")
    persist_in_redis(applications)


main()