import re
import datetime

from siphon.catalog import TDSCatalog, Dataset
from lxml import etree



iso_namespaces = {'gco': "http://www.isotc211.org/2005/gco", 
'gmd': "http://www.isotc211.org/2005/gmd", 
'gmi': "http://www.isotc211.org/2005/gmi", 
'gml': "http://www.opengis.net/gml/3.2"}


class THREDDSMdGenerator():
    def create_aggregate_gmd_distributor_md(catalog_xml_url):
      xml = '''
        <gmd:distributor 
              xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
              xmlns:gco="http://www.isotc211.org/2005/gco" 
              xmlns:gmd="http://www.isotc211.org/2005/gmd" 
              xmlns:gmi="http://www.isotc211.org/2005/gmi" 
              xmlns:srv="http://www.isotc211.org/2005/srv" 
              xmlns:gmx="http://www.isotc211.org/2005/gmx" 
              xmlns:gsr="http://www.isotc211.org/2005/gsr" 
              xmlns:gss="http://www.isotc211.org/2005/gss" 
              xmlns:gts="http://www.isotc211.org/2005/gts" 
              xmlns:gml="http://www.opengis.net/gml/3.2" 
              xmlns:xlink="http://www.w3.org/1999/xlink" 
              xmlns:xs="http://www.w3.org/2001/XMLSchema">
             <gmd:MD_Distributor>
                <gmd:distributorContact>
                   <gmd:CI_ResponsibleParty>
                      <gmd:individualName gco:nilReason="missing"/>
                      <gmd:organisationName>
                         <gco:CharacterString>UCAR/UNIDATA (CyberConnector Aggregation)</gco:CharacterString>
                      </gmd:organisationName>
                      <gmd:contactInfo>
                         <gmd:CI_Contact>
                            <gmd:address>
                               <gmd:CI_Address>
                                  <gmd:electronicMailAddress>
                                     <gco:CharacterString>support@unidata.ucar.edu</gco:CharacterString>
                                  </gmd:electronicMailAddress>
                               </gmd:CI_Address>
                            </gmd:address>
                         </gmd:CI_Contact>
                      </gmd:contactInfo>
                      <gmd:role>
                         <gmd:CI_RoleCode codeList="http://www.ngdc.noaa.gov/metadata/published/xsd/schema/resources/Codelist/gmxCodelists.xml#CI_RoleCode" codeListValue="publisher">publisher</gmd:CI_RoleCode>
                      </gmd:role>
                   </gmd:CI_ResponsibleParty>
                </gmd:distributorContact>
                <gmd:distributorFormat>
                   <gmd:MD_Format>
                      <gmd:name>
                         <gco:CharacterString>HTTP Catalog URL</gco:CharacterString>
                      </gmd:name>
                      <gmd:version gco:nilReason="unknown"/>
                   </gmd:MD_Format>
                </gmd:distributorFormat>
                <gmd:distributorTransferOptions>
                   <gmd:MD_DigitalTransferOptions>
                      <gmd:onLine>
                         <gmd:CI_OnlineResource>
                            <gmd:linkage>
                               <gmd:URL>%s</gmd:URL>
                            </gmd:linkage>
                            <gmd:protocol>
                               <gco:CharacterString>WWW:LINK</gco:CharacterString>
                            </gmd:protocol>
                            <gmd:name>
                               <gco:CharacterString>THREDDS Catalog XML URL</gco:CharacterString>
                            </gmd:name>
                            <gmd:description>
                               <gco:CharacterString>This URL contains the catalog for all metadata granules like this one across the entire temporal extent of this metadata granule</gco:CharacterString>
                            </gmd:description>
                            <gmd:function>
                               <gmd:CI_OnLineFunctionCode codeList="http://www.ngdc.noaa.gov/metadata/published/xsd/schema/resources/Codelist/gmxCodelists.xml#CI_OnLineFunctionCode" codeListValue="download">download</gmd:CI_OnLineFunctionCode>
                            </gmd:function>
                         </gmd:CI_OnlineResource>
                      </gmd:onLine>
                   </gmd:MD_DigitalTransferOptions>
                </gmd:distributorTransferOptions>
             </gmd:MD_Distributor>
          </gmd:distributor>

      ''' % catalog_xml_url
      return xml


class RadarTemporalExtent():
    def __init__(self):
        # create datetime range FROM 18-days-ago at 00:00:00 TO today at 23:59:59
        self.begin = datetime.datetime.today() - datetime.timedelta(days=18)
        self.begin = self.begin.replace(hour=0, minute=0, second=0, microsecond=0)

        self.end = datetime.datetime.today()
        self.end = self.end.replace(hour=23, minute=59, second=59, microsecond=999999)


        self.begin_timestamp = self.begin.strftime("%Y-%m-%dT%H:%M:%SZ")
        self.end_timestamp = self.end.strftime("%Y-%m-%dT%H:%M:%SZ")

        self.date_stamp = self.end.strftime("%Y-%m-%d")
        self.datetime_stamp = self.end_timestamp


class THREDDSMdEditor():
    def __init__(self, doc):
        self.doc = doc

    def replace_time_extent(self):
        time_extent = RadarTemporalExtent()
        replacements = {
            '//gmd:extent//gml:TimePeriod/gml:beginPosition': time_extent.begin_timestamp,
            '//gmd:extent//gml:TimePeriod/gml:endPosition': time_extent.end_timestamp,
            '//gmd:dateStamp/gco:Date': time_extent.date_stamp,
            '//gmd:date//gco:DateTime ': time_extent.datetime_stamp
        }
        for xpath, new_text in replacements.items():
            for el in self.doc.xpath(xpath, namespaces=iso_namespaces):
                el.text = new_text


    def add_live_thredds_link(self):
        # find existing granule link
        gmd_url_el = self.doc.xpath('//gmd:distributionInfo//gmd:linkage/gmd:URL', namespaces=iso_namespaces)[0].text

        catalog_xml_url = re.sub(r"\d{8}/[^/]*$", 'catalog.xml', gmd_url_el)
        catalog_xml_url = re.sub(r"dodsC", 'catalog', catalog_xml_url)
        # print(catalog_xml_url)

        distributor_md_xml = THREDDSMdGenerator.create_aggregate_gmd_distributor_md(catalog_xml_url)
        distributor_md_el = etree.fromstring(distributor_md_xml)

        self.doc.xpath('//gmd:MD_Distribution', namespaces=iso_namespaces)[0].append(distributor_md_el)


    def replace_granule_ids(self):
        '''"NEXRAD/ABC/XYZ/20180615/Level3_VWX_OHA_20180615_1643.nids" -> "NEXRAD/ABC/XYX/__CYBERCONNECTOR_MULTIDATASET_AGGREGATE__"'''

        xpaths = [
            '//gmd:fileIdentifier/gco:CharacterString',
            '//gmd:identifier//gco:CharacterString',
            '//gmd:linkage/gmd:URL'
        ]

        for xpath in xpaths:
            for el in self.doc.xpath(xpath, namespaces=iso_namespaces):
                el.text = re.sub(r"\d{8}/[^/]*$", '__CYBERCONNECTOR_MULTIDATASET_AGGREGATE__', el.text)


def expand_thredds_iso_md(inpath, outpath):
    with open(inpath) as f:
        doc = etree.parse(f)

    md_editor = THREDDSMdEditor(doc)

    md_editor.replace_time_extent()
    md_editor.add_live_thredds_link()
    md_editor.replace_granule_ids()

    with open(outpath, 'w+') as f:
        f.write(etree.tostring(doc, pretty_print=True).decode('utf-8'))


