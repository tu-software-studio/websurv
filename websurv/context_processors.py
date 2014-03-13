from backend.models import Project

def ProjectList(request):
    return {'projects':Project.objects.all()}
