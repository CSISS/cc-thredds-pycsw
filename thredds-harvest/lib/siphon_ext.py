from siphon.catalog import TDSCatalog
from siphon.catalog import Dataset

### EXTEND TDCatalog
def follow_refs(self, *names):
    catalog = self
    for n in names:
        catalog = catalog.catalog_refs[n].follow()
    return catalog

# def save_catalog_to_db(self, parent_catalog_id):
#     with lock:
#         db.query('INSERT INTO catalogs (parent_catalog_id, name, url) VALUES(:pc_id, :name, :url)',
#         pc_id=parent_catalog_id, name=self.catalog_name, url=self.catalog_url)
#         self.db_id = db.query("select id from catalogs where url=:url", url=self.catalog_url).first()['id']
#     return self.db_id


TDSCatalog.follow_refs = follow_refs
# TDSCatalog.save_catalog_to_db = save_catalog_to_db


# ### EXTEND Dataset

# def save_dataset_to_db(self, catalog_id):
#     with lock:
#     # print("save " + self.catalog_name)
#         db.query('INSERT INTO datasets (catalog_id, name, url_path, iso_url) VALUES(:c_id, :name, :url_path, :iso_url)',
#         c_id=catalog_id, name=self.name, url_path=self.url_path, iso_url=self.access_urls.get('ISO') or '')
#         self.db_id = db.query("select id from datasets where name=:name and url_path=:url_path", name=self.name, url_path=self.url_path).first()['id']
#     return self.db_id

# Dataset.save_dataset_to_db = save_dataset_to_db
