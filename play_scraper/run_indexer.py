__author__ = 'Grainier Perera'
import pickle
import redis
from properties import google_prop
from multiprocessing import Pool
from util.indexer import ApplicationIndexer
from util.scraper import ApplicationScraper

# http://stackoverflow.com/questions/20309170/selenium-and-phantomjs-error-cannot-connect-to-ghostdriver


def process_url(url):
    app_indexer = ApplicationIndexer(url)
    applications = app_indexer.get_scraped_apps()

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
    # r_server.shutdown()
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
    pool = Pool(processes=google_prop.parallel_processes)               # start 2 worker processes
    pool.map_async(process_url, urls)                                   # Perform the mapping
    pool.close()
    pool.join()                                                         # wait for the worker processes to exit

    """ Get details of the application keys in the not_updated_applications SET """
    application_keys = r_server.smembers(google_prop.not_updated_set_key)
    pool = Pool(processes=google_prop.parallel_processes)               # start 4 worker processes
    pool.map_async(scrape_application, application_keys)                # Perform the mapping
    pool.close()
    pool.join()                                                         # wait for the worker processes to exit

    r_server.save()                                                     # persist the dump
    # r_server.shutdown()                                               # shutdown redis server
    pass


if __name__ == '__main__':
    main()
    pass
