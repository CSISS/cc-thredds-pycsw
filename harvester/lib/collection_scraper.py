import re

from siphon.catalog import TDSCatalog, Dataset

from .timestamp_util import timestamp_re
from .collection_generator import CollectionGenerator
from . import siphon_ext

from .util import slugify, http_getfile



class CollectionScraper():
    def __init__(self, queue, outputdir='../records/scraped'):
        self.queue = queue
        self.outputdir = outputdir
        self.collection_generator = CollectionGenerator()

    def dataset_download_url(self, dataset_catalog, dataset):
        return(dataset_catalog.iso_md_url(dataset))

    def dataset_download_file(self, dataset):
        collection_name = re.sub(timestamp_re.date_time, '', dataset.name)
        file = self.outputdir + "/" + slugify(collection_name) + ".iso.xml"
        return(file)


    def harvest_collection_catalog_metadata(self, collection_catalog, leaf_ref):
        # print("MATCH     %s.%s" % (collection_catalog.ref_name, leaf_ref.title))
        leaf_catalog = leaf_ref.follow()

        for ds_name, ds in leaf_catalog.datasets.items():
            if(timestamp_re.search_date_time(ds.id)):
                url = self.dataset_download_url(leaf_catalog, ds)
                file = self.dataset_download_file(ds)

                print("%s -> %s" % (collection_catalog.ref_name, url))
                http_getfile(url, file)

                self.collection_generator.generate_collection_iso_for_dataset(collection_catalog, ds, url, file)
                # print("quitting")
                # exit(0)
                return


    def scrape_catalog(self, catalog):
        # print("TRAVERSE  %s" % catalog.ref_name)
        for ref_name, ref in catalog.catalog_refs.items():

            # if catalog contains sub catalog named like: "20180818"
            if(timestamp_re.fullmatch_yesterday(ref_name)):
                self.harvest_collection_catalog_metadata(catalog, ref)
                return

            # if catalog contains sub-catalog with date and time in the name
            # like: "GEFS_Global_1p0deg_Ensemble_20180818_0000.grib2"
            if(timestamp_re.search_date_time(ref_name)):
                self.harvest_collection_catalog_metadata(catalog, ref)
                return

            # process subcatalogs that don't contain a timestamp
            if(timestamp_re.search_date(ref_name) == None):
                self.queue.put(ref)