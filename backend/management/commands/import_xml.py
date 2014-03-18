__author__ = 'akeenan'

from django.core.management.base import BaseCommand

from xml.dom import minidom as XML_Parser
import xmltodict
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
                root_node = XML_Parser.parse(file_name)
                xml_dict = xmltodict.parse(root_node.toxml())
                with open("export.json", 'w') as f:
                    f.write(json.dumps(xml_dict, indent=2))
                    f.close()
            else:
                self.stdout("Must be an xml file!")