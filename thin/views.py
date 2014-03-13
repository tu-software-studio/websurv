from django.contrib import messages
from django.shortcuts import render, redirect

from backend.models import Dictionary, Project, Survey, Variety

from thin import forms

def home(request):
    """Render the main home page."""
    survey = Survey.objects.get(id=1)
    dictionary = survey.dictionary
    project = dictionary.project
    breadcrumb_menu = [project,dictionary,survey]
    context = {'breadcrumb_menu':breadcrumb_menu}

    return render(request, 'thin/base.html',context)

def dictionary_add(request, id):
    """  """
    if request.method == 'POST': # If the form has been submitted
        form = forms.DictionaryForm(request.POST)
        if form.is_valid():
            form.instance.project = Project.objects.get(pk=id)
            form.save()
            messages.success(request, "Dictionary Added!")
            return redirect('project_detail', num=id)
    else:
        form = forms.DictionaryForm()
    return render(request,'thin/project_add.html', {'form' : form })

def dictionary_delete(request, id):
    try:
        dictionary = Dictionary.objects.get(pk=id)
    except Dictionary.DoesNotExist:
        messages.error(request, "Can't find the selected dictionary")
        return redirect('dictionary_index')
    dictionary.delete()
    messages.success(request, "Dictionary has been deleted!")
    return redirect('project_detail', num=dictionary.project_id)

def dictionary_detail(request, id):
    try:
        dictionary = Dictionary.objects.get(pk=id)
        project = dictionary.project
        breadcrumb_menu = [project,dictionary]
        #varieties = Variety.objects.filter(dictionary=dictionary)
    except Dictionary.DoesNotExist:
        messages.error(request, "Can't find selected dictionary.")
        return redirect('dictionary_index')
    return render(request, 'thin/dictionary_detail.html', {'dictionary' : dictionary, 'breadcrumb_menu':breadcrumb_menu })

def dictionary_edit(request, id):
    try:
        dictionary = Dictionary.objects.get(pk=id)
    except Dictionary.DoesNotExist:
        messages.error(request, "Can't find selected Dictionary.")
        return redirect('dictionary_index')
    if request.method == 'POST': # If the form has been submitted
        form = forms.DictionaryForm(request.POST,instance=dictionary)
        if form.is_valid():
            form.save()
            messages.success(request,"Dictionary has been editted successfully!")
            return redirect('dictionary_detail', id=dictionary.id)
    else:
        form = forms.DictionaryForm(instance=dictionary)
    return render(request,'thin/dictionary_edit.html', {'form' : form, 'dictionary' : dictionary })

def dictionary_index(request): 
    dictionaries = Dictionary.objects.all()
    return render(request, 'thin/dictionary_index.html', { 'dictionary_list' : dictionaries })

def project_add(request):
    if request.method == 'POST': # If the form has been submitted
        form = forms.ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Project Added!")
            return redirect('project_index')
    else:
        form = forms.ProjectForm()
    return render(request,'thin/project_add.html', {'form' : form})

def project_delete(request,num):
    project = Project.objects.get(pk=num)
    project.delete()
    messages.success(request, "Project has been deleted!")
    return redirect('project_index')

def project_detail(request, num):
    try:
        project = Project.objects.get(pk=num)
        dictionaries = Dictionary.objects.filter(project=project)
        breadcrumb_menu = [project]
    except Project.DoesNotExist:
        messages.error(request, "Can't find selected project.")
        return redirect('project_index')
    context = {'project' : project, 'dictionaries':dictionaries,'breadcrumb_menu':breadcrumb_menu }
    return render(request, 'thin/project_detail.html', context)

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
    context = {'form' : form, 'project' : project}
    return render(request,'thin/project_edit.html', context)

def project_index(request):
    projects = Project.objects.all()    
    return render(request, 'thin/project_index.html', {'project_list' : projects})

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

def survey_delete(request, id):
    survey = Survey.objects.get(id=id)
    survey.delete()
    return redirect('survey_index')

def survey_detail(request, id):
    try:
        survey = Survey.objects.get(id=id)
        varieties = Variety.objects.filter(id=survey.id)
        dictionary = survey.dictionary
        project = dictionary.project
        breadcrumb_menu = [project,dictionary,survey]
    except Survey.DoesNotExist:
        messages.error(request, "Can't find selected survey.")
        return redirect('survey_index')
    context = {'survey' : survey, 'varieties' : varieties, 'breadcrumb_menu':breadcrumb_menu}
    return render(request, 'thin/survey_detail.html', context)

def survey_edit(request,id):
    survey = Survey.objects.get(id=id)
    if request.method == 'POST': # If the form has been submitted
        form = forms.SurveyForm(request.POST, instance=survey)
        if form.is_valid():
            form.save()
            return redirect('survey_detail', id=id)
    else:
        form = forms.SurveyForm(instance=survey)
    return render(request, 'thin/survey_edit.html',
                  { 'form': form, 'survey': survey })

def survey_index(request):
    survey_list = Survey.objects.all() # TODO - only get stuff we need
    context = {'survey_list': survey_list}
    return render(request, 'thin/survey_index.html', context)

def variety_add(request):
    if request.method == 'POST': # If the form has been submitted
        form = forms.VarietyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Variety Added!")
            return redirect('project_index')
    else:
        form = forms.VarietyForm()
        messages.error(request,"Variety failed to be created")
    return render(request,'thin/variety_add.html', {'form' : form})

def variety_delete(request,num):
    variety = Variety.objects.get(pk=num)
    variety.delete()
    messages.success(request, "Variety has been deleted!")
    return redirect('variety_index')

def variety_detail(request, num):
    variety = Variety.objects.get(pk=num)
    transcripts = Transcription.objects.filter(variety=variety)
    return render(request, 'thin/variety_detail.html',{'variety':variety, 'transcripts' : transcripts})

def variety_edit(request, num):
    try:
        variety = Variety.objects.get(pk=num)
    except Variety.DoesNotExist:
        messages.error(request, "Can't find selected variety.")
        return redirect('variety_index')
    if request.method == 'POST': # If the form has been submitted
        form = forms.VarietyForm(request.POST, instance=variety)
        if form.is_valid():
            form.save()
            messages.success(request,"Variety has been editted successfully!")
            return redirect('variety_detail', num=variety.id)
    else:
        form = forms.VarietyForm(instance=variety)
    return render(request,'thin/variety_edit.html', {'form' : form, 'variety' : variety })

def variety_index(request):
    varieties = Variety.objects.all()
    return render(request, 'thin/variety_index.html', {'varieties' : varieties})

def comparison_index(request):
    pass

def comparison_detail(request, num):
    pass

def comparison_edit(request, num):
    pass
