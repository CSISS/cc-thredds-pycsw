
import sys

from timeit import default_timer as timer
import records

from queue import Queue
from threading import Thread
from threading import Lock

import lib.siphon_ext


lock = Lock()
q = Queue(maxsize=0)
num_threads = 50
    

# def get_cat_ds_ids(cat):
#     print(cat.catalog_url, file=index_file, flush=True)
#     print('.', end='', flush=True)
#     ids = {ds for ds in cat.datasets.values()}
#     for subref in cat.catalog_refs.values():
#         ids = ids | get_cat_ds_ids(subref.follow())
#     return ids


# def get_cat_ds_ids(cat):
#     print(cat.catalog_url, file=index_file, flush=True)
#     print('.', end='', flush=True)
#     ids = {ds for ds in cat.datasets.values()}
#     for subref in cat.catalog_refs.values():
#         ids = ids | get_cat_ds_ids(subref.follow())
#     return ids


def scrape_catalog(cat, parent_catalog_id):
    cat.save_catalog_to_db(parent_catalog_id)
    for ds in cat.datasets.values():
        ds.save_dataset_to_db(cat.db_id)
    for ref in cat.catalog_refs.values():
        q.put((ref, cat.db_id))
        # scrape_catalog(ref.follow(), cat.db_id)


def reset_db():
    db.query('delete from catalogs')
    db.query('ALTER TABLE catalogs AUTO_INCREMENT = 1')
    db.query('delete from datasets')
    db.query('ALTER TABLE datasets AUTO_INCREMENT = 1')
    top_cat.save_catalog_to_db(0)

def scrape_from_queue(q):
    while True:
        ref, cat_db_id = q.get()
        print('*', end='', flush=True)
        try:
            scrape_catalog(ref.follow(), cat_db_id)
        except Exception as e:
            print("REF ERROR %s %s %s" % (ref.name, ref.title, ref.href))
            print(e)
        q.task_done()

for i in range(num_threads):
  worker = Thread(target=scrape_from_queue, args=(q,))
  worker.setDaemon(True)
  worker.start()


### PROGRAM BEGIN ####

print("+++ THREDDS Metadata Experiment +++")

db = records.Database('mysql://root@localhost/thredds_radar_analysis')
top_cat = TDSCatalog('http://thredds.ucar.edu/thredds/catalog.xml')
reset_db()

catalog_names = ['Forecast Model Data', 
                 'Forecast Products and Analyses', 
                 'Observation Data', 
                 # 'Radar Data', 
                 'Satellite Data']

catalog_names = ['Radar Data']

for name in catalog_names:
    # index_filename = name.replace(' ', '-').lower() + ".index"
    print("\n" + name + "\n")
    cat = top_cat.catalog_refs[name].follow()
    print('.', end='', flush=True)
    scrape_catalog(cat, top_cat.db_id)

print("waiting to join queue")
q.join()
print("done!")

    # print("================")
    # print(cat.catalog_url)
    # print(cat.catalog_name)
    # # print(cat.metadata)

    # start = timer()
    # with open(index_filename, "w") as index_file:
    #     cat_ids = get_cat_ds_ids(cat)
    # end = timer()
    # print("total # of ids %d" % len(cat_ids))
    # print("time elapsed = %f" % (end - start))
    # print("")