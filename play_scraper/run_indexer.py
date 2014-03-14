__author__ = 'Grainier Perera'
import time
import logging
import pickle
import redis
from util.current_time import current_time_millisecond
from properties import google_prop
from multiprocessing import Pool
from util.indexer import ApplicationIndexer
from util.scraper import ApplicationScraper


def process_url(url):
    app_indexer = ApplicationIndexer(url)
    applications = app_indexer.get_scraped_apps()

    applications_count = len(applications)
    logging.info('URL [ ' + url + ' ] + | applications [ ' + str(applications_count) + ' ]')

    r_server = redis.Redis(google_prop.redis_host, google_prop.redis_port)
    for application in applications:
        application_key = google_prop.application_index_prefix + application['app_id']
        serialized_existing_application = r_server.get(application_key)

        if serialized_existing_application is not None:
            existing_application = pickle.loads(serialized_existing_application)
            existing_price_data = existing_application['price_data']
            existing_price_data[str(current_time_millisecond())] = application['app_price']
            application['price_data'] = existing_price_data
            pass
        else:
            price_data = {str(current_time_millisecond()): application['app_price']}
            application['price_data'] = price_data
            pass

        serialized_data = pickle.dumps(application)
        r_server.set(application_key, serialized_data)
        r_server.srem(google_prop.not_updated_set_key, application_key)
        pass
    pass


def scrape_application(application_id):
    r_server = redis.Redis(google_prop.redis_host, google_prop.redis_port)
    serialized_application_raw_data = r_server.get(application_id)
    application_raw_data = pickle.loads(serialized_application_raw_data)

    app_id = application_raw_data['app_id']
    app_url = application_raw_data['app_url']

    application_key = google_prop.application_index_prefix + app_id
    scraper = ApplicationScraper()
    application = scraper.scrape(app_id, app_url)

    r_server.set(application_key, application)
    r_server.srem(google_prop.not_updated_set_key, application_key)
    pass


def main():
    """ Move existing keys in to not updated set in order to keep track on updated keys """
    r_server = redis.Redis(google_prop.redis_host, google_prop.redis_port)
    existing_app_indexes = r_server.keys(google_prop.application_index_prefix + '*')
    for existing_index in existing_app_indexes:
        r_server.sadd(google_prop.not_updated_set_key, existing_index)
        pass

    """ Process the urls list """
    urls = [url.strip() for url in open("index_urls.txt").readlines()]  # Build our 'map' parameters
    pool_indexers = Pool(processes=google_prop.parallel_processes)      # start 2 worker processes
    pool_indexers.map(process_url, urls)                                # Perform the mapping
    pool_indexers.close()
    pool_indexers.join()                                                # wait for the worker processes to exit

    """ Get details of the application keys in the not_updated_applications SET """
    application_keys = r_server.smembers(google_prop.not_updated_set_key)
    pool_scrapers = Pool(processes=google_prop.parallel_processes)      # start 4 worker processes
    pool_scrapers.map(scrape_application, application_keys)             # Perform the mapping
    pool_scrapers.close()
    pool_scrapers.join()                                                # wait for the worker processes to exit

    r_server.save()                                                     # persist the dump
    pass


if __name__ == '__main__':
    logging.basicConfig(
        filename='logs/indexer_' + time.strftime("%Y:%m:%d:_%H:%M") + '.log',
        level=logging.INFO,
        format='%(asctime)s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p'
    )
    logging.info('start : ' + time.strftime("%Y:%m:%d:_%H:%M"))
    main()
    logging.info('finish : ' + time.strftime("%Y:%m:%d:_%H:%M"))

    pass
