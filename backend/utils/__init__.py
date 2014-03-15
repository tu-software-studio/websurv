__author__ = 'akeenan'

from django.core import management

def import_xml_to_database(file_name):
    management.call_command('import_xml', file_name)