from django.db import models
from django.test import TestCase
from django.test.client import Client
from django.utils import unittest

from backend.models import Comparison, Dictionary, Gloss, PartOfSpeech, Project, Survey, Variety

class SessionsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_sessions_login_exists(self):
        response = self.client.get('/login/')
        self.assertEquals(response.status_code, 200)

    def test_sessions_logout_exists(self):
        response = self.client.get('/logout/')
        self.assertEquals(response.status_code, 302)


class AdminTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_admin_page_exists(self):
        """ 
        Tests that the page exists. We'll assume everything 
        on it is correct since it's django's stuff.
        """
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)


class ComparisonTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.project = Project.objects.create(name="project")
        self.dictionary = Dictionary.objects.create(name="dictionary_1", project=self.project)
        self.survey = Survey.objects.create(name="survey_1", title="Title", dictionary=self.dictionary)

#        self.gloss = Gloss(""" TODO """)
#        self.transcription = Transcription(ipa='ipa', gloss=self.gloss,)
        self.instance = Comparison.objects.create(
            name='comparison_1',
            description='testing',
            survey = self.survey
        )

    def test_comparison_index_exists(self):
        response = self.client.get('/comparisons/')
        self.assertEqual(response.status_code, 200)

    def test_comparison_detail_exists(self):
        response = self.client.get('/comparisons/' + str(self.instance.id) + '/')
        self.assertEqual(response.status_code, 200)

    def test_comparison_edit_exists(self):
        response = self.client.get('/comparisons/' + str(self.instance.id) + '/edit/')
        self.assertEqual(response.status_code, 200)


class DictionaryTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.project = Project.objects.create(name="project")
        self.instance = Dictionary.objects.create(name="dictionary_1", project=self.project)

    def test_dictionary_add_exists(self):
        response = self.client.get('/dictionaries/add/'+ str(self.project.id) + '/')
        self.assertEqual(response.status_code, 200)

    def test_dictionary_delete_exists(self):
        response = self.client.post('/dictionaries/1/delete')
        # Status code should be 301 since we want a redirect
        self.assertEqual(response.status_code, 301)
        
    def test_dictionary_delete_removes_dictionary(self):
        """ Tests that the dictionary_delete view deletes a dicionary. """
        num_dicts = self.project.dictionaries.count()
        self.client.post('/dictionaries/' + str(self.instance.id) + '/delete/')
        response = self.client.get('/dictionaries/')
        self.assertEqual(len(response.context['dictionary_list']), num_dicts - 1)

    def test_dictionary_detail_exists(self):
        response = self.client.get('/dictionaries/' + str(self.instance.id) + '/')
        self.assertEqual(response.status_code, 200)

    def test_dictionary_edit_exists(self):
        response = self.client.get('/dictionaries/' + str(self.instance.id) + '/edit/')
        self.assertEqual(response.status_code, 200)

    def test_dictionary_index_exists(self):
        response = self.client.get('/dictionaries/')
        self.assertEqual(response.status_code, 200)

    def test_dictionary_index_contains_dictionary(self):
        Dictionary.objects.create(name="dictionary_2", project=self.project)
        response = self.client.get('/dictionaries/')
        self.assertEqual(len(response.context['dictionary_list']), 2)


class GlossTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.pos = PartOfSpeech.objects.create(name='noun')
        self.project = Project.objects.create(name="project_1")
        self.dictionary = Dictionary.objects.create(name='dictionary_1', project=self.project)
        self.instance = Gloss.objects.create(
            primary="primary_1",
            secondary="secondary_1",
            pos=self.pos,
            dictionary=self.dictionary,
            field_tip="field_tip_1",
            comment_tip="comment_tip_1",
            created_at = models.DateTimeField(auto_now_add=True)
        )

    def test_gloss_add_exists(self):
        response = self.client.get('/glosses/add/' + str(self.dictionary.id) + '/')
        self.assertEqual(response.status_code, 200)

    def test_gloss_delete_exists(self):
        response = self.client.post('/glosses/' + str(self.instance.id) + '/delete/')
        self.assertEqual(response.status_code, 302)

    def test_gloss_detail_exists(self):
        response = self.client.get('/glosses/' + str(self.instance.id) + '/')
        self.assertEqual(response.status_code, 200)

    def test_gloss_edit_exists(self):
        response = self.client.get('/glosses/' + str(self.instance.id) + '/edit/')
        self.assertEqual(response.status_code, 200)
        
    def test_gloss_index_exists(self):
        response = self.client.get('/glosses/')
        self.assertEqual(response.status_code, 200)

        
class ProjectTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.instance = Project.objects.create(name="project_1")

    def test_project_add_exists(self):
        response = self.client.post('/projects/add/')
        self.assertEqual(response.status_code, 200)

    def test_project_add(self):
        self.client.post('/projects/add/', {'name' : 'minombre'})
        response = self.client.get('/projects/2/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,'minombre')
              
    def test_project_delete_works(self):
        self.client.post('/projects/1/delete/')
        response = self.client.get('/projects/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['project_list']),0)

    def test_project_detail_exists(self):
        response = self.client.post('/projects/' + str(self.instance.id) + '/')
        self.assertEqual(response.status_code, 200)

    def test_project_edit_exist(self):
        response = self.client.get('/projects/' + str(self.instance.id) + '/edit/')
        self.assertEqual(response.status_code, 200)

    def test_edit_project_name(self):
        self.client.post('/projects/1/edit/', {'name' : 'new_name'})
        response = self.client.get('/projects/1/')
        self.assertContains(response, 'new_name')

    def test_project_index_exists(self):
        response = self.client.get('/projects/')
        self.assertEqual(response.status_code, 200)
        
    def test_project_index_contains_project(self):
        Project.objects.create(name='project_2')
        response = self.client.get('/projects/')
        self.assertEqual(len(response.context['project_list']), 2)


class SurveyTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.project = Project.objects.create(name="project")
        self.dictionary = Dictionary.objects.create(name="dictionary_1", project=self.project)
        self.instance = Survey.objects.create(name="survey_1", title="Title", dictionary=self.dictionary)

    def test_survey_add_exists(self):
        response = self.client.get('/surveys/add/')
        self.assertEqual(response.status_code, 200)

    def test_survey_delete_exists(self):
        response = self.client.post('/surveys/' + str(self.instance.id) + '/delete/')
        self.assertEqual(response.status_code, 302)

    def test_survey_detail_exists(self):
        response = self.client.get('/surveys/' + str(self.instance.id) + '/')
        self.assertEqual(response.status_code, 200)

    def test_survey_edit_exists(self):
        response = self.client.get('/surveys/' + str(self.instance.id) + '/edit/')
        self.assertEqual(response.status_code, 200)
        
    def test_survey_index_exists(self):
        response = self.client.get('/surveys/')
        self.assertEqual(response.status_code, 200)


class VarietyTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.project = Project.objects.create(name="project")
        self.dictionary = Dictionary.objects.create(name="dictionary_1", project=self.project)
        self.survey = Survey.objects.create(name="survey_1", title="Title", dictionary=self.dictionary)
        self.instance = Variety.objects.create(name='variety_1', survey=self.survey)

    def test_variety_add_exists(self):
        response = self.client.get('/varieties/add/')
        self.assertEqual(response.status_code, 200)

    def test_variety_delete_exists(self):
        response = self.client.post('/varieties/' + str(self.instance.id) + '/delete/')
        self.assertEqual(response.status_code, 302)

    def test_variety_detail_exists(self):
        response = self.client.get('/varieties/' + str(self.instance.id) + '/')
        self.assertEqual(response.status_code, 200)

    def test_variety_edit_exists(self):
        response = self.client.get('/varieties/' + str(self.instance.id) + '/edit/')
        self.assertEqual(response.status_code, 200)
        
    def test_variety_index_exists(self):
        response = self.client.get('/varieties/')
        self.assertEqual(response.status_code, 200)

