import factory

from backend import models
# from backend.models import Comparison, Dictionary, Gloss, PartOfSpeech, Project, Survey, Variety


# Done
class ProjectFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Project

    name = factory.Sequence(lambda n: 'Test Project {0}'.format(n))


class LanguageFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Language

    name = factory.Sequence(lambda n: 'Test Language {0}'.format(n))
    iso_code = 'USA'


class DictionaryFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Dictionary

    name = factory.Sequence(lambda n: 'Test Dictionary {0}'.format(n))
    project = factory.SubFactory(ProjectFactory)
    language = factory.SubFactory(LanguageFactory)


class SurveyFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Survey

    name = factory.Sequence(lambda n: 'Test Survey {0}'.format(n))
    full_title = factory.LazyAttribute(lambda a: 'Full Title For {0}'.format(a.name))
    project = factory.SubFactory(ProjectFactory)


class VarietyFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Variety

    name = factory.Sequence(lambda n: 'Test Variety {0}'.format(n))
    survey = factory.SubFactory(SurveyFactory)


class ComparisonFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Comparison

    name = factory.Sequence(lambda n: 'Test Comparison {0}'.format(n))
    description = factory.LazyAttribute(lambda a: 'Description for {0}'.format(a.name))
    survey = factory.SubFactory(SurveyFactory)


class PartOfSpeechFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.PartOfSpeech

    name = 'Noun'

class GlossFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Gloss

    primary = factory.Sequence(lambda n: 'primary {0}'.format(n))
    secondary = factory.Sequence(lambda n: 'secondary {0}'.format(n))
    part_of_speech = factory.SubFactory(PartOfSpeechFactory)
    dictionary = factory.SubFactory(DictionaryFactory)
    field_tip = factory.Sequence(lambda n: 'field tip {0}'.format(n))
    comment_tip = factory.Sequence(lambda n: 'comment tip {0}'.format(n))

class TranscriptionFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Transcription

    ipa = factory.Sequence(lambda n: 'ipa {0}'.format(n))
    gloss = factory.SubFactory(GlossFactory)
    variety = factory.SubFactory(VarietyFactory)
    
