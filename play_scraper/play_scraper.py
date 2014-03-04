import pickle

import redis

import workerpool
import ApplicationScraper

__author__ = 'grainier'

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
    pass


def main():
    # Make a pool, five threads
    pool = workerpool.WorkerPool(size=5)

    # Perform the mapping
    pool.map(scrape_application, application_keys)

    # Send shutdown jobs to all threads, and wait until all the jobs have been completed
    pool.shutdown()
    pool.wait()
    pass

main()
print('done')