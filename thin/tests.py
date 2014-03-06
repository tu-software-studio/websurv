from django.test import TestCase
from django.test.client import Client
from django.utils import unittest

from backend.models import Dictionary, Project

# Create your tests here.
class DictionaryIndexTestCase(TestCase):
    def setUp(self):
        Project.objects.create(name="project_1")
        Dictionary.objects.create(name="dictionary_1", project="project_1")

    def test_index_contains_dictionary(self):
        client = Client()
        response = client.get('dictionary_index')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['dictionaries']), 1)

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
