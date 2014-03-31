from django import forms
from django.forms import ModelForm
from django.forms.models import modelformset_factory

from backend.models import *

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name']

class SurveyForm(ModelForm):
    class Meta:
        model = Survey
        fields = ['name','title']

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
        fields = ['primary','secondary','pos','field_tip','comment_tip']

