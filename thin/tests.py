from django.test import TestCase
from django.test.client import Client
from django.utils import unittest

from backend.models import Dictionary, Project

# Create your tests here.
class DictionaryIndexTestCase(TestCase):
    def set_up(self):
        Project.objects.create(name="project_1")
        Dictionary.objects.create(name="dictionary_1", project="project_1")

    def test_index_contains_dictionary(self):
        client = Client()
        response = client.get('dictionary_index')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['dictionaries']), 1)

class ProjectTestCase(TestCase):
    def setup(self):
        self.client = Client()
        self.instance = Project(name="test")

    def test_project_index(self):
        response = self.client.get('/projects/')
        self.assertEqual(response.status_code, 200)

    def test_project_create(self):
        self.client.post('/projects/add/', {'name' : 'test'})
        response = self.client.get('/projects/1/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response,'test')
               

    def test_project_index_has_same_amount_of_projects_as_database(self):
        response = self.client.get('/projects/')
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.context['project_list']),len(Project.objects.all()))
>>>>>>> 06b01abd7db2a8c0dc9854c004305e854c486abe
