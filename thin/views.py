from django.shortcuts import render, get_list_or_404, get_object_or_404
from backend.models import Dictionary, Project, Survey, Variety
from thin import forms
from forms import SurveyForm

# Create your views here.
def home(request):
    return render(request, 'thin/base.html')


def dictionary_index(request):
    dictionaries = get_list_or_404(Dictionary)
    return render(request, 'thin/dictionary_index.html', {'d_lst': dictionaries})
    # Can't test if this'll work until the db is seeded
    #return render(request, dictionary_index, {'d_lst': dictionaries})

def survey_index(request):
    surveys_list = get_list_or_404(Variety, Variety.name != null)
    context = {'surveys_list': surveys_list}
    return render(request, 'survey_index.html', context)

def survey_edit(request, pk):
    survey = get_object_or_404(Survey, id=pk)

    if request.method == 'POST': # If the form has been submitted
        form = SurveyForm(request.POST)
        if form.is_valid():
            # TODO: Process the data in form.cleaned_data
            # ...

            return redirect(request, 'thin/survey_index.html', {'form': form, 'survey': survey})
    else:
        form = SurveyForm()
            
    return render(request, 'thin/survey_edit.html', {
        'form': form, 'survey': survey
    })


def project_index(request):
    projects = get_list_or_404(Project)
    return render(request, 'thin/project_index.html', {'project_lst' : projects})

def project_detail(request, num):
    project = get_object_or_404(Project, id=num)
    return render(request, 'thin/project_detail.html', {'project' : project})

def project_edit(request, num):
    project = get_object_or_404(Project, id=num)
    form = forms.ProjectForm(instance=project)
    return render(request,'thin/project_edit.html', {'form' : form})
