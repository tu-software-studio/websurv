from django.contrib import messages
from django.shortcuts import render, redirect
from django.forms.formsets import formset_factory 
from django.forms.models import modelformset_factory
from django.http import HttpResponse

import json

from backend.models import Comparison, Dictionary, Project, Survey, Variety, Transcription, Gloss

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
        project = dictionary.project
        breadcrumb_menu = [project, dictionary]
        glosses = Gloss.objects.filter(dictionary=dictionary)
    except Dictionary.DoesNotExist:
        messages.error(request, "Can't find selected dictionary.")
        return redirect('dictionary_index')
    return render(request, 'thin/dictionary_detail.html',
                  {'dictionary': dictionary, 'breadcrumb_menu': breadcrumb_menu, 'glosses': glosses})


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
    return render(request, 'thin/dictionary_edit.html', {'form': form, 'dictionary': dictionary})


def dictionary_add(request, id):
    """  """
    if request.method == 'POST':  # If the form has been submitted
        form = forms.DictionaryForm(request.POST)
        if form.is_valid():
            form.instance.project = Project.objects.get(pk=id)
            form.save()
            messages.success(request, "Dictionary Added!")
            return redirect('project_detail', id=id)
    else:
        form = forms.DictionaryForm()
    return render(request, 'thin/dictionary_add.html', {'form': form})


def dictionary_delete(request, id):
    try:
        dictionary = Dictionary.objects.get(pk=id)
    except Dictionary.DoesNotExist:
        messages.error(request, "Can't find the selected dictionary")
        return redirect('dictionary_index')
    dictionary.delete()
    messages.success(request, "Dictionary has been deleted!")
    return redirect('project_detail', id=dictionary.project_id)


def survey_index(request):
    survey_list = Survey.objects.all()  # TODO - only get stuff we need
    context = {'survey_list': survey_list}
    return render(request, 'thin/survey_index.html', context)


def survey_detail(request, id):
    try:
        survey = Survey.objects.get(id=id)
        varieties = Variety.objects.filter(survey=survey)
        project = survey.project
        breadcrumb_menu = [project, survey]
    except Survey.DoesNotExist:
        messages.error(request, "Can't find selected survey.")
        return redirect('survey_index')
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
    return render(request, 'thin/survey_edit.html',
                  {'form': form, 'survey': survey})

def survey_add(request, id):
    project=Project.objects.get(pk=id)
    dictionary_list=list(project.dictionaries.all())

    if request.method == 'POST':  # If the form has been submitted
        form = forms.SurveyAddForm(request.POST)
        if form.is_valid():
            form.instance.project = Project.objects.get(id=id)
            form.save()
            dictionary_list = request.POST.getlist('dictionaries') #dictionaries that were selected
            for x in dictionary_list:
                dictionary = Dictionary.objects.get(id=x)
                glosses=list(dictionary.glosses.all())
                for gloss in glosses:
                    form.instance.glosses.add(gloss)
            messages.success(request, "Survey added!")
            return redirect('survey_detail', id=form.instance.id)
    else:
        form = forms.SurveyAddForm()
    return render(request, 'thin/survey_add.html', {'form': form })


def survey_delete(request, id):
    survey = Survey.objects.get(id=id)
    survey.delete()
    messages.success(request, "Survey has been deleted!")
    return redirect('survey_index')


def project_index(request):
    projects = Project.objects.all()
    return render(request, 'thin/project_index.html', {'project_list': projects})


def project_detail(request, id):
    try:
        project = Project.objects.get(pk=id)
        dictionaries = Dictionary.objects.filter(project=project)
        surveys = Survey.objects.filter(project=project)
        breadcrumb_menu = [project]
    except Project.DoesNotExist:
        messages.error(request, "Can't find selected project.")
        return redirect('project_index')
    return render(request, 'thin/project_detail.html',
                  {'project': project, 'dictionaries': dictionaries, 'surveys':surveys, 'breadcrumb_menu': breadcrumb_menu})


def project_edit(request, id):
    try:
        project = Project.objects.get(pk=id)
    except Project.DoesNotExist:
        messages.error(request, "Can't find selected project.")
        return redirect('project_index')
    if request.method == 'POST':  # If the form has been submitted
        form = forms.ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Project has been editted successfully!")
            return redirect('project_detail', id=project.id)
    else:
        form = forms.ProjectForm(instance=project)
    return render(request, 'thin/project_edit.html', {'form': form, 'project': project})


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


def project_delete(request, id):
    project = Project.objects.get(pk=id)
    project.delete()
    messages.success(request, "Project has been deleted!")
    return redirect('project_index')


def variety_index(request):
    varieties = Variety.objects.all()
    return render(request, 'thin/variety_index.html', {'varieties': varieties})


def variety_detail(request, id):
    try:
        variety = Variety.objects.get(pk=id)
        transcripts = Transcription.objects.filter(variety=variety)
        survey = variety.survey
        project = survey.project
        breadcrumb_menu = [project, survey, variety]
    except Survey.DoesNotExist:
        messages.error(request, "Can't find selected variety.")
        return redirect('variety_index')
    return render(request, 'thin/variety_detail.html',
                  {'variety': variety, 'transcripts': transcripts, 'breadcrumb_menu': breadcrumb_menu})


def variety_edit(request, id):
    try:
        variety = Variety.objects.get(pk=id)
    except Variety.DoesNotExist:
        messages.error(request, "Can't find selected variety.")
        return redirect('variety_index')
    if request.method == 'POST':  # If the form has been submitted
        form = forms.VarietyForm(request.POST, instance=variety)
        if form.is_valid():
            form.save()
            messages.success(request, "Variety has been editted successfully!")
            return redirect('variety_detail', id=variety.id)
    else:
        form = forms.VarietyForm(instance=variety)
    return render(request, 'thin/variety_edit.html', {'form': form, 'variety': variety})


def variety_add(request, id):
    if request.method == 'POST':  # If the form has been submitted
        survey=Survey.objects.get(pk=id)
        form = forms.VarietyForm(request.POST)
        if form.is_valid():
            form.instance.survey=survey
            form.save()
            messages.success(request, "Variety Added!")
            return redirect('survey_detail', id)
    else:
        form = forms.VarietyForm()
    return render(request, 'thin/variety_add.html', {'form': form})


def variety_delete(request, id):
    variety = Variety.objects.get(pk=id)
    variety.delete()
    messages.success(request, "Variety has been deleted!")
    return redirect('variety_index')


def comparison_index(request):
    return render(request, 'thin/comparison_index.html')


def comparison_detail(request, id):
    try:
        comparison = Comparison.objects.get(pk=id)
    except Comparison.DoesNotExist:
        messages.error(request, "Can't find selected comparison.")
        return redirect('comparison_index')
    return render(request, 'thin/comparison_detail.html', {'comparison' : comparison})


def comparison_edit(request, id):
    try:
        comparison = Comparison.objects.get(pk=id)
    except Comparison.DoesNotExist:
        messages.error(request, "Can't find the selected comparison.")
        return redirect('comparison_index')
    return render(request, 'thin/comparison_edit.html', {'comparison' : comparison})


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
    return render(request, 'thin/gloss_detail.html', {'gloss': gloss})


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
    return render(request, 'thin/gloss_edit.html', {'form': form, 'gloss': gloss})


def gloss_add(request, id):
    form = forms.GlossForm()
    return render(request, 'thin/gloss_add.html', {'form': form, 'id': id})

@api_view(['POST'])
def gloss_add_with_ajax(request, id):
    serializer = GlossSerializer(data=request.DATA)
    if serializer.is_valid():
        serializer.object.dictionary = Dictionary.objects.get(pk=id)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def transcription_index(request):
    transcriptions = Transcription.objects.all()
    return render(request, 'thin/transcription_index.html', {'transcription_list': transcriptions})


def transcription_delete(request, id):
    transcription = Transcription.objects.get(id=id)
    transcription.delete()
    messages.success(request, "Transcription has been deleted!")
    return redirect('dictionary_detail', id=transcription.dictionary_id)


def transcription_detail(request, id):
    try:
        transcription = Transcription.objects.get(pk=id)
    except Transcription.DoesNotExist:
        messages.error(request, "Can't find selected transcription.")
        return redirect('transcription_index')
    return render(request, 'thin/transcription_detail.html', {'transcription': transcription})


def transcription_edit(request, id):
    try:
        transcription = Transcription.objects.get(pk=id)
    except:
        messages.error(request, "Couldn't find the selected transcription.")
        return redirect('transcription_index')
    if request.method == "POST":
        form = forms.TranscriptionForm(request.POST, instance=transcription)
        if form.is_valid():
            form.save()
            messages.success(request, "Transcription has been updated!")
            return redirect('transcription_detail', id=transcription.id)
    else:
        form = forms.TranscriptionForm(instance=transcription)
    return render(request, 'thin/transcription_edit.html', {'form': form, 'transcription': transcription})


#form = forms.VarietyForm(request.POST, instance=variety)


def transcription_add(request, id):
    """ Lists all of the glosses in a survey's variety that do 
        not already have transcriptions entered into the database
    """
    variety = Variety.objects.get(pk=id)
    
    gloss_list=variety.survey.glosses.all()
    formset = formset_factory(forms.TranscriptionForm, extra=len(gloss_list))
    #ipdb.set_trace()
    if request.method == "POST":
        formset = formset(request.POST)
        if formset.is_valid():
            counter=0
            for form in formset:
               if form.is_valid():
                    form.instance.variety=variety                
                    form.instance.gloss=gloss_list[counter]
                    if form.instance.ipa!="":
                        form.save()
               counter +=1     

        return redirect('variety_detail', id=id)
    return render(request, 'thin/transcription_add.html', {'formset': formset, 'id': id, 'gloss_list' : gloss_list})
