from backend.models import Project

def ProjectList(request):
    return {'request': request, 'projects': Project.objects.all()}
