from django.test import TestCase
from django.test.client import Client

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
