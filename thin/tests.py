from django.utils import unittest
from django.test import TestCase
from django.test.client import Client

from backend.models import Project

# Create your tests here.

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
