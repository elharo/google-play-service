__author__ = 'grainier'
import pickle
import redis
from multiprocessing import Pool
from util.scraper import ApplicationScraper

scraped_applications = []
set_key = 'set_priority_x'
r_server = redis.Redis("localhost")
application_keys = r_server.smembers(set_key)


def scrape_application(application_id):
    serialized_application_raw_data = r_server.get(application_id)
    application_raw_data = pickle.loads(serialized_application_raw_data)

    app_id = application_raw_data['app_id']
    app_url = application_raw_data['app_url']

    scraper = ApplicationScraper()
    application = scraper.scrape(app_id, app_url)

    r_server.set('full_application_' + app_id, application)
    scraper = None
    pass


def main():
    pool = Pool(processes=4)  # start 4 worker processes
    pool.map(scrape_application, application_keys)  # Perform the mapping
    pool.close()
    pool.join()  # wait for the worker processes to exit
    pass

if __name__ == '__main__':
    main()
    pass