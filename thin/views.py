from django.contrib import messages
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404

from backend.models import Dictionary, Project, Survey

from forms import SurveyForm
from thin import forms

def home(request):
    """Render the main home page."""
    survey = Survey.objects.get(id=1)
    dictionary = survey.dictionary
    project = dictionary.project
    breadcrumb_menu = [project,dictionary,survey]
    context = {'breadcrumb_menu':breadcrumb_menu}
    return render(request, 'thin/base.html',context)

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
    projects = Project.objects.all()    
    return render(request, 'thin/project_index.html', {'project_list' : projects})

def project_detail(request, num):
    try:
        project = Project.objects.get(pk=num)
        dictionaries = Dictionary.objects.filter(project=project)
    except Project.DoesNotExist:
        messages.error(request, "Can't find selected project.")
        return redirect('project_index')
    return render(request, 'thin/project_detail.html', {'project' : project, 'dictionaries':dictionaries})

def project_edit(request, num):
    try:
        project = Project.objects.get(pk=num)
    except Project.DoesNotExist:
        messages.error(request, "Can't find selected project.")
        return redirect('project_index')
    form = forms.ProjectForm(instance=project)
    return render(request,'thin/project_edit.html', {'form' : form, 'project' : project })

def variety_index(request):
    pass

def variety_detail(request, num):
    pass

def variety_edit(request, num):
    pass

def comparison_index(request):
    pass

def comparison_detail(request, num):
    pass

def comparison_edit(request, num):
    pass
