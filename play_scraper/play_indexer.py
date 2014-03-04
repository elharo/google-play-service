import workerpool
import ApplicationIndexer

__author__ = 'Grainier Perera'


def process_url(url):
    indexer = ApplicationIndexer(url)
    indexer.run()
    pass


def main():
    urls = [
        'https://play.google.com/store/apps/collection/topselling_paid',
        'https://play.google.com/store/apps/collection/topgrossing',
        'https://play.google.com/store/apps/collection/topselling_new_paid',
        'https://play.google.com/store/apps/category/GAME/collection/topgrossing',
        'https://play.google.com/store/apps/category/GAME/collection/topselling_paid',
        'https://play.google.com/store/apps/category/GAME/collection/topselling_new_paid',
        'https://play.google.com/store/apps/collection/editors_choice',
    ]

    # Make a pool, five threads
    pool = workerpool.WorkerPool(size=5)

    # Perform the mapping
    pool.map(process_url, urls)

    # Send shutdown jobs to all threads, and wait until all the jobs have been completed
    pool.shutdown()
    pool.wait()
    pass

main()