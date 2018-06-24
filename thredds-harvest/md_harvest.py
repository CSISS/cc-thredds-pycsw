import sys
assert sys.version_info >= (3,6)


from siphon.catalog import TDSCatalog, Dataset

from lib.thredds_md_editor import THREDDSMdEditor
import lib.siphon_ext


import urllib.parse
import urllib.request
import unicodedata

import re
import pathlib
import datetime

import traceback


from threading import Thread, Lock
from queue import Queue, Empty



OUTPUT_DIR = '../records/harvested'

yesterday = datetime.date.today() - datetime.timedelta(days=1)
YESTERDAY_RE = r"%d.*%d.*%d" % (yesterday.year, yesterday.month, yesterday.day)
THIS_YEAR_RE = r"%d.*\d\d.*\d\d" % (yesterday.year)



NUM_THREADS = 50
WORKER_TIMEOUT = 30 # wait n seconds for more work and then stop
catalog_refs_queue = Queue(maxsize=0)



def process_dataset(cat, ds):
    # ignore all datasets that have an day in their ID, but that day is not yesterday
    if(re.search(THIS_YEAR_RE, ds.id) and not re.search(YESTERDAY_RE, ds.id)):
        return

    try:
        url = cat.iso_md_url(ds)
        file = OUTPUT_DIR + "/" + THREDDSMdEditor.slugify(ds.name) + ".iso.xml"
        print("download", ds.id, url, file)
        urllib.request.urlretrieve(url, file)
        THREDDSMdEditor.fix_data_id(file, ds.id)
    except Exception as e:
        print(e)
        traceback.print_tb(e.__traceback__)
        print("[ERROR] process_dataset. catalog_url=%s, ds.id=%s, url=%s, file=%s" % (cat.catalog_url, ds.id, url, file))


def process_catalog_ref(cat_ref):
    # ignore all catalogs that have a day in their path, but that day is not yesterday
    if(re.search(THIS_YEAR_RE, cat_ref.href) and not re.search(YESTERDAY_RE, cat_ref.href)):
        print("skip", cat_ref.href)
        return
    try:
        print("follow", cat_ref.href)
        cat = cat_ref.follow()
        for ref in cat.catalog_refs.values():
            # print("enqueue", ref.href)
            catalog_refs_queue.put(ref)
            # print("queue put! size =", catalog_refs_queue.qsize())
        for ds in cat.datasets.values():
            process_dataset(cat, ds)

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


def harvest_catalog(ref_name):
    print("HARVEST:", ref_name)
    cat_ref = top_cat.catalog_refs[ref_name]

    catalog_refs_queue.put(cat_ref)
    threads = []
    for _ in range(NUM_THREADS):
        t = Thread(target=worker_loop)
        threads.append(t)
        t.start()

    # print('...catalog_refs_queue.join()', flush=True)
    catalog_refs_queue.join()
    # print('catalog_refs_queue.join() DONE')

top_cat = TDSCatalog('http://thredds.ucar.edu/thredds/catalog.xml')

for ref_name in ['Forecast Model Data', 'Forecast Products and Analyses', 'Observation Data', 'Satellite Data']:
    harvest_catalog(ref_name)
