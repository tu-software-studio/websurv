from django import forms
from django.forms import ModelForm

from backend.models import *

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name']

class SurveyForm(ModelForm):
    class Meta:
        model = Survey
        fields = ['name','full_title']

class DictionaryForm(ModelForm):
    class Meta:
        model = Dictionary
        fields = ['name']

class VarietyForm(ModelForm):
    class Meta:
        model = Variety
        fields = ['name']

class GlossForm(ModelForm):
    class Meta:
        model = Gloss
        fields = ['primary','secondary','part_of_speech','field_tip','comment_tip']
