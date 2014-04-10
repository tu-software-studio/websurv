__author__ = 'akeenan'

from django.core.management.base import BaseCommand

from xml.dom import minidom as XML_Parser
import xmltodict
import json
from collections import OrderedDict

from backend.models import Project, Dictionary, Gloss, Survey, Variety, Transcription, PartOfSpeech


class Command(BaseCommand):
    args = '<project_to_import_to> <[file_to_import].xml>'
    help = 'Imports xml from WordSurv6 into the database'

    def handle(self, *args, **options):
        """
        This will import data from an xml export from wordsurv6.
        """
        if not args or len(args) != 2:
            self.stdout.write('You must have all arguments')
        else:
            project_name = args[0]
            import_file_name = args[1]
            if import_file_name[import_file_name.rfind('.') + 1:] == 'xml':
                self.stdout.write('Running import_xml')
                root_node = XML_Parser.parse(import_file_name)
                xml_dict = xmltodict.parse(root_node.toxml())['survey']
                self.fix_dict(xml_dict)
                with open("debug_xml_to_dict.json", 'w') as f:
                    f.write(json.dumps(xml_dict, indent=2))
                    f.close()
                self.dict_to_db(project_name, xml_dict)
            else:
                self.stdout("Must be an xml file!")

    def fix_dict(self, dic):
        """
        Names the entries the correct things to match the database. Removes unnecessary levels.

        :param dic: The dictionary from xmltodict
        :type dic: dict
        """
        dic['gloss'] = dic['glosses']['gloss']
        dic['variety'] = dic['word_lists']['word_list']
        del dic['glosses']
        del dic['word_lists']
        if type(dic['gloss']) is not list:
            dic['gloss'] = [dic['gloss']]
        for gloss in dic['gloss']:
            gloss['transcription'] = gloss['transcriptions']['transcription']
            del gloss['transcriptions']

    def dict_to_db(self, project_name, dic):
        """
        Adds the dictionary from xmltodict to the database

        :param project_name: Name of the project you wish to add the info to. If it doesn't exist, it will be created.
        :type project_name: str
        :param dic:  The dictionary from xmltodict
        :type dic: dict
        """
        project = Project.objects.filter(name=project_name)
        if len(project) > 0:
            p_id = project[0].id
        else:
            p_id = self.create_project(project_name)
        dict_id = self.create_dictionary('imported_dictionary', p_id)
        survey_id = self.create_survey(dic['name'], dic['description'], p_id)
        variety_id = self.create_variety(dic['variety'], survey_id)
        for gloss in dic['gloss']:
            gloss_id = self.create_gloss(gloss['name'], gloss['definition'], gloss['part_of_speech'], dict_id)
            if type(gloss['transcription']) is not list:
                gloss['transcription'] = [gloss['transcription']]
            for transcription in gloss['transcription']:
                self.create_transcription(transcription['name'], gloss_id, variety_id)

    def create_project(self, name):
        return self.add_obj_to_db(Project, {'name': name})

    def create_dictionary(self, name, project_id):
        entry = {
            'name': name,
            'project_id': project_id,
            'language_id': 1
        }
        return self.add_obj_to_db(Dictionary, entry)

    def create_gloss(self, name, definition, part_of_speech, dict_id):
        entry = {
            'primary': name,
            'comment_tip': definition,
            'part_of_speech': PartOfSpeech.objects.filter(name=part_of_speech)[0],
            'dictionary_id': dict_id
        }
        return self.add_obj_to_db(Gloss, entry)

    def create_survey(self, name, description, project_id):
        entry = {
            'name': name,
            'full_title': description,
            'project_id': project_id
        }
        return self.add_obj_to_db(Survey, entry)

    def convert_time(self, str):
        from dateutil.parser import parse
        from dateutil.tz import tzlocal
        from pytz import utc

        return parse(str, tzinfos=tzlocal).astimezone(utc)

    def create_variety(self, variety, survey_id):
        entry = {
            'name': variety['name'],
            'description': variety['description'],
            'start_date': self.convert_time(variety['start_date']),
            'end_date': self.convert_time(variety['end_date']),
            'surveyors': variety['surveyors'],
            'consultants': variety['consultants'],
            'language_helper': variety['language_helper'],
            'language_helper_age': variety['language_helper_age'],
            'reliability': variety['reliability'],
            'village': variety['village'],
            'province_state': variety['province_state'],
            'district': variety['district'],
            'subdistrict': variety['subdistrict'],
            'country': variety['country'],
            'coordinates': variety['coordinates'],
            'survey_id': survey_id,
        }
        return self.add_obj_to_db(Variety, entry)

    def create_transcription(self, ipa, gloss_id, variety_id):
        entry = {
            'ipa': ipa,
            'gloss_id': gloss_id,
            'variety_id': variety_id
        }
        return self.add_obj_to_db(Transcription, entry)

    def add_obj_to_db(self, model, data):
        self.stdout.write("Creating new {} with data: {}".format(model.__name__, data))
        obj = model(**data)
        obj.save()
        return obj.id