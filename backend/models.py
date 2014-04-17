from django.core.urlresolvers import reverse
from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project_detail', args=[str(self.id)])


class Language(models.Model):
    name = models.CharField(max_length=20, null=True)
    iso_code = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.name.capitalize()


class Dictionary(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, related_name='dictionaries')
    language = models.ForeignKey(Language, related_name='languages')

    class Meta:
        verbose_name_plural = 'Dictionaries'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('dictionary_detail', args=[str(self.id)])


class PartOfSpeech(models.Model):
    name = models.CharField(max_length=40)

    class Meta:
        verbose_name_plural = 'Parts of Speech'

    def __unicode__(self):
        return self.name


class Gloss(models.Model):
    primary = models.CharField(max_length=50)
    secondary = models.CharField(max_length=50, blank=True, null=True)
    part_of_speech = models.ForeignKey(PartOfSpeech)
    dictionary = models.ForeignKey(Dictionary, related_name='glosses')
    field_tip = models.TextField(blank=True, null=True)
    comment_tip = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Glosses'

    def __unicode__(self):
        return self.primary


class SortOrder(models.Model):
    name = models.CharField(max_length=100)
    dictionary = models.ForeignKey(Dictionary, related_name='sort_orders')

    def __unicode__(self):
        return self.name


class SortPosition(models.Model):
    sort = models.ForeignKey(SortOrder, related_name='positions')

    def __unicode__(self):
        return self.name


class Survey(models.Model):
    name = models.CharField(max_length=20)
    full_title = models.CharField(max_length=100)
    project = models.ForeignKey(Project, related_name='surveys')
    glosses = models.ManyToManyField(Gloss, related_name='surveys')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('survey_detail', args=[str(self.id)])


def get_time():
    from datetime import datetime
    import pytz

    return pytz.utc.localize(datetime.utcnow())


class Variety(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateTimeField(default=get_time)
    end_date = models.DateTimeField(default=get_time)
    surveyors = models.CharField(max_length=100, blank=True, null=True)
    consultants = models.CharField(max_length=100, blank=True, null=True)
    language_helper = models.CharField(max_length=30, blank=True, null=True)
    language_helper_age = models.CharField(max_length=3, blank=True, null=True)
    reliability = models.CharField(max_length=100, blank=True, null=True)
    village = models.CharField(max_length=100, blank=True, null=True)
    province_state = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    subdistrict = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    coordinates = models.CharField(max_length=100, blank=True, null=True)

    survey = models.ForeignKey(Survey, related_name='varieties')

    class Meta:
        verbose_name_plural = 'Varieties'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('variety_detail', args=[str(self.id)])


class Transcription(models.Model):
    ipa = models.CharField(max_length=100)
    gloss = models.ForeignKey(Gloss, related_name='transcriptions')
    variety = models.ForeignKey(Variety, related_name='tanscriptions')

    def __unicode__(self):
        return self.ipa

    def get_absolute_url(self):
        return reverse("transcription_detail", args=[str(self.id)])


class Comparison(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    survey = models.ForeignKey(Survey, related_name='comparisons')
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('comparison_detail', args=[str(self.id)])


class ComparisonEntry(models.Model):
    aligned_form = models.CharField(max_length=100)
    exclude = models.BooleanField()
    comparison = models.ForeignKey(Comparison, related_name='entries')
    transcription = models.ForeignKey(Transcription, related_name='comparison_entries')

    class Meta:
        verbose_name_plural = 'Comaparison Entries'

    def __unicode__(self):
        return self.aligned_form


