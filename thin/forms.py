from django import forms
from backend.models import Project
from django.forms import ModelForm


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name']
