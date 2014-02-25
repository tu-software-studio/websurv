from django.shortcuts import render, get_list_or_404
from backend.models import Dictionary, Survey, Variety

# Create your views here.
def home(request):
    return render(request, 'thin/base.html')

def dictionary_index(request):
    dictionaries = get_list_or_404(Dictionary)
    return render(request, 'thin/dictionary_index.html', {'d_lst': dictionaries})

def survey_index(request):
    surveys_list = get_list_or_404(Variety, Variety.name != null)
    context = {'surveys_list': surveys_list}
    return render(request, 'survey_index.html', context)

