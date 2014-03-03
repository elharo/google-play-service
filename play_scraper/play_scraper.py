from ApplicationScraper import ApplicationScraper
import redis
import pickle
import workerpool

__author__ = 'grainier'

scraped_applications = []
set_key = 'set_priority_x'
r_server = redis.Redis("localhost")
application_keys = r_server.smembers(set_key)

for application_key in application_keys:
    serialized_application_raw_data = r_server.get(application_key)
    application_raw_data = pickle.loads(serialized_application_raw_data)

    app_id = application_raw_data['app_id']
    app_url = application_raw_data['app_url']

    scraper = ApplicationScraper()
    application = scraper.scrape(app_id, app_url)

    scraped_applications.append(application)
    pass

print('done')

def process_xls_sheets(path):
    xls_files = get_xls_files(path)
    xls_processed_data = get_xls_processed_data(xls_files)

    # Make a pool, five threads
    pool = workerpool.WorkerPool(size=5)

    # Perform the mapping
    pool.map(process_single_row, xls_processed_data)

    # Send shutdown jobs to all threads, and wait until all the jobs have been completed
    pool.shutdown()
    pool.wait()
    pass