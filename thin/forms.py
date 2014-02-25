from django import forms
from django.forms import ModelForm

from backend.models import Project, Dictionary

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name']


class SurveyForm(ModelForm):
    class Meta:
        model = Dictionary
        fields = '__all__'      # TODO - Check whether this is necessary; default behavior?
