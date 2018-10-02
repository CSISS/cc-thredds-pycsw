import re

from .siphon.catalog import TDSCatalog, Dataset

from .timestamp_util import timestamp_re
from .collection_generator import CollectionGenerator
from . import siphon_ext

from .util import slugify, http_getfile

from queue import Queue

from datetime import datetime, timedelta



class CollectionGranuleIndexer():
    def __init__(self):
        self.queue = Queue(maxsize=0)
        self.download_dir = '../records/scraped'
        self.collection_generator = CollectionGenerator(output_dir='../records/collections')
        self.indexes = []

        self.duration_re = re.compile(r'((?P<hours>\d+?)\shours?)?((?P<minutes>\d+?)\sminutes?)?((?P<seconds>\d+?)\sseconds?)?')

    def parse_duration(self, duration_str):
        parts = self.duration_re.match(duration_str)
        if not parts:
            return

        parts = parts.groupdict()
        time_params = {}
        for (name, param) in parts.items():
            if param:
                time_params[name] = int(param)
        
        return timedelta(**time_params)


    # FROM: {'start': '2018-09-11T06:00:00Z', 'end': None, 'duration': 5 minutes}
    # TO: (2018-09-11T06:00:00Z, 2018-09-11T06:05:00Z)
    def time_coverage_to_time_span(self, start, end, duration):
        strpformat = '%Y-%m-%dT%H:%M:%S'
        
        if start != None:
            start = datetime.strptime(start[0:19], strpformat) 
        else:
            start = datetime.now()

        if duration != None:
            end = start + self.parse_duration(duration)
        elif end != None:
            end = datetime.strptime(end[0:19], strpformat)
        else:
            end = start


        result = (start, end)
        return result


    def index_dataset(self, catalog, ds):
        # print("index ds %s" % ds.id)
        # print(ds.time_coverage)
        iso_url = catalog.iso_md_url(ds)
        access_url = ds.access_urls.get('HTTPServer') or ds.access_urls.get('OPENDAP')

        start, end = self.time_coverage_to_time_span(**ds.time_coverage)
        result = {'name': ds.id, 'iso_url': iso_url, 'access_url': access_url, 'time_start': start, 'time_end': end}
        self.indexes.append(result)

    def scrape_catalog(self, catalog):
        # print("TRAVERSE  %s" % catalog.ref_name)
        for ref_name, ref in catalog.catalog_refs.items():
            self.queue.put(ref)

        for ds_name, ds in catalog.datasets.items():
            if(timestamp_re.search_date(ds_name) != None):
                self.index_dataset(catalog, ds)
            

