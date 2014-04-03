import factory

from backend import models
# from backend.models import Comparison, Dictionary, Gloss, PartOfSpeech, Project, Survey, Variety


# Done
class ProjectFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Project

    name = factory.Sequence(lambda n: 'Test Project {0}'.format(n))


class LanguageFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Language

    name = 'English'
    iso_code = 'USA'


class DictionaryFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Dictionary

    name = factory.Sequence(lambda n: 'Test Dictionary {0}'.format(n))
    project = factory.SubFactory(ProjectFactory)
    language = factory.SubFactory(LanguageFactory)
