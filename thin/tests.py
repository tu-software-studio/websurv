from django.db import models
from django.test import TestCase
from django.test.client import Client
from django.utils import unittest

from . import factories
from backend.models import Comparison, Dictionary, Gloss, PartOfSpeech, Project, Survey, Variety

class SessionsTestCase(TestCase):
    def test_sessions_login_exists(self):
        response = self.client.get('/login/')
        self.assertEquals(response.status_code, 200)

    def test_sessions_logout_exists(self):
        response = self.client.get('/logout/')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response['Location'], 'http://testserver/projects/')


class AdminTestCase(TestCase):
    def test_admin_page_exists(self):
        """ 
        Tests that the page exists. We'll assume everything 
        on it is correct since it's django's stuff.
        """
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)


class ComparisonTestCase(TestCase):
    def setUp(self):
        self.instance = factories.ComparisonFactory()

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
        self.project = factories.ProjectFactory()
        self.instance = factories.DictionaryFactory(project=self.project)

    def test_dictionary_add_exists(self):
        response = self.client.get('/dictionaries/add/'+ str(self.project.id) + '/')
        self.assertEqual(response.status_code, 200)

    def test_dictionary_delete_exists(self):
        response = self.client.post('/dictionaries/1/delete')
        # Status code should be 301 since we want a redirect
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response['Location'], 'http://testserver/dictionaries/1/delete/')
        
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
        factories.DictionaryFactory(project=self.project)
        response = self.client.get('/dictionaries/')
        self.assertEqual(len(response.context['dictionary_list']), 2)


class GlossTestCase(TestCase):
    def setUp(self):
        self.instance = factories.GlossFactory()

    def test_gloss_add_exists(self):
        response = self.client.get('/glosses/add/' + str(self.instance.dictionary.id) + '/')
        self.assertEqual(response.status_code, 200)

    def test_gloss_delete_exists(self):
        response = self.client.post('/glosses/' + str(self.instance.id) + '/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'http://testserver/dictionaries/1/')

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
        """ Set up for ProjectTestCase test cases """
        self.instance = factories.ProjectFactory()

    def test_project_add_exists(self):
        """ Test that a GET request works on /project/add/ """
        response = self.client.get('/projects/add/')
        self.assertEqual(response.status_code, 200)

    def test_project_add(self):
        """ Test that project add creates project """
        response = self.client.post('/projects/add/', {'name' : 'new_name'})
        try:
            new_instance = Project.objects.get(name='new_name')
        except Project.DoesNotExist:
            # Tested, and this happens if the object is not created.
            self.fail("Project was not created")
        self.assertEqual(new_instance.name, 'new_name')
              
    def test_project_delete_works(self):
        """ Test that project delete removes project """
        response = self.client.post('/projects/' + str(self.instance.id) + '/delete/')
        self.assertEqual(response.status_code, 302)
        # Make sure the project has been deleted by looking for the id.
        self.assertFalse(Project.objects.filter(id=self.instance.id).exists())

    # TODO: Here
    def test_project_detail(self):
        response = self.client.post('/projects/' + str(self.instance.id) + '/')
        self.assertEqual(response.status_code, 200)

        # Test response includes project.name
        self.assertContains(response, self.instance.name)

        # Test for edit link
        # TODO: find how to test for a link...
        print()
        print("href='/projects/" + str(self.instance.id) + "/edit/'")
        self.assertContains(response, "href='/projects/" + str(self.instance.id) + "/edit/'")

        ## Test that all dictionaries in the project show up
        # If no dictionaries, tell the user
        self.assertContains(response, 'There are currently no dictionaries for this project.')

        # Now try it with some dictionaries
        for i in range(3):
            factories.DictionaryFactory(project=self.instance)

        dictionaries = Dictionary.objects.filter(project=self.instance)
        response = self.client.post('/projects/' + str(self.instance.id) + '/')
        for dictionary in dictionaries:
            self.assertContains(response, dictionary.id)

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
        project_2 = factories.ProjectFactory()
        response = self.client.get('/projects/')
        self.assertEqual(len(response.context['project_list']), 2)


class SurveyTestCase(TestCase):
    def setUp(self):
        self.instance = factories.SurveyFactory()

    def test_survey_add_exists(self):
        response = self.client.get('/surveys/add/')
        self.assertEqual(response.status_code, 200)

    def test_survey_delete_exists(self):
        response = self.client.post('/surveys/' + str(self.instance.id) + '/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'http://testserver/surveys/')

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
        self.instance = factories.VarietyFactory()

    def test_variety_add_exists(self):
        response = self.client.get('/varieties/add/')
        self.assertEqual(response.status_code, 200)

    def test_variety_delete_exists(self):
        response = self.client.post('/varieties/' + str(self.instance.id) + '/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'http://testserver/varieties/')

    def test_variety_detail_exists(self):
        response = self.client.get('/varieties/' + str(self.instance.id) + '/')
        self.assertEqual(response.status_code, 200)

    def test_variety_edit_exists(self):
        response = self.client.get('/varieties/' + str(self.instance.id) + '/edit/')
        self.assertEqual(response.status_code, 200)
        
    def test_variety_index_exists(self):
        response = self.client.get('/varieties/')
        self.assertEqual(response.status_code, 200)

