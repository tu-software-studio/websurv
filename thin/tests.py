from django.test import TestCase
from django.test.client import Client
from django.utils import unittest

from backend.models import Dictionary, Project

# Create your tests here.
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
        response = self.client.delete('/dictionaries/1/delete')
        # response = self.client.get('/dictionaries/')
        # TODO: get this working...
        # self.assertEqual(len(response.context['dictionary_list']), len(self.project.dictionaries.count) - 1)
        self.assertEqual(len(response.context['dictionary_list']), 0)

    def test_dictionary_detail_exists(self):
        response = self.client.get('/dictionaries/' + str(self.instance.id) + '/')
        self.assertEqual(response.status_code, 200)

    def test_dictionary_index_exists(self):
        response = self.client.get('/dictionaries/')
        self.assertEqual(response.status_code, 200)

    def test_dictionary_index_contains_dictionary(self):
        Dictionary.objects.create(name="dictionary_2", project=self.project)
        response = self.client.get('/dictionaries/')
        self.assertEqual(len(response.context['dictionary_list']), 2)


class ProjectTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.instance = Project.objects.create(name="test")

    def test_project_page_index_works(self):
        response = self.client.get('/projects/')
        self.assertEqual(response.status_code, 200)
        
    def test_project_add(self):
        self.client.post('/projects/add/', {'name' : 'minombre'})
        response = self.client.get('/projects/2/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,'minombre')
              
    def test_project_index_has_the_project(self):
        response = self.client.get('/projects/')
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.context['project_list']),1)

    def test_project_delete_works(self):
        self.client.post('/projects/1/delete/')
        response = self.client.get('/projects/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['project_list']),0)

    def test_edit_project_name(self):
        self.client.post('/projects/1/edit/', {'name' : 'changedit'})
        response = self.client.get('/projects/1/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,'changedit')
