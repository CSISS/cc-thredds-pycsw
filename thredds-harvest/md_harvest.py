# python3

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

OUTPUT_DIR = '../records/harvested'



NUM_THREADS = 10
lock = Lock()
queue = Queue(maxsize=0)



class Crawler(Thread): 
    def __init__(self, queue): 
        Thread.__init__(self)
        self._queue = queue

    def fix_data_id(self, fname, id):
        with open(fname) as f:
            text = f.read()

        text = re.sub(r"<gmd:fileIdentifier>[^\$]+?</gmd:fileIdentifier>",
            "<gmd:fileIdentifier><gco:CharacterString>%s</gco:CharacterString></gmd:fileIdentifier>" % id,
            text,
            re.MULTILINE)

        with open(fname, "w") as f:
            f.write(text)

    def download_iso(self, cat, ds):
        iso_md_url = ds.access_urls['ISO'] + \
            '?catalog=' + \
            urllib.parse.quote_plus(cat.catalog_url) + \
            '&dataset=' + \
            urllib.parse.quote_plus(ds.id)

        print("download: %s" + iso_md_url)
        dl_file = OUTPUT_DIR + "/" + ds.name + ".iso.xml"

        urllib.request.urlretrieve(iso_md_url, dl_file)
        self.fix_data_id(dl_file, ds.id) 


    def crawl_catalog(self, cat):
        try:
            for ref in cat.catalog_refs.values():
                self._queue.put(ref.follow(), True)
            for ds in cat.datasets.values():
                self.download_iso(cat, ds)

        except Exception as e:
            print("error processing catalog_url: %s" % cat.catalog_url)
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
                self.crawl_catalog(cat)
            except Empty:
                return

            self._queue.task_done()



# expand_thredds_iso_md('../records/generated/Level3_YUX_PTA_20180618_2058.nids.iso.xml', '../records/generated/Level3_YUX_PTA_20180618_2058.nids.iso.expanded.xml')
# exit(1)


cat = TDSCatalog('http://thredds.ucar.edu/thredds/catalog.xml').follow_refs('Satellite Data', 'Infrared (11 um)', 'WEST-CONUS_4km')

queue.put(cat)
workers = []
for _ in range(NUM_THREADS):
    worker = Crawler(queue)
    worker.start()
    workers.append(worker)

queue.join()


