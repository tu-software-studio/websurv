from django.contrib import messages
from django.shortcuts import render, redirect


from backend.models import *

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
    varieties = Variety.objects.all() # TODO - only get varieties from current project, dictionary and survey.
    context = {'varieties': varieties}
    return render(request, 'thin/survey_index.html', context)

def survey_detail(request, pk):
    try:
        survey = Survey.objects.get(id=pk)
        varieties = Variety.objects.filter(id=survey.id)
    except Survey.DoesNotExist:
        messages.error(request, "Can't find selected survey.")
        return redirect('survey_index')
    context = {'survey' : survey, 'varieties' : varieties}
    return render(request, 'thin/survey_detail.html', context)

def survey_edit(request,pk):
    survey = get_object_or_404(Survey, id=pk) # TODO - Use get and handle exceptions.
    if request.method == 'POST': # If the form has been submitted
        form = forms.SurveyForm(request.POST, instance=survey)
        if form.is_valid():
            form.save()
            return redirect('survey_detail', id=id)
    else:
        form = forms.SurveyForm(instance=survey)
    return render(request, 'thin/survey_edit.html',
                  { 'form': form, 'survey': survey })

def variety_index(request):
    varieties = Variety.objects.all() # TODO - only get varieties from current project, dictionary and variety.
    context = {'varieties': varieties}
    return render(request, 'thin/variety_index.html', context)

def variety_detail(request, pk):
    try:
        variety = Variety.objects.get(id=pk)
    except Variety.DoesNotExist:
        messages.error(request, "Can't find selected variety.")
        return redirect('variety_index')
    context = {'variety' : variety}
    return render(request, 'thin/variety_detail.html', context)

def survey_delete(request, id):
    survey = Survey.objects.get(id=id)
    survey.delete()
    return redirect('survey_index')

def survey_add(request):
    if request.method == 'POST': # If the form has been submitted
        form = forms.SurveyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Survey added!")
            return redirect('survey_index')
    else:
        form = forms.SurveyForm()
    return render(request, 'thin/survey_add.html', {'form': form})

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
    if request.method == 'POST': # If the form has been submitted
        form = forms.ProjectForm(request.POST,instance=project)
        if form.is_valid():
            form.save()
            messages.success(request,"Project has been editted successfully!")
            return redirect('project_detail',num=project.id)
    else:
        form = forms.ProjectForm(instance=project)
    return render(request,'thin/project_edit.html', {'form' : form, 'project' : project })

def project_add(request):
    if request.method == 'POST': # If the form has been submitted
        form = forms.ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Project Added!")
            return redirect('project_index')
    else:
        form = forms.ProjectForm()
        messages.error(request,"Project failed to be created")
    return render(request,'thin/project_add.html', {'form' : form})

def project_delete(request,num):
    project = Project.objects.get(pk=num)
    project.delete()
    messages.success(request, "Project has been deleted!")
    return redirect('project_index')

def variety_index(request):
    varieties = Variety.objects.all()
    return render(request, 'thin/variety_index.html', { 'varieties':varieties})

def variety_detail(request, num):
    variety = Variety.objects.get(pk=num)
    transcripts = Transcription.objects.filter(variety=variety)
    return render(request, 'thin/variety_detail.html',{ 'variety':variety, 'transcripts':transcripts})

def variety_edit(request, num):
    pass

def variety_add(request):

def variety_delete(request,num):
    variety = Variety.objects.get(pk=num)
    variety.delete()
    messages.success(request, "Project has been deleted!")
    return redirect('variety_index')

def comparison_index(request):
    pass

def comparison_detail(request, num):
    pass

def comparison_edit(request, num):
    pass
