from django.contrib import messages
from django.shortcuts import render, redirect
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from django.http import HttpResponse

import json

from backend.models import Comparison, ComparisonEntry, Dictionary, Project, Survey, Variety, Transcription, Gloss

from thin import forms

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from backend.serializers import GlossSerializer, ComparisonEntrySerializer


def home(request):
    """Render the main home page."""
    breadcrumb_menu = []
    context = {'breadcrumb_menu': breadcrumb_menu }
    return render(request, 'thin/base.html', context)

def dictionary_index(request):
    return redirect('home')


def dictionary_detail(request, id):
    try:
        dictionary = Dictionary.objects.get(pk=id)
        glosses = Gloss.objects.filter(dictionary=dictionary)
    except Dictionary.DoesNotExist:
        messages.error(request, "Can't find selected dictionary.")
        return redirect('dictionary_index')
    breadcrumb_menu = [dictionary.project, dictionary]
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
            messages.success(request, "Dictionary has been edited successfully!")
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
            return redirect('dictionary_detail', id=form.instance.id)
        messages.error(request, "Dictionary was not created.")
    else:
        form = forms.DictionaryForm()
    breadcrumb_menu = [project]
    return render(request, 'thin/dictionary_add.html', {'form': form, 'breadcrumb_menu': breadcrumb_menu})

# def dictionary_delete(request, id):
#     ipdb.set_trace()
#     try:
#         dictionary = Dictionary.objects.get(pk=id)
#     except Dictionary.DoesNotExist:
#         messages.error(request, "Can't find the selected dictionary")
#         return redirect('dictionary_index')
#     dictionary.delete()
#     messages.success(request, "Dictionary has been deleted!")
#     #return redirect('project_detail', id=dictionary.project.id)
#     return redirect('project_index')

def dictionary_delete(request, id):
    dictionary = Dictionary.objects.get(pk=id)
    dictionary.delete()
    messages.success(request, "Dictionary has been deleted!")
    return redirect('project_detail',id=dictionary.project.id)


def survey_index(request):
    return redirect('home')


def survey_detail(request, id):
    try:
        survey = Survey.objects.get(id=id)
        varieties = Variety.objects.filter(survey=survey)
        comparisons = Comparison.objects.filter(survey=survey)
    except Survey.DoesNotExist:
        messages.error(request, "Can't find selected survey.")
        return redirect('survey_index')
    breadcrumb_menu = [survey.project, survey]
    context = {'survey': survey, 'varieties': varieties, 'comparisons': comparisons, 'breadcrumb_menu': breadcrumb_menu}
    return render(request, 'thin/survey_detail.html', context)
#
# try:
#         survey = Survey.objects.get(id=id)
#         varieties = Variety.objects.filter(survey=survey)
#         comparisons = Comparison.objects.filter(survey=survey)
#         project = survey.project
#         breadcrumb_menu = [project, survey]
#     except Survey.DoesNotExist:
#         messages.error(request, "Can't find selected survey.")
#         return redirect('survey_index')
#     context = {'survey': survey, 'varieties': varieties, 'breadcrumb_menu': breadcrumb_menu, "comparisons": comparisons}
#     return render(request, 'thin/survey_detail.html', context)

def survey_edit(request, id):
    survey = Survey.objects.get(id=id)
    if request.method == 'POST':  # If the form has been submitted
        form = forms.SurveyForm(request.POST, instance=survey)
        if form.is_valid():
            form.save()
            return redirect('survey_detail', id=id)
    else:
        form = forms.SurveyForm(instance=survey)
    breadcrumb_menu = [survey.project, survey]
    return render(request, 'thin/survey_edit.html', {'form': form, 'survey': survey, 'breadcrumb_menu': breadcrumb_menu})


def survey_add(request, id):
    project = Project.objects.get(pk=id)
    dictionary_list = list(project.dictionaries.all())

    if request.method == 'POST':  # If the form has been submitted
        form = forms.SurveyAddForm(request.POST)
        if form.is_valid():
            form.instance.project = project
            form.save()
            dictionary_list = request.POST.getlist('dictionaries')  #dictionaries that were selected
            for x in dictionary_list:
                dictionary = Dictionary.objects.get(id=x)
                glosses = list(dictionary.glosses.all())
                for gloss in glosses:
                    form.instance.glosses.add(gloss)
            messages.success(request, "Survey added!")
            return redirect('survey_detail', id=form.instance.id)
    else:
        form = forms.SurveyAddForm()
    breadcrumb_menu = [project]
    return render(request, 'thin/survey_add.html', {'form': form, 'breadcrumb_menu': breadcrumb_menu})


def survey_delete(request, id):
    survey = Survey.objects.get(id=id)
    survey.delete()
    messages.success(request, "Survey has been deleted!")
    return redirect('project_detail', id=survey.project_id)


def project_index(request):
    projects = Project.objects.all()
    if len(projects)<1:
        messages.error(request, "There are no projects.")
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
    if len(dictionaries)<1:
        messages.error(request, 'There are currently no dictionaries for this project.')
    return render(request, 'thin/project_detail.html',
                  {'project': project, 'dictionaries': dictionaries, 'surveys': surveys, 'breadcrumb_menu': breadcrumb_menu})


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
    breadcrumb_menu = [project]
    return render(request, 'thin/project_edit.html', {'form': form, 'project': project, 'breadcrumb_menu': breadcrumb_menu})


def project_add(request):
    if request.method == 'POST':  # If the form has been submitted
        form = forms.ProjectForm(request.POST)
        if form.is_valid():
            new_project = form.save()
            messages.success(request, "Project Added!")
            #return redirect('project_index')
            return redirect('project_detail', id=new_project.id)
    else:
        form = forms.ProjectForm()
    return render(request, 'thin/project_add.html', {'form': form})


def project_delete(request, id):
    project = Project.objects.get(pk=id)
    project.delete()
    messages.success(request, "Project has been deleted!")
    return redirect('project_index')


def variety_index(request):
    return redirect('home')


def variety_detail(request, id):
    try:
        variety = Variety.objects.get(pk=id)
        surveyglosses = list(variety.survey.glosses.all())
        transcripts = Transcription.objects.filter(variety=variety)
    except Survey.DoesNotExist:
        messages.error(request, "Can't find selected variety.")
        return redirect('variety_index')
    transcriptglosses=[]
    surveyglosscopy=surveyglosses[:]
    for transcript in transcripts:
        transcriptglosses.append(transcript.gloss)
    for gloss in surveyglosscopy:
        if gloss in transcriptglosses:
            surveyglosses.remove(gloss)
    breadcrumb_menu = [variety.survey.project, variety.survey, variety]
    return render(request, 'thin/variety_detail.html',
                  {'variety': variety, 'transcripts': transcripts, 'surveyglosses' : surveyglosses, 'breadcrumb_menu': breadcrumb_menu})


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
    breadcrumb_menu = [variety.survey.project, variety.survey, variety.survey, variety]
    return render(request, 'thin/variety_edit.html', {'form': form, 'variety': variety, 'breadcrumb_menu': breadcrumb_menu})


def variety_add(request, id):
    survey = Survey.objects.get(pk=id)
    if request.method == 'POST':  # If the form has been submitted
        form = forms.VarietyForm(request.POST)
        if form.is_valid():
            form.instance.survey=survey
            variety = form.save()
            messages.success(request, "Variety Added!")
            return redirect('variety_detail', variety.id)
    else:
        form = forms.VarietyForm()
    breadcrumb_menu = [survey.project, survey]
    return render(request, 'thin/variety_add.html', {'form': form, 'breadcrumb_menu': breadcrumb_menu})


def variety_delete(request, id):
    variety = Variety.objects.get(pk=id)
    variety.delete()
    messages.success(request, "Variety has been deleted!")
    return redirect('survey_detail', variety.survey_id)


def comparison_add(request, id):
    survey = Survey.objects.get(pk=id)
    if request.method == "POST":
        form = forms.ComparisonForm(request.POST)
        if form.is_valid():
            form.instance.survey = survey
            form.save()
            form.instance.create_entries()
            messages.success(request, "Comparison Created!")
            return redirect('comparison_detail', form.instance.id)
    else:
        form = forms.ComparisonForm()
    breadcrumb_menu = [survey.project, survey]
    return render(request, "thin/comparison_add.html", {'form': form, 'breadcrumb_menu': breadcrumb_menu})



def comparison_index(request):
    return redirect('home')

@api_view(['GET','POST'])
def comparison_detail(request, id):
    def create_aligned_form(params):
        try:
            # print "in function", params
            letters = [(key,params[key]) for key in params.keys() if key[:7] == 'letter-']
            letters = sorted(letters, key=lambda item: (item[1], int(item[0][7:])))
            # print letters
            aligned_form = ''
            current_group = 1
            # print "entering loop", letters
            for letter in letters:
                # print letter
                if int(letter[1][0]) != current_group:
                    # print "next group"
                    current_group = int(letter[1][0])
                    aligned_form = aligned_form[:-1] + ','
                # print "appending letter"
                aligned_form += letter[0][7:]+'|'
            # print "returning"
            aligned_form = aligned_form[:-1]
            return aligned_form
        except Exception as e:
            print "Exception!"
            print e
    def create_aligned_form2(params):
        try:
            letters = [(key,params[key]) for key in params.keys() if key[:7] == 'letter-']
            letters = sorted(letters, key=lambda item: int(item[0][7:]))
            aligned_form = ''
            for letter in letters:
                aligned_form += letter[1][0] + ','
            return aligned_form[:-1]
        except Exception as e:
            print "Exception!"
            print e
    try:
        comparison = Comparison.objects.get(pk=id)
    except Comparison.DoesNotExist:
        messages.error(request, "Can't find selected comparison.")
        return redirect('survey_detail', id)
    if request.method == "GET":
        breadcrumb_menu = [comparison.survey.project, comparison.survey, comparison]
        context = {'comparison': comparison, 'comparison_entries': comparison.entries.all(), "breadcrumb_menu": breadcrumb_menu}
        return render(request, 'thin/comparison_detail.html', context )
    elif request.method == "POST":
        data = dict(request.DATA.iterlists())
        data['group'] = str(data['group'][0])
        data['aligned_form'] = create_aligned_form2(data)

        comparison_entry = ComparisonEntry.objects.get(transcription_id=data['trans_id'][0])

        serializer = ComparisonEntrySerializer(comparison_entry, data=data)
        if serializer.is_valid():
            serializer.object.comparison = Comparison.objects.get(pk=id)
            serializer.object.transcription = Transcription.objects.get(pk=request.DATA['trans_id'])
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print "NOOOO", serializer.errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def comparison_edit(request, id):
    try:
        comparison = Comparison.objects.get(pk=id)
    except Comparison.DoesNotExist:
        messages.error(request, "Couldn't find the selected Comparison.")
        return redirect('comparison_index')
    if request.method == "POST":
        form = forms.ComparisonForm(request.POST, instance=comparison)
        if form.is_valid():
            form.save()
            messages.success(request, "Comparison has been updated!")
            return redirect('comparison_detail', id=comparison.id)
    else:
        form = forms.ComparisonForm(instance=comparison)
    breadcrumb_menu = [comparison.survey.project, comparison.survey, comparison]
    return render(request, 'thin/comparison_edit.html', {'form': form, 'comparison': comparison, 'breadcrumb_menu': breadcrumb_menu})


def comparison_delete(request, id):
    comparison = Comparison.objects.get(id=id)
    comparison.delete()
    messages.success(request, "Comparison has been deleted!")
    return redirect('survey_detail', id=comparison.survey_id)


def gloss_index(request):
    return redirect('home')


def gloss_delete(request, id):
    gloss = Gloss.objects.get(id=id)
    gloss.delete()
    messages.success(request, "Gloss has been deleted!")
    return redirect('dictionary_detail', id=gloss.dictionary_id)


def gloss_detail(request, id):
    try:
        gloss = Gloss.objects.get(pk=id)
    except Gloss.DoesNotExist:
        return redirect('home')
    return redirect('dictionary_detail', gloss.dictionary.id)
    # breadcrumb_menu = [gloss.dictionary.project, gloss.dictionary, gloss]
    # return render(request, 'thin/gloss_detail.html', {'gloss': gloss, 'breadcrumb_menu': breadcrumb_menu})


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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def transcription_index(request):
    return redirect('home')


def transcription_delete(request, id):
    transcription = Transcription.objects.get(id=id)
    transcription.delete()
    messages.success(request, "Transcription has been deleted!")
    return redirect('dictionary_detail', id=transcription.dictionary_id)


def transcription_detail(request, id):
    try:
        transcription = Transcription.objects.get(pk=id)
    except Transcription.DoesNotExist:
        return redirect('home')
    return redirect('variety_detail', transcription.variety.id)
    # return render(request, 'thin/transcription_detail.html', {'transcription': transcription})


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
    breadcrumb_menu = [transcription.variety.survey.project, transcription.variety.survey, transcription.variety, transcription]
    return render(request, 'thin/transcription_edit.html', {'form': form, 'transcription': transcription, 'breadcrumb_menu': breadcrumb_menu})


def transcription_add(request, id):
    """
    Lists all of the glosses in a survey's variety that do
    not already have transcriptions entered into the database
    """
    variety = Variety.objects.get(pk=id)
    gloss_list = list(variety.survey.glosses.all())
    transcription_list = variety.transcriptions.all()
    for x in transcription_list: #only has glosses that don't have transcriptions in the gloss_list
        if x.gloss in gloss_list:
            gloss_list.remove(x.gloss)
    if len(gloss_list)==0: #If all of glosses have transcriptions then you can't add any more
        messages.error(request,"No transcriptions left to add in survey")
        return redirect('variety_detail', id=id)
    formset = formset_factory(forms.TranscriptionForm, extra=len(gloss_list))
    if request.method == "POST":
        formset = formset(request.POST)
        if formset.is_valid():
            counter = 0
            for form in formset:
                if form.is_valid():
                    form.instance.variety = variety
                    form.instance.gloss = gloss_list[counter]
                    if form.instance.ipa != "":
                        form.save()
                counter += 1
        return redirect('variety_detail', id=id)
    breadcrumb_menu = [variety.survey.project, variety.survey, variety]
    return render(request, 'thin/transcription_add.html', {'formset': formset, 'id': id, 'gloss_list': gloss_list, 'breadcrumb_menu': breadcrumb_menu})

def transcription_edit(request, id):
    """
    Lets a single transcription IPA to be editted
    """
    try:
        transcription = Transcription.objects.get(pk=id)
    except Transcription.DoesNotExist:
        messages.error(request, "Can't find selected transcription.")
        return redirect('transcription_index')
    if request.method == 'POST':  # If the form has been submitted
        form = forms.TranscriptionForm(request.POST, instance=transcription)
        if form.is_valid():
            form.save()
            messages.success(request, "Transcription has been editted successfully!")
            return redirect('variety_detail', id=transcription.variety.id)
    else:
        form = forms.TranscriptionForm(instance=transcription)
    breadcrumb_menu = [transcription.variety.survey.project, transcription.variety.survey, transcription.variety, transcription]
    return render(request, 'thin/transcription_edit.html', {'form': form, 'transcription': transcription, 'breadcrumb_menu': breadcrumb_menu})
