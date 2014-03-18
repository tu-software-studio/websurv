__author__ = 'akeenan'

from django.core.management.base import BaseCommand

from xml.etree import ElementTree as XML_Parser
from xml.dom import minidom as XML_Parser
import json


class Command(BaseCommand):
    args = '<[export].xml>'
    help = 'Imports xml from WordSurv6 into the database'

    def handle(self, *args, **options):
        if not args or len(args) != 1:
            self.stdout.write('You must have a single argument')
        else:
            file_name = args[0]
            if file_name[file_name.rfind('.') + 1:] == 'xml':
                self.stdout.write('Running import_xml')
                root = XML_Parser.parse(file_name)
                if root.documentElement.tagName == "survey":
                    # for child in [x for x in root.childNodes if x.nodeType != XML_Parser.Node.COMMENT_NODE]:
                    json_dump = json.dumps(self.get_data(root.documentElement), indent=2)
                    self.stdout.write(json_dump)
                    with open("export.json", 'w') as f:
                        f.write(json_dump)
                        f.close()
            else:
                self.stdout("Must be an xml file!")

    def get_data(self, node):
        if node.hasChildNodes():
            node_dictionary = {}
            for child in node.childNodes:
                if child.attributes:
                    node_dictionary[node.nodeName] = {x: y for x, y in child.attributes.items()}
                data = self.get_data(child)
                if data:
                    if node.nodeName not in node_dictionary:
                        node_dictionary[node.nodeName] = {}
                    if "data" in node_dictionary[node.nodeName]:
                        node_dictionary[node.nodeName]["data"].update(data)
                    else:
                        if type(data) != dict:
                            node_dictionary[node.nodeName] = data
                        else:
                            node_dictionary[node.nodeName]["data"] = data
            return node_dictionary
        else:
            if node.nodeValue and node.nodeValue.strip() != "":
                return node.nodeValue