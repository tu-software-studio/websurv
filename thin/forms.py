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
        fields = ['name','full_title']


class SurveyAddForm(ModelForm):
    class Meta:
        model = Survey
        fields = ['name','full_title']
    dictionaries = forms.ModelMultipleChoiceField(queryset=Dictionary.objects.all(),label="Dictionaries for Survey")


class DictionaryForm(ModelForm):
    class Meta:
        model = Dictionary
        fields = ['name', 'language']


class VarietyForm(ModelForm):
    class Meta:
        model = Variety
        fields = ['name']


class GlossForm(ModelForm):
    class Meta:
        model = Gloss
        fields = ['primary','secondary','part_of_speech','field_tip','comment_tip']


class TranscriptionForm(ModelForm):
    class Meta:
        model = Transcription
        fields = ['ipa']


class ComparisonForm(ModelForm):
    class Meta:
        model = Comparison
        fields = ['name', 'description']
