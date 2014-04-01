__author__ = 'akeenan'

from django.core.management.base import BaseCommand

from xml.dom import minidom as XML_Parser
import xmltodict
import json
from collections import OrderedDict

from backend.models import Project, Dictionary, Gloss, Survey, Variety, Transcription, PartOfSpeech


class Command(BaseCommand):
    args = '<project_to_import_to> <[file_to_import].xml> <[file_to_export_to].json>'
    help = 'Imports xml from WordSurv6 into the database'

    def handle(self, *args, **options):
        if not args or len(args) != 3:
            self.stdout.write('You must have all arguments')
        else:
            project_name = args[0]
            import_file_name = args[1]
            export_file_name = args[2]
            if import_file_name[import_file_name.rfind('.') + 1:] == 'xml':
                self.stdout.write('Running import_xml')
                root_node = XML_Parser.parse(import_file_name)
                xml_dict = xmltodict.parse(root_node.toxml())['survey']
                self.fix_dict(xml_dict)
                with open("debug_xml_to_dict.json", 'w') as f:
                    f.write(json.dumps(xml_dict, indent=2))
                    f.close()
                fixture = self.json_to_db(project_name, xml_dict)
                with open(export_file_name, 'w') as f:
                    f.write(json.dumps(fixture, indent=2))
                    f.close()
            else:
                self.stdout("Must be an xml file!")

    def fix_dict(self, dic):
        dic['gloss'] = dic['glosses']['gloss']
        dic['variety'] = dic['word_lists']['word_list']
        del dic['glosses']
        del dic['word_lists']
        if type(dic['gloss']) is not list:
            dic['gloss'] = [dic['gloss']]
        for gloss in dic['gloss']:
            gloss['transcription'] = gloss['transcriptions']['transcription']
            del gloss['transcriptions']

    def json_to_db(self, project_name, dic):
        # print dic['survey']
        self.list_to_add = []
        # self.add_to_list("survey", dic)

        project = Project.objects.filter(name=project_name)
        if len(project) > 0:
            p_id = project[0].id
        else:
            p_id = self.create_project(project_name)
        print(p_id)
        dict_id = self.create_dictionary('imported_dictionary', p_id)
        survey_id = self.create_survey(dic['name'], dic['description'], dict_id)
        variety_id = self.create_variety(dic['variety']['name'], survey_id)
        for gloss in dic['gloss']:
            gloss_id = self.create_gloss(gloss['name'], gloss['definition'], gloss['part_of_speech'], dict_id)
            if type(gloss['transcription']) is not list:
                gloss['transcription'] = [gloss['transcription']]
            for transcription in gloss['transcription']:
                self.create_transcription(transcription['name'], gloss_id, variety_id)

        return self.list_to_add

    def create_project(self, name):
        return self.add_obj_to_db(Project, {'name': name})

    def create_dictionary(self, name, project_id):
        entry = {
            'name': name,
            'project_id': project_id,
            'language_id': 0
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

    def create_survey(self, name, description, dict_id):
        entry = {
            'name': name,
            'full_title': description,
            'dictionary_id': dict_id
        }
        return self.add_obj_to_db(Survey, entry)

    def create_variety(self, name, survey_id): # TODO will need to change this to reflect the new variety attributes
        entry = {
            'name': name,
            'survey_id': survey_id
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
        print "Creating new {} with data: {}".format(model.__name__, data)
        obj = model(**data)
        obj.save()
        return obj.id

    def add_to_list(self, item, data):
        entry = {
            "pk": None,
            "model": "backend.{}".format(item),
            "fields": {name: value for name, value in data.iteritems() if
                       type(value) is not OrderedDict and type(value) is not list}}
        self.list_to_add.append(entry)

    def rename_key(self, dic, from_key, to_key):
        dic[to_key] = dic[from_key]
        del dic[from_key]