__author__ = 'Grainier Perera'
from multiprocessing import Pool
from util.indexer import ApplicationIndexer


def process_url(url):
    app_indexer = ApplicationIndexer(url)
    app_indexer.run()
    pass


def main():
    urls = [url.strip() for url in open("index_urls.txt").readlines()]  # Build our 'map' parameters
    pool = Pool(processes=2)  # start 2 worker processes
    pool.map_async(process_url, urls)  # Perform the mapping
    pool.close()
    pool.join()  # wait for the worker processes to exit
    pass


if __name__ == '__main__':
    main()
    pass
