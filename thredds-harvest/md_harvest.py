import lib.siphon_ext
from siphon.catalog import TDSCatalog
from siphon.catalog import Dataset

import urllib.request
import re


OUTPUT_DIR = "records/harvested"

def fix_data_id(fname, id):
    with open(fname) as f:
        text = f.read()

    text = re.sub(r"<gmd:fileIdentifier>[^\$]+?</gmd:fileIdentifier>",
        "<gmd:fileIdentifier><gco:CharacterString>%s</gco:CharacterString></gmd:fileIdentifier>" % id,
        text,
        re.MULTILINE)

    with open(fname, "w") as f:
        f.write(text)


def download_iso(ds):
    try:
        url = ds.access_urls['ISO']
        file = OUTPUT_DIR + "/" + ds.name + ".iso.xml"
        print(url + " -> " + file)
        # print("results/" + ds.name + ".iso")
        urllib.request.urlretrieve(url, file)
        fix_data_id(file, ds.name)

    except Exception as e:
        print(e)


def download_catalog(cat):
    for ds in cat.datasets.values():
        download_iso(ds)
    for ref in cat.catalog_refs.values():
        download_catalog(ref.follow())



top_cat = TDSCatalog('http://thredds.ucar.edu/thredds/catalog.xml')

# cat = top_cat.catalog_refs['Satellite Data'].follow()
cat = top_cat.follow_refs('Satellite Data', 'Infrared (11 um)', 'WEST-CONUS_4km')

download_catalog(cat)
