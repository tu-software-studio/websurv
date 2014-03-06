from django import forms
from django.forms import ModelForm

from backend.models import Dictionary, Project, Survey

class DictionaryForm(ModelForm):
    class Meta:
        model = Dictionary
        fields = ['name','project']


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name']


class SurveyForm(ModelForm):
    class Meta:
        model = Survey
        fields = ['name','title']
