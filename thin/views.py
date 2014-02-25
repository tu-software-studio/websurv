from django.contrib import messages
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404

from backend.models import Dictionary, Project, Survey

from forms import SurveyForm
from thin import forms

def home(request):
    """Render the main home page."""
    return render(request, 'thin/base.html')

def dictionary_index(request):
    dictionaries = Dictionary.objects.all() # TODO - only get dictionaries for current project.
    return render(request, 'thin/dictionary_index.html', {'dict_list': dictionaries})

def dictionary_detail(request, id):
    pass

def dictionary_edit(request, id):
    pass

def survey_index(request):
    variety_list = Variety.objects.all() # TODO - only get varieties from current dictionary and survey.
    context = {'variety_list': variety_list}
    return render(request, 'thin/survey_index.html', context)

def survey_detail(request, id):
    pass

def survey_edit(request, pk):
    survey = get_object_or_404(Survey, id=pk) # TODO - Use get and handle exceptions.

    if request.method == 'POST': # If the form has been submitted
        form = SurveyForm(request.POST)
        if form.is_valid():
            # TODO: Process the data in form.cleaned_data
            # ...

            return redirect(request, 'thin/survey_index.html', {'form': form, 'survey': survey})
    else:
        form = SurveyForm()

    return render(request, 'thin/survey_edit.html',
                  { 'form': form, 'survey': survey })

def project_index(request):
    projects = get_list_or_404(Project)                                           # TODO - Use objects.all
    return render(request, 'thin/project_index.html', {'project_lst' : projects}) # TODO - lst => list

def project_detail(request, num):
    try:
        project = Project.objects.get(pk=num)
    except Project.DoesNotExist:
        messages.error(request, "Can't find selected project.")
        return redirect('project_index')
    return render(request, 'thin/project_detail.html', {'project' : project})

def project_edit(request, num):
    project = get_object_or_404(Project, id=num) # TODO
    form = forms.ProjectForm(instance=project)
    return render(request,'thin/project_edit.html', {'form' : form})
