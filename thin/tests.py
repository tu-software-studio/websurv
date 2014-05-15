from django.db import models
from django.test import TestCase
from django.test.client import Client
from django.utils import unittest
from django.core.urlresolvers import reverse

from . import factories
from backend.models import Comparison, Dictionary, Gloss, PartOfSpeech, Project, Survey, Variety

class SessionsTestCase(TestCase):
    def test_sessons_login_exists(self):
        """ 
        Ensure login page exists. We'll assume it
        works, since it's django's stuff.
        """
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)

    def test_sessions_logout_exists(self):
        """ Ensure logout exists and redirects to / """
        response = self.client.get(reverse('logout'))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('project_index'))


class HomeTestCase(TestCase):
    def setUp(self):
        """ Set up for home page tests. """
        self.response = self.client.get(reverse('home'))

    def test_home_page_exists(self):
        """ Ensure the home page exists. """
        self.assertEqual(self.response.status_code, 200)

    def test_home_page_location(self):
        """ Ensure home page is project_index. """
        names = []
        for template in self.response.templates:
            names.append(template.name)
        self.assertIn('thin/project_index.html', names)


class AdminTestCase(TestCase):
    def test_admin_page_exists(self):
        """ 
        Tests that the page exists. We'll assume everything 
        on it is correct since it's django's stuff.
        """
        response = self.client.get('/admin/') #TODO - is there a way to give the admin pages a name?
        self.assertEqual(response.status_code, 200)


class ComparisonTestCase(TestCase):
    def setUp(self):
        self.instance = factories.ComparisonFactory.create()

    def test_comparison_index_exists(self):
        response = self.client.get(reverse('comparison_index'))
        self.assertEqual(response.status_code, 302)

    def test_comparison_detail_exists(self):
        response = self.client.get(reverse('comparison_detail', kwargs = { 'id' : self.instance.id }))
        self.assertEqual(response.status_code, 200)

    def test_comparison_edit_exists(self):
        response = self.client.get(reverse('comparison_edit', kwargs = { 'id' : self.instance.id }))
        self.assertEqual(response.status_code, 200)

class GlossTestCase(TestCase):
    def setUp(self):
        self.instance = factories.GlossFactory.create()

    def test_gloss_add_exists(self):
        response = self.client.get(reverse('gloss_add', kwargs = { 'id' : self.instance.dictionary.id }))
        self.assertEqual(response.status_code, 200)

    def test_gloss_delete_exists(self):
        response = self.client.post(reverse('gloss_delete', kwargs = { 'id' : self.instance.id }))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dictionary_detail',kwargs = { 'id' : self.instance.dictionary.id }))

    def test_gloss_detail_exists(self):
        response = self.client.get(reverse('gloss_detail', kwargs = { 'id' : self.instance.id }))
        self.assertEqual(response.status_code, 302)

    def test_gloss_edit_exists(self):
        response = self.client.get(reverse('gloss_edit', kwargs = { 'id' : self.instance.id }))
        self.assertEqual(response.status_code, 200)
        
    def test_gloss_index_exists(self):
        response = self.client.get(reverse('gloss_index'))
        self.assertEqual(response.status_code, 302)

        
class ProjectTestCase(TestCase):
    def setUp(self):
        """ Set up for ProjectTestCase test cases """
        self.instance = factories.ProjectFactory.create()

    def test_project_add_exists(self):
        """ Test that a GET request works on /project/add/ """
        response = self.client.get(reverse('project_add'))
        self.assertEqual(response.status_code, 200)

    def test_project_add(self):
        """ Test that project add creates project """
        response = self.client.post(reverse('project_add'), {'name' : 'new_project' })
        try:
            new_instance = Project.objects.get(name='new_project')
        except Project.DoesNotExist:
            # Tested, and this code runs if the object is not created.
            self.fail("Project was not created.")
        self.assertEqual(new_instance.name, 'new_project')
        self.assertRedirects(response, reverse('project_detail', kwargs = { 'id' : new_instance.id } ))
              
    def test_project_delete_works(self):
        """ Test that project delete removes project """
        response = self.client.post(reverse('project_delete', kwargs = { 'id' : self.instance.id } ))
        self.assertEqual(response.status_code, 302)
        # Make sure the project has been deleted by looking for the id.
        self.assertFalse(Project.objects.filter(id=self.instance.id).exists())

    def test_project_detail(self):
        """ Test project detail properly displays project """
        response = self.client.get(reverse('project_detail',kwargs = { 'id' : self.instance.id } ))
        self.assertEqual(response.status_code, 200)

        # Test response includes project.name
        self.assertContains(response, self.instance.name)

        # Test for edit link
        # TODO: find how to better test for a link.
        self.assertContains(response, 'href="edit"')

        # If no dictionaries, tell the user
        self.assertContains(response, 'There are currently no dictionaries for this project.')

        # Test that all dictionaries in the project show up
        for i in range(15): # Use high number because we're just searching for the number in the html
            factories.DictionaryFactory.create(project=self.instance)

        dictionaries = Dictionary.objects.filter(project=self.instance)
        response = self.client.get(reverse('project_detail', kwargs = { 'id' : self.instance.id } ))
        for dictionary in dictionaries:
            self.assertContains(response, dictionary.id)

        # Test for dictionary/add link
        self.assertContains(response, "<a href='/dictionaries/add/" + str(self.instance.id)+ "/")

        # Test for Surveys
        for i in range(15):
            factories.SurveyFactory.create(project=self.instance)
        surveys = Survey.objects.filter(project=self.instance)

        response = self.client.get(reverse('project_detail', kwargs = { 'id' : self.instance.id } ))
        for survey in surveys:
            self.assertContains(response, survey.name)
            self.assertContains(response, reverse('survey_detail', kwargs = { 'id' : survey.id } ))

        # Test that add new survey link is there
        self.assertContains(response, reverse('survey_add',kwargs = { 'id' : self.instance.id } ))

        # Test that add new dictionary link is there
        self.assertContains(response, reverse('dictionary_add',kwargs = { 'id' : self.instance.id } ))

    def test_project_edit_exist(self):
        """ Test project edit link exists for GET request """
        response = self.client.get(reverse('project_detail', kwargs = { 'id' : self.instance.id } ))
        self.assertEqual(response.status_code, 200)

    def test_project_edit(self):
        """ Test project edit actually edits the project """
        self.client.post(reverse('project_edit', kwargs = { 'id' : self.instance.id }), {'name' : 'new_name'})
        try:
            project = Project.objects.filter(name='new_name')
        except Project.DoesNotExist:
            self.fail("Project edit should change project name.")
        self.assertEqual(project[0].name, 'new_name')

    def test_project_index(self):
        """ Test project index displays properly """
        # First test with no projects, even though this will almost never be true
        self.instance.delete()
        response = self.client.get(reverse('project_index'))
        self.assertEqual(len(response.context['project_list']), 0)
        self.assertContains(response, "There are no projects.")

        # Now add some projects and test for stuff
        num_projects = 15
        for i in range(num_projects):
            factories.ProjectFactory.create()
        
        response = self.client.get(reverse('project_index'))
        self.assertEqual(len(response.context['project_list']), num_projects)
        for project in Project.objects.all():
            # Check for project detail and edit links for each existing project
            self.assertContains(response, "<a href='/projects/" + str(project.id) + "/")
            self.assertContains(response, "<a href='/projects/" + str(project.id) + "/edit/")

class TranscriptionTestCase(TestCase):
    def setUp(self):
        self.instance = factories.TranscriptionFactory.create()

    def test_transcription_add_exists(self):
        response = self.client.get(reverse('transcription_add', kwargs = { 'id' : self.instance.variety.id } ))
        self.assertEqual(response.status_code, 302)

class VarietyTestCase(TestCase):
    def setUp(self):
        self.instance = factories.VarietyFactory.create()

    def test_variety_add_exists(self):
        response = self.client.get(reverse('variety_add', kwargs = { 'id' : self.instance.id } ))
        self.assertEqual(response.status_code, 200)

    def test_variety_delete_exists(self):
        response = self.client.post(reverse('variety_delete', kwargs = { 'id' : self.instance.id }))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('survey_detail', kwargs = { 'id' : self.instance.id } ))

    def test_variety_detail_exists(self):
        response = self.client.get(reverse('variety_detail', kwargs = { 'id' : self.instance.id } ))
        self.assertEqual(response.status_code, 200)

    def test_variety_edit_exists(self):
        response = self.client.get(reverse('variety_edit', kwargs = { 'id' : self.instance.id } ))
        self.assertEqual(response.status_code, 200)
        
    def test_variety_index_exists(self):
        response = self.client.get(reverse('variety_index'))
        self.assertEqual(response.status_code, 302)

class DictionaryTestCase(TestCase):
    def setUp(self):
        """ Set up for DictionaryTestCase test cases """
        self.instance = factories.DictionaryFactory.create()

    def test_Dictionary_add_exists(self):
        """ Test that a GET request works on /project/add/ """
        response = self.client.get(reverse('dictionary_add', kwargs = { 'id' : self.instance.project.id }))
        self.assertEqual(response.status_code, 200)

    def test_dictionary_add(self):
        response = self.client.post(reverse('dictionary_add',kwargs = { 'id' : self.instance.project.id }),
                                    {'name': 'new_dictionary',
                                     'language': factories.LanguageFactory.create().id
                                     })
        try:
            new_instance = Dictionary.objects.get(name='new_dictionary')
        except Dictionary.DoesNotExist:
            self.fail("Dictionary was not created.")
        self.assertEqual(new_instance.name, 'new_dictionary')
        self.assertRedirects(response, reverse('dictionary_detail', kwargs = { 'id' : new_instance.id }))

    def test_dictionary_delete_exists(self):
        response = self.client.post(reverse('dictionary_delete', kwargs = { 'id' : self.instance.id }))
        # Status code should be 302 since we want a redirect
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('project_detail', kwargs = { 'id' : self.instance.project.id }))

    def test_dictionary_edit_exists(self):
        response = self.client.get(reverse('dictionary_edit', kwargs = { 'id' : self.instance.id }))
        self.assertEqual(response.status_code, 200)

    def test_dictionary_index_exists(self):
        response = self.client.get(reverse('dictionary_index'))
        self.assertEqual(response.status_code, 302)

    def test_dictionary_delete_works(self):
        """ Test that the dictionary delete removes dictionary """
        response = self.client.post(reverse('dictionary_delete', kwargs = { 'id' : self.instance.id } ))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Dictionary.objects.filter(id=self.instance.id).exists())


    def test_dictionary_detail(self):
        """ Test dictionary detail properly displays dictionary """
        response = self.client.get(reverse('dictionary_detail',kwargs = { 'id' : self.instance.id } ))
        self.assertEqual(response.status_code, 200)

        # Test response includes dictionary.name
        self.assertContains(response, self.instance.name)

        # Test for having the dictionary's project
        self.assertContains(response, self.instance.project.name)

        # Test for edit link
        # TODO: find how to better test for a link.
        self.assertContains(response, 'href="edit"')

        # If no surveys, tell the user
        #self.assertContains(response, 'There are currently no dictionaries for this project.')

        # Test that all dictionaries in the project show up
        for i in range(15): # Use high number because we're just searching for the number in the html
            factories.GlossFactory.create(dictionary=self.instance)

        glosses = Gloss.objects.filter(dictionary=self.instance)
        response = self.client.get(reverse('dictionary_detail', kwargs = { 'id' : self.instance.id } ))
        for gloss in glosses:
            self.assertContains(response, gloss.id)

        # Test for gloss_add link
        self.assertContains(response, reverse('gloss_add', kwargs = { 'id' : self.instance.id }))

        # Test that glosses are shown
        num_glosses = 15
        for i in range(num_glosses):
            factories.GlossFactory.create(dictionary=self.instance)

        response = self.client.get(reverse('dictionary_detail', kwargs = { 'id' : self.instance.id} ))
        for gloss in Gloss.objects.all():
            self.assertContains(response, str(gloss.primary))
            self.assertContains(response, reverse('gloss_edit', kwargs = { 'id' : gloss.id }))

    def test_dictionary_edit(self):
        """ Test project edit link exists for GET request """
        response = self.client.get(reverse('dictionary_detail', kwargs = { 'id' : self.instance.id } ))
        self.assertEqual(response.status_code, 200)

        """ Test project edit actually edits the project """
        self.client.post(reverse('dictionary_edit', kwargs = { 'id' : self.instance.id }), {'name' : 'new_name', 
                                                                                             'language': factories.LanguageFactory.create().id,
                                                                                            'project' : self.instance.project })
        try:
            dictionary = Dictionary.objects.filter(name='new_name')
        except Dictionary.DoesNotExist:
            self.fail("Dictionary edit should change dictionary name.")
        self.assertEqual(dictionary[0].name, 'new_name')

class SurveyTestCase(TestCase):
    def setUp(self):
        self.instance = factories.SurveyFactory.create()

    def test_survey_add_exists(self):
        response = self.client.get(reverse('survey_add', kwargs = { 'id' : self.instance.project.id } ))
        self.assertEqual(response.status_code, 200)
               
    def test_survey_add(self):
        response = self.client.post(reverse('survey_add', kwargs = { 'id' : self.instance.project.id }),
                                    {'name': 'new_survey',
                                     'full_title': 'hello',
                                     'dictionaries' : factories.DictionaryFactory(project=self.instance.project).id
                                     })
        try:
            new_instance = Survey.objects.get(name='new_survey')
        except Survey.DoesNotExist:
            self.fail("Survey was not created.")
        self.assertEqual(new_instance.name, 'new_survey')
        self.assertRedirects(response, reverse('survey_detail', kwargs = { 'id' : new_instance.id }))

    def test_survey_delete_exists(self):
        response = self.client.post(reverse('survey_delete', kwargs = { 'id' : self.instance.id } ))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('project_detail', kwargs = { 'id' : self.instance.project.id } ))

    def test_survey_delete_works(self):
        """ test that the survey delete really deletes a survey """
        response = self.client.post(reverse('survey_delete', kwargs = { 'id' : self.instance.id } ))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Dictionary.objects.filter(id=self.instance.id).exists())

    def test_survey_detail_exists(self):
        response = self.client.get(reverse('survey_detail', kwargs = { 'id' : self.instance.id } ))
        self.assertEqual(response.status_code, 200)

    def test_survey_detail(self):
        # Test Survey Detail properly displays itself
        response = self.client.get(reverse('survey_detail', kwargs = { 'id' : self.instance.id } ))
        self.assertEqual(response.status_code, 200)


        # Test response includes survey.name
        self.assertContains(response, self.instance.name)

        # Test for having the survey's project
        self.assertContains(response, self.instance.project.name)

        # Test for edit link
        # TODO: find how to better test for a link.
        self.assertContains(response, 'href="edit"')

        # Test that varieties show up
        for i in range(15):
            factories.VarietyFactory.create(survey = self.instance)

        response = self.client.get(reverse('survey_detail', kwargs = { 'id' : self.instance.id } ))
        varieties = Variety.objects.filter(survey=self.instance)
        for variety in varieties:
            self.assertContains(response, variety.name)
            self.assertContains(response, reverse('variety_detail', kwargs = { 'id' : variety.id } ))

        # Test for variety_add link
        self.assertContains(response, reverse('variety_add', kwargs = { 'id' : self.instance.id }))

    def test_survey_edit_exists(self):
        response = self.client.get(reverse('survey_edit', kwargs = { 'id' : self.instance.id } ))
        self.assertEqual(response.status_code, 200)
        
    def test_survey_index_exists(self):
        response = self.client.get(reverse('survey_index'))
        self.assertEqual(response.status_code, 302)

    def test_survey_edit(self): #TODO - I cant get it to change the name
        """ Test project edit link exists for GET request """
        response = self.client.get(reverse('survey_detail', kwargs = { 'id' : self.instance.id } ))
        self.assertEqual(response.status_code, 200)
    
        # Test project edit actually edits the project
        response = self.client.post(reverse('survey_edit', kwargs = { 'id' : self.instance.project.id }),
                                    {'name': 'new_name',
                                     'full_title': 'hello',
                                     'dictionaries' : factories.DictionaryFactory(project=self.instance.project).id
                                     })
        try:
            survey = Survey.objects.filter(name='new_name', full_title='hello')
        except Survey.DoesNotExist:
            self.fail("Survey edit should change survey name.")
        self.assertEqual(survey[0].name, 'new_name')
