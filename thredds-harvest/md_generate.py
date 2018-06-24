import sys
assert sys.version_info >= (3,6)


from siphon.catalog import TDSCatalog, Dataset

from lib.thredds_md_editor import THREDDSMdEditor
import lib.siphon_ext


import urllib.parse
import urllib.request

import re
import pathlib
import datetime

import traceback


from threading import Thread, Lock
from queue import Queue, Empty

OUTPUT_DIR = '../records/generated'

today = datetime.date.today()
TODAY_RE = r"%d.*%d.*%d" % (today.year, today.month, today.day)
THIS_YEAR_RE = r"%d.*\d\d.*\d\d" % (today.year)


yesterday = datetime.date.today() - datetime.timedelta(days=1)
YESTERDAY_RE = r"%d.*%d.*%d" % (yesterday.year, yesterday.month, yesterday.day)
THIS_YEAR_RE = r"%d.*\d\d.*\d\d" % (yesterday.year)

OUTPUT_DIR = '../records/generated'

NUM_THREADS = 50
WORKER_TIMEOUT = 30 # wait n seconds for more work and then stop
catalog_refs_queue = Queue(maxsize=0)




class MDGenerator():
    def generate_for_catalog_dataset(cat, ds):
        try:
            url = cat.iso_md_url(ds)
            file = OUTPUT_DIR + "/" + THREDDSMdEditor.slugify(ds.name) + ".iso.xml"
            print("download", ds.id, url, file)

            urllib.request.urlretrieve(url, file)
            THREDDSMdEditor.expand_thredds_iso_md(file, file)
        except Exception as e:
            print(e)
            traceback.print_tb(e.__traceback__)
            print("[ERROR] generate_for_catalog_dataset. catalog_url=%s, ds.id=%s, url=%s, file=%s" % (cat.catalog_url, ds.id, url, file))


    def generate_for_catalog(cat):
        if len(cat.datasets) > 1:
            ds = cat.datasets[1]
            MDGenerator.generate_for_catalog_dataset(cat, ds)


def process_catalog_ref(cat_ref):
    try:
        if(re.search(YESTERDAY_RE, cat_ref.href)):
            # found yesterdays catalog
            print("follow", cat_ref.href)
            cat = cat_ref.follow()
            MDGenerator.generate_for_catalog(cat)
        elif(re.search(THIS_YEAR_RE, cat_ref.href)):
            # found a daily catalog that is not yesterdays
            print("skip", cat_ref.href)
        else:
            # found a catalog without a date
            print("follow", cat_ref.href)
            cat = cat_ref.follow()

            # process all children
            for child_cat_ref in cat.catalog_refs.values():
                # print("enqueue", child_cat_ref.href)
                catalog_refs_queue.put(child_cat_ref)

    except Exception as e:
        print("[ERROR] process_catalog_ref", cat_ref.href)
        print(e)
        traceback.print_tb(e.__traceback__)


    
def worker_loop():
    print('Worker started')
    while True:
        try:
            # print("...queue get. size =", catalog_refs_queue.qsize())
            cat_ref = catalog_refs_queue.get(timeout=WORKER_TIMEOUT)
            process_catalog_ref(cat_ref)
            catalog_refs_queue.task_done()
        except Empty:
            print('Worker timed out waiting for queue')
            return


cat_ref = TDSCatalog('http://thredds.ucar.edu/thredds/catalog.xml').catalog_refs['Radar Data']
# cat_ref = TDSCatalog('http://thredds.ucar.edu/thredds/catalog.xml').follow_refs('Radar Data', 'NEXRAD Level III Radar', 'PTA').catalog_refs['YUX']
# cat_ref = TDSCatalog('http://thredds.ucar.edu/thredds/catalog.xml').follow_refs('Radar Data', 'NEXRAD Level III Radar').catalog_refs['PTA']

catalog_refs_queue.put(cat_ref)
threads = []
for _ in range(NUM_THREADS):
    t = Thread(target=worker_loop)
    threads.append(t)
    t.start()

catalog_refs_queue.join()
