__author__ = 'Grainier Perera'
import pickle
import redis
from multiprocessing import Pool
from util.indexer import ApplicationIndexer
from util.scraper import ApplicationScraper

application_index_prefix = 'application_index:'
redis_host = 'localhost'
redis_port = '6379'


def process_url(url):
    app_indexer = ApplicationIndexer(url)
    app_indexer.run()
    pass


def scrape_application(application_id):
    r_server = redis.Redis(redis_host, redis_port)
    serialized_application_raw_data = r_server.get(application_id)
    application_raw_data = pickle.loads(serialized_application_raw_data)

    app_id = application_raw_data['app_id']
    app_url = application_raw_data['app_url']

    application_key = application_index_prefix + app_id
    scraper = ApplicationScraper()
    application = scraper.scrape(app_id, app_url)

    r_server.set(application_key, application)
    r_server.srem('not_updated_applications', application_key)
    r_server.shutdown()
    pass


def main():
    application_index_prefix = 'application_index:'
    r_server = redis.Redis(redis_host, redis_port)
    existing_app_indexes = r_server.keys(application_index_prefix + '*')
    for existing_index in existing_app_indexes:
        r_server.sadd('not_updated_applications', existing_index)
        pass

    # Process the urls list
    urls = [url.strip() for url in open("index_urls.txt").readlines()]  # Build our 'map' parameters
    pool = Pool(processes=2)  # start 2 worker processes
    pool.map_async(process_url, urls)  # Perform the mapping
    pool.close()
    pool.join()  # wait for the worker processes to exit
    
    # Get details of the application keys in the not_updated_applications SET
    not_updated_set_key = 'not_updated_applications'
    application_keys = r_server.smembers(not_updated_set_key)
    pool = Pool(processes=2)  # start 4 worker processes
    pool.map(scrape_application, application_keys)  # Perform the mapping
    pool.close()
    pool.join()  # wait for the worker processes to exit

    r_server.shutdown()
    pass


if __name__ == '__main__':
    main()
    pass
