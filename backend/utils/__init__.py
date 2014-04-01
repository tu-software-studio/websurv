__author__ = 'akeenan'

from django.core import management

def import_xml_to_database(import_file_name, export_file_name):
    management.call_command('import_xml', import_file_name, export_file_name)
    management.call_command('loaddata', export_file_name)