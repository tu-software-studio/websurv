from django.contrib import messages
from django.shortcuts import render, redirect
from django.forms.formsets import formset_factory
from django.http import HttpResponse

import json

from backend.models import Dictionary, Project, Survey, Variety, Transcription, Gloss

from thin import forms

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from backend.serializers import GlossSerializer


def home(request):
    """Render the main home page."""
    survey = Survey.objects.get(id=1)
    dictionary = survey.dictionary
    project = dictionary.project
    breadcrumb_menu = [project, dictionary, survey]
    context = {'breadcrumb_menu': breadcrumb_menu}

    return render(request, 'thin/base.html', context)


def dictionary_index(request):
    dictionaries = Dictionary.objects.all()
    return render(request, 'thin/dictionary_index.html', {'dictionary_list': dictionaries})


def dictionary_detail(request, id):
    try:
        dictionary = Dictionary.objects.get(pk=id)
        surveys = Survey.objects.filter(dictionary=dictionary)
        glosses = Gloss.objects.filter(dictionary=dictionary)
    except Dictionary.DoesNotExist:
        messages.error(request, "Can't find selected dictionary.")
        return redirect('dictionary_index')
    breadcrumb_menu = [dictionary.project, dictionary]
    return render(request, 'thin/dictionary_detail.html',
                  {'dictionary': dictionary, 'breadcrumb_menu': breadcrumb_menu, 'surveys': surveys, 'glosses': glosses})


def dictionary_edit(request, id):
    try:
        dictionary = Dictionary.objects.get(pk=id)
    except Dictionary.DoesNotExist:
        messages.error(request, "Can't find selected Dictionary.")
        return redirect('dictionary_index')
    if request.method == 'POST':  # If the form has been submitted
        form = forms.DictionaryForm(request.POST, instance=dictionary)
        if form.is_valid():
            form.save()
            messages.success(request, "Dictionary has been editted successfully!")
            return redirect('dictionary_detail', id=dictionary.id)
    else:
        form = forms.DictionaryForm(instance=dictionary)
    breadcrumb_menu = [dictionary.project, dictionary]
    return render(request, 'thin/dictionary_edit.html', {'form': form, 'dictionary': dictionary, 'breadcrumb_menu': breadcrumb_menu})


def dictionary_add(request, id):
    project = Project.objects.get(pk=id)
    if request.method == 'POST':  # If the form has been submitted
        form = forms.DictionaryForm(request.POST)
        if form.is_valid():
            form.instance.project = project
            form.save()
            messages.success(request, "Dictionary Added!")
            return redirect('project_detail', num=id)
    else:
        form = forms.DictionaryForm()
    breadcrumb_menu = [project]
    return render(request, 'thin/dictionary_add.html', {'form': form, 'breadcrumb_menu': breadcrumb_menu})


def dictionary_delete(request, id):
    try:
        dictionary = Dictionary.objects.get(pk=id)
    except Dictionary.DoesNotExist:
        messages.error(request, "Can't find the selected dictionary")
        return redirect('dictionary_index')
    dictionary.delete()
    messages.success(request, "Dictionary has been deleted!")
    return redirect('project_detail', num=dictionary.project_id)


def survey_index(request):
    survey_list = Survey.objects.all()
    context = {'survey_list': survey_list}
    return render(request, 'thin/survey_index.html', context)


def survey_detail(request, id):
    try:
        survey = Survey.objects.get(id=id)
        varieties = Variety.objects.filter(id=survey.id)
    except Survey.DoesNotExist:
        messages.error(request, "Can't find selected survey.")
        return redirect('survey_index')
    breadcrumb_menu = [survey.dictionary.project, survey.dictionary, survey]
    context = {'survey': survey, 'varieties': varieties, 'breadcrumb_menu': breadcrumb_menu}
    return render(request, 'thin/survey_detail.html', context)


def survey_edit(request, id):
    survey = Survey.objects.get(id=id)
    if request.method == 'POST':  # If the form has been submitted
        form = forms.SurveyForm(request.POST, instance=survey)
        if form.is_valid():
            form.save()
            return redirect('survey_detail', id=id)
    else:
        form = forms.SurveyForm(instance=survey)
    breadcrumb_menu = [survey.dictionary.project, survey.dictionary, survey]
    return render(request, 'thin/survey_edit.html', {'form': form, 'survey': survey, 'breadcrumb_menu': breadcrumb_menu})


def survey_add(request, id):
    dictionary = Dictionary.objects.get(id=id)
    if request.method == 'POST':  # If the form has been submitted
        form = forms.SurveyForm(request.POST)
        if form.is_valid():
            form.instance.dictionary = dictionary
            survey = form.save()
            messages.success(request, "Survey added!")
            return redirect('survey_detail', id=survey.id)
    else:
        form = forms.SurveyForm()
    breadcrumb_menu = [dictionary.project, dictionary]
    return render(request, 'thin/survey_add.html', {'form': form, 'breadcrumb_menu': breadcrumb_menu})


def survey_delete(request, id):
    survey = Survey.objects.get(id=id)
    survey.delete()
    messages.success(request, "Survey has been deleted!")
    return redirect('survey_index')


def project_index(request):
    projects = Project.objects.all()
    return render(request, 'thin/project_index.html', {'project_list': projects})


def project_detail(request, num):
    try:
        project = Project.objects.get(pk=num)
        dictionaries = Dictionary.objects.filter(project=project)
        breadcrumb_menu = [project]
    except Project.DoesNotExist:
        messages.error(request, "Can't find selected project.")
        return redirect('project_index')
    return render(request, 'thin/project_detail.html',
                  {'project': project, 'dictionaries': dictionaries, 'breadcrumb_menu': breadcrumb_menu})


def project_edit(request, num):
    try:
        project = Project.objects.get(pk=num)
    except Project.DoesNotExist:
        messages.error(request, "Can't find selected project.")
        return redirect('project_index')
    if request.method == 'POST':  # If the form has been submitted
        form = forms.ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Project has been editted successfully!")
            return redirect('project_detail', num=project.id)
    else:
        form = forms.ProjectForm(instance=project)
    breadcrumb_menu = [project]
    return render(request, 'thin/project_edit.html', {'form': form, 'project': project, 'breadcrumb_menu': breadcrumb_menu})


def project_add(request):
    if request.method == 'POST':  # If the form has been submitted
        form = forms.ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Project Added!")
            return redirect('project_index')
    else:
        form = forms.ProjectForm()
    return render(request, 'thin/project_add.html', {'form': form})


def project_delete(request, num):
    project = Project.objects.get(pk=num)
    project.delete()
    messages.success(request, "Project has been deleted!")
    return redirect('project_index')


def variety_index(request):
    varieties = Variety.objects.all()
    return render(request, 'thin/variety_index.html', {'varieties': varieties})


def variety_detail(request, num):
    try:
        variety = Variety.objects.get(pk=num)
        transcripts = Transcription.objects.filter(variety=variety)
    except Survey.DoesNotExist:
        messages.error(request, "Can't find selected variety.")
        return redirect('variety_index')
    breadcrumb_menu = [variety.survey.dictionary.project, variety.survey.dictionary, variety.survey, variety]
    return render(request, 'thin/variety_detail.html',
                  {'variety': variety, 'transcripts': transcripts, 'breadcrumb_menu': breadcrumb_menu})


def variety_edit(request, num):
    try:
        variety = Variety.objects.get(pk=num)
    except Variety.DoesNotExist:
        messages.error(request, "Can't find selected variety.")
        return redirect('variety_index')
    if request.method == 'POST':  # If the form has been submitted
        form = forms.VarietyForm(request.POST, instance=variety)
        if form.is_valid():
            form.save()
            messages.success(request, "Variety has been editted successfully!")
            return redirect('variety_detail', num=variety.id)
    else:
        form = forms.VarietyForm(instance=variety)
    breadcrumb_menu = [variety.survey.dictionary.project, variety.survey.dictionary, variety.survey, variety]
    return render(request, 'thin/variety_edit.html', {'form': form, 'variety': variety, 'breadcrumb_menu': breadcrumb_menu})


def variety_add(request, id):
    survey = Survey.objects.get(pk=id)
    if request.method == 'POST':  # If the form has been submitted
        form = forms.VarietyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Variety Added!")
            return redirect('project_index')
    else:
        form = forms.VarietyForm()
        messages.error(request, "Variety failed to be created")
    breadcrumb_menu = [survey.dictionary.project, survey.dictionary, survey]
    return render(request, 'thin/variety_add.html', {'form': form, 'breadcrumb_menu': breadcrumb_menu})


def variety_delete(request, num):
    variety = Variety.objects.get(pk=num)
    variety.delete()
    messages.success(request, "Variety has been deleted!")
    return redirect('variety_index')


def comparison_index(request):
    pass


def comparison_detail(request, num):
    pass


def comparison_edit(request, num):
    pass


def gloss_index(request):
    glosses = Gloss.objects.all()
    return render(request, 'thin/gloss_index.html', {'gloss_list': glosses})


def gloss_delete(request, id):
    gloss = Gloss.objects.get(id=id)
    gloss.delete()
    messages.success(request, "Gloss has been deleted!")
    return redirect('dictionary_detail', id=gloss.dictionary_id)


def gloss_detail(request, id):
    try:
        gloss = Gloss.objects.get(pk=id)
    except Gloss.DoesNotExist:
        messages.error(request, "Can't find selected gloss.")
        return redirect('gloss_index')
    breadcrumb_menu = [gloss.dictionary.project, gloss.dictionary, gloss]
    return render(request, 'thin/gloss_detail.html', {'gloss': gloss, 'breadcrumb_menu': breadcrumb_menu})


def gloss_edit(request, id):
    try:
        gloss = Gloss.objects.get(pk=id)
    except:
        messages.error(request, "Couldn't find the selected gloss.")
        return redirect('gloss_index')
    if request.method == "POST":
        form = forms.GlossForm(request.POST, instance=gloss)
        if form.is_valid():
            form.save()
            messages.success(request, "Gloss has been updated!")
            return redirect('gloss_detail', id=gloss.id)
    else:
        form = forms.GlossForm(instance=gloss)
    breadcrumb_menu = [gloss.dictionary.project, gloss.dictionary, gloss]
    return render(request, 'thin/gloss_edit.html', {'form': form, 'gloss': gloss, 'breadcrumb_menu': breadcrumb_menu})


def gloss_add(request, id):
    form = forms.GlossForm()
    dictionary = Dictionary.objects.get(pk=id)
    breadcrumb_menu = [dictionary.project, dictionary]
    return render(request, 'thin/gloss_add.html', {'form': form, 'id': id, 'breadcrumb_menu': breadcrumb_menu})


@api_view(['POST'])
def gloss_add_with_ajax(request, id):
    serializer = GlossSerializer(data=request.DATA)
    if serializer.is_valid():
        serializer.object.dictionary = Dictionary.objects.get(pk=id)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        #for x in serializer.errors:
            #print x+" : "+ str(serializer.errors[x][0])
            #messages.error(request, x + " : " + str(serializer.errors[x][0]))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
