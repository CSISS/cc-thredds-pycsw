# import lib.siphon_ext

from lib.thredds_md_expander import expand_thredds_iso_md



from siphon.catalog import TDSCatalog, Dataset

def follow_refs(self, *names):
    catalog = self
    for n in names:
        catalog = catalog.catalog_refs[n].follow()
    return catalog

TDSCatalog.follow_refs = follow_refs


import urllib.parse
import urllib.request

import sys
import re
import pathlib
import datetime

import traceback


from threading import Thread, Lock
from queue import Queue, Empty

OUTPUT_DIR = '../records/generated'

today = datetime.date.today()
TODAY_RE = r"%d.*%d.*%d" % (today.year, today.month, today.day)
SAME_YEAR_RE = r"%d.*\d\d.*\d\d" % (today.year)


NUM_THREADS = 10
lock = Lock()
queue = Queue(maxsize=0)


class MDGenerator():
    def generate_for_catalog_dataset(cat, ds):
        iso_md_url = ds.access_urls['ISO'] + \
            '?catalog=' + \
            urllib.parse.quote_plus(cat.catalog_url) + \
            '&dataset=' + \
            urllib.parse.quote_plus(ds.id)


        dl_file = OUTPUT_DIR + "/" + ds.name + ".iso.xml"
        # expanded_file = OUTPUT_DIR + "/" + ds.name + ".iso.expanded.xml"
        
        # print("download: " + iso_md_url + " to: " + dl_file)
        urllib.request.urlretrieve(iso_md_url, dl_file)

        expand_thredds_iso_md(dl_file, dl_file)


    def generate_for_catalog(cat):
        for ref_name in cat.catalog_refs.keys():
            if(re.search(TODAY_RE, ref_name) or re.search(SAME_YEAR_RE, ref_name)):
                child_cat = cat.catalog_refs[ref_name].follow()
                # dont use the first dataset in the catalog, because it's often the one named 'latest'
                # which is different from all other datasets
                if len(child_cat.datasets) > 1:
                    ds = child_cat.datasets[1]
                    MDGenerator.generate_for_catalog_dataset(child_cat, ds)
                    return



class Crawler(Thread): 
    def __init__(self, queue): 
        Thread.__init__(self)
        self._queue = queue 

    def generate_aggregate_md_for_catalog(self, cat):
        print(cat.catalog_url)


    def inspect_refs(self, cat):
        for ref_name in cat.catalog_refs.keys():
            try:
                if re.search(TODAY_RE, ref_name):
                    # we found todays catalog. use that to generate a single aggregate metadata for all sibling catalogs
                    MDGenerator.generate_for_catalog(cat)
                    return
                elif re.search(SAME_YEAR_RE, ref_name):
                    # previous days catalog
                    next
                else:
                    child_cat = cat.catalog_refs[ref_name].follow()
                    self._queue.put(child_cat, True)
            except Exception as e:
                print("error processing catalog_url: %s with ref %s" % (cat.catalog_url, ref_name))
                exc_type, exc_value, exc_tb = sys.exc_info()
                tbe = traceback.TracebackException(
                    exc_type, exc_value, exc_tb,
                )
                print(''.join(tbe.format()))

                print('\nexception only:')
                print(''.join(tbe.format_exception_only()))

    
    def run(self):
        while True:
            try:
                # print(self._queue.qsize())
                cat = self._queue.get(timeout=2) 
                self.inspect_refs(cat)
            except Empty:
                return

            self._queue.task_done()



# expand_thredds_iso_md('../records/generated/Level3_YUX_PTA_20180618_2058.nids.iso.xml', '../records/generated/Level3_YUX_PTA_20180618_2058.nids.iso.expanded.xml')
# exit(1)


cat = TDSCatalog('http://thredds.ucar.edu/thredds/catalog.xml').follow_refs('Radar Data')

queue.put(cat)
workers = []
for _ in range(NUM_THREADS):
    worker = Crawler(queue)
    worker.start()
    workers.append(worker)

queue.join()
