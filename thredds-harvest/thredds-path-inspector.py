# python3
# takes 1.5 minute to run

import lib.siphon_ext
from siphon.catalog import TDSCatalog, Dataset

import urllib.request
import re
import pathlib

from threading import Thread, Lock
from queue import Queue, Empty
# from concurrent.futures.thread import ThreadPoolExecutor



MAX_THREADS = 30
INDEX_FILE = 'indexes/20180614-refs'
with open(INDEX_FILE, "w") as f:
    f.write("")


lock = Lock()
queue = Queue(maxsize=0)


class Scraper(Thread): 
    def __init__(self, queue): 
        Thread.__init__(self)
        self._queue = queue 

    def record_ref(self, text):
        print(text)
        with lock:
            with open(INDEX_FILE, "a") as f:
                f.write(text + "\n")


    def inspect_refs(self, cat, base_ref):
        for ref_name in cat.catalog_refs.keys():
            if re.search(r"2018.*06.*14", ref_name):
                # todays catalog
                self.record_ref(base_ref + ref_name)
                return
            elif re.search(r"2018.*\d\d.*\d\d", ref_name):
                # previous days catalog
                next
            else:
                c2 = cat.catalog_refs[ref_name].follow()
                c2_base_ref = base_ref + ref_name + "/"
                self._queue.put((c2, c2_base_ref), True)

    
    def run(self):
        while True:
            try:
                # print(self._queue.qsize())
                cat, base_ref = self._queue.get(timeout=2) 
                self.inspect_refs(cat, base_ref)
            except Empty:
                return
            except Exception as e:
                print("REF ERROR %s " % (cat.catalog_url))
                print(e)
            self._queue.task_done()





cat = TDSCatalog('http://thredds.ucar.edu/thredds/catalog.xml')#.follow_refs('Forecast Model Data', 'GEFS Members - Analysis')

queue.put((cat, "/"))
workers = []
for _ in range(MAX_THREADS):
    worker = Scraper(queue)
    worker.start()
    workers.append(worker)

queue.join()

