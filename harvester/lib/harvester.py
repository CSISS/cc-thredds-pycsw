from threading import Thread
from queue import Queue, Empty
import traceback


class Harvester():
    def __init__(scraper, num_workers=20, queue_timeout=10):
        self.scraper = scraper
        self.num_workers = num_workers
        self.queue_timeout = queue_timeout

    def scrape_ref(self, ref):
        try:
            catalog = ref.follow()
            self.scraper.scrape_catalog(catalog)
        except Exception as e:
            print("[ERROR] scrape_ref", ref.href)
            print(e)
            traceback.print_tb(e.__traceback__)


    def worker_loop(self):
        while True:
            try:
                # print("...queue get. size =", catalog_refs_queue.qsize())
                catalog_ref = self.scraper.queue.get(timeout=self.queue_timeout)
                self.scrape_ref(catalog_ref)
                self.scraper.queue.task_done()
            except Empty:
                num_workers -= 1
                print('worker timed out')
                return

    def harvest(self, catalog_refs):
        for ref in catalog_refs:
            self.scraper.queue.put(ref)

        print("starting %d worker threads" % self.num_workers)
        self.threads = []
        for _ in range(self.num_workers):
            t = Thread(target=self.worker_loop)
            self.threads.append(t)
            t.start()

        self.scraper.queue.join()

