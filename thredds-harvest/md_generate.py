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
SAME_YEAR_RE = r"%d.*\d\d.*\d\d" % (today.year)



OUTPUT_DIR = '../records/generated'

NUM_THREADS = 1
WORKER_TIMEOUT = 30 # wait n seconds for more work and then stop
catalog_refs_queue = Queue(maxsize=0)




class MDGenerator():
    def generate_for_catalog_dataset(cat, ds):
        try:
            url = cat.iso_md_url(ds)
            file = OUTPUT_DIR + "/" + THREDDSMdEditor.slugify(ds.name) + ".iso.xml"
            print("collection sample dataset download", ds.id, url, file)

            urllib.request.urlretrieve(url, file)
            THREDDSMdEditor.expand_thredds_iso_md(file, file)
        except Exception as e:
            print(e)
            traceback.print_tb(e.__traceback__)
            print("[ERROR] generate_for_catalog_dataset. catalog_url=%s, ds.id=%s, url=%s, file=%s" % (cat.catalog_url, ds.id, url, file))


    def generate_for_catalog(cat):
        for ref_name in cat.catalog_refs.keys():
            # find a sub-catalog that is for today or within same year
            # inside that sub-catalog pick a dataset that represents a typical MD granule
            if(re.search(TODAY_RE, ref_name) or re.search(SAME_YEAR_RE, ref_name)):
                child_cat = cat.catalog_refs[ref_name].follow()
                # dont use the first dataset in the catalog, because it's often the one named 'latest'
                # which is different from all other datasets
                if len(child_cat.datasets) > 1:
                    ds = child_cat.datasets[1]
                    MDGenerator.generate_for_catalog_dataset(child_cat, ds)
                    return



def process_catalog_ref(cat_ref):
    print("follow", cat_ref.href)
    cat = cat_ref.follow()
    for ref_name in cat.catalog_refs.keys():
        try:
            if re.search(TODAY_RE, ref_name):
                # we found todays catalog
                # use that to generate a single aggregate metadata for all sibling catalogs
                MDGenerator.generate_for_catalog(cat)
                return
            elif re.search(SAME_YEAR_RE, ref_name):
                # previous days catalog
                next
            else:
                child_cat_ref = cat.catalog_refs[ref_name]
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

catalog_refs_queue.put(cat_ref)
threads = []
for _ in range(NUM_THREADS):
    t = Thread(target=worker_loop)
    threads.append(t)
    t.start()

catalog_refs_queue.join()
