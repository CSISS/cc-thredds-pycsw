from lxml import etree as ETree


class XMLEditor():
    iso_namespaces = {'gco': "http://www.isotc211.org/2005/gco", 
    'gmd': "http://www.isotc211.org/2005/gmd", 
    'gmi': "http://www.isotc211.org/2005/gmi", 
    'gml': "http://www.opengis.net/gml/3.2"}

    def __init__(self, xml):
        xml = xml.encode('utf-8')
        parser = ETree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')

        self.etree = ETree.fromstring(xml, parser=parser)
        print(type(self.etree))

    def fromfile(file):
        with open(file, 'r') as f:
            return(XMLEditor(f.read()))

    def fromstring(xml):
        return(XMLEditor(xml))

    def tofile(self, file):
        with open(file, 'w') as f:
            f.write(ETree.tostring(self.etree).decode('utf-8'))
        print("wrote %s" % file)

    def get_xpath_text(self, xpath):
        return(self.etree.xpath(xpath, namespaces=XMLEditor.iso_namespaces)[0].text)

    def get_xpath_element(self, xpath):
        return(self.etree.xpath(xpath, namespaces=XMLEditor.iso_namespaces)[0])

    def append_element_to_xpath(self, xpath, element):
        self.etree.xpath(xpath, namespaces=XMLEditor.iso_namespaces)[0].append(element)

    def update_xpath_fromstring(self, xpath, xml_string):
        element = ETree.fromstring(xml_string)

        self.etree.xpath(xpath, namespaces=XMLEditor.iso_namespaces)[0].append(element)



