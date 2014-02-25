from django.shortcuts import render, get_list_or_404
from backend.models import Dictionary
from backend.models import Project
from thin import forms

# Create your views here.
def home(request):
    return render(request, 'thin/base.html')

def dictionary_index(request):
    dictionaries = get_list_or_404(Dictionary)
    return render(request, 'thin/dictionary_index.html', {'d_lst': dictionaries})

def project_index(request):
    projects = get_list_or_404(Project)
    return render(request, 'thin/project_index.html', {'project_lst' : projects})

def project_detail(request, num):
    project = Project.objects.get(id=num)
    return render(request, 'thin/project_detail.html', {'project' : project})

def project_edit(request, num):
    project = Project.objects.get(id=num)
    form = forms.ProjectForm(instance=project)
    return render(request,'thin/project_edit.html', {'form' : form})
