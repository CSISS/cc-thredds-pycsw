# python3

# import lib.siphon_ext

# from lib.thredds_md_expander import expand_thredds_iso_md



from siphon.catalog import TDSCatalog, Dataset

import urllib.parse
import urllib.request
import unicodedata

import sys
import re
import pathlib
import datetime

import traceback


from threading import Thread, Lock
from queue import Queue, Empty



def follow_refs(self, *names):
    catalog = self
    for n in names:
        catalog = catalog.catalog_refs[n].follow()
    return catalog


def iso_md_url(self, ds):
    try:
        return ds.access_urls['ISO'] + \
            '?catalog=' + \
            urllib.parse.quote_plus(self.catalog_url) + \
            '&dataset=' + \
            urllib.parse.quote_plus(ds.id)
    except Exception as e:
        print("bad iso_md_url", cat_ref.href, ds.id)
        print(e)
        return "INVALID"

TDSCatalog.follow_refs = follow_refs
TDSCatalog.iso_md_url = iso_md_url



OUTPUT_DIR = '../records/harvested'

NUM_THREADS = 50
# lock = Lock()
catalog_refs_queue = Queue(maxsize=0)


def fix_data_id(fname, id):
    with open(fname) as f:
        text = f.read()

    text = re.sub(r"<gmd:fileIdentifier>[^\$]+?</gmd:fileIdentifier>",
        "<gmd:fileIdentifier><gco:CharacterString>%s</gco:CharacterString></gmd:fileIdentifier>" % id,
        text,
        re.MULTILINE)

    with open(fname, "w") as f:
        f.write(text)


def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    # value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    value = re.sub('[-\s]+', '-', value)
    return value

def process_dataset(cat, ds):
    try:
        url = cat.iso_md_url(ds)
        file = OUTPUT_DIR + "/" + slugify(ds.name) + ".iso.xml"
        print("dataset download", ds.id, url, file)
        urllib.request.urlretrieve(url, file)
        fix_data_id(file, ds.id)
    except Exception as e:
        print("[ERROR] process_dataset. catalog_url=%s, ds.id=%s, url=%s, file=%s" % (cat.catalog_url, ds.id, url, file))
        print(e)
        traceback.print_tb(e.__traceback__)


def process_catalog_ref(cat_ref):
    try:
        print("cat_ref follow", cat_ref.href)
        cat = cat_ref.follow()
        for ref in cat.catalog_refs.values():
            catalog_refs_queue.put(ref)
            print("queue put! size =", catalog_refs_queue.qsize())
        for ds in cat.datasets.values():
            process_dataset(cat, ds)

    except Exception as e:
        print("[ERROR] process_catalog_ref", cat_ref.href)
        print(e)
        traceback.print_tb(e.__traceback__)


def worker_loop():
    print('Worker')
    while True:
        try:
            print("...queue get. size =", catalog_refs_queue.qsize())
            cat_ref = catalog_refs_queue.get(timeout=2)
            process_catalog_ref(cat_ref)
            catalog_refs_queue.task_done()
        except Empty:
            return


def harvest_catalog(ref_name):
    cat_ref = top_cat.catalog_refs[ref_name]

    catalog_refs_queue.put(cat_ref)
    threads = []
    for _ in range(NUM_THREADS):
        t = Thread(target=worker_loop)
        threads.append(t)
        t.start()

    print('...catalog_refs_queue.join()', flush=True)
    catalog_refs_queue.join()
    print('catalog_refs_queue.join() DONE')

# top_cat = TDSCatalog('http://thredds.ucar.edu/thredds/catalog.xml')
top_cat = TDSCatalog('http://thredds.ucar.edu/thredds/catalog.xml').follow_refs('Forecast Model Data')
harvest_catalog('GEFS Members - Analysis')

# for ref_name in ['Forecast Model Data', 'Forecast Products and Analyses', 'Observation Data', 'Satellite Data', 'Unidata case studies']:
# for ref_name in ['Forecast Model Data']:
