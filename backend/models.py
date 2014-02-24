from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class Dictionary(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, related_name='dictionaries')

    class Meta:
        verbose_name_plural = 'dictionaries'

    def __unicode__(self):
        return self.name

class PartOfSpeech(models.Model):
    name = models.CharField(max_length=40)

    def __unicode__(self):
        return self.name

class Gloss(models.Model):
    primary = models.CharField(max_length=50)
    secondary = models.CharField(max_length=50)
    pos = models.ForeignKey(PartOfSpeech)
    dictionary = models.ForeignKey(Dictionary, related_name='glosses')
    field_tip = models.TextField()
    comment_tip = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

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
    name = models.CharField(max_length=100)
    title = models.TextField()
    dictionary = models.ForeignKey(Dictionary, related_name='surveys')

    def __unicode__(self):
        return self.name

class Variety(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class Transcription(models.Model):
    ipa = models.CharField(max_length = 100)
    gloss = models.ForeignKey(Gloss, related_name='transcriptions')
    variety = models.ForeignKey(Variety, related_name='tanscriptions')

    def __unicode__(self):
        return self.ipa

class Comparison(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    survey = models.ForeignKey(Survey, related_name='comparisons')
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

class ComparisonEntry(models.Model):
    aligned_form = models.CharField(max_length=100)
    exclude = models.BooleanField()
    comparison = models.ForeignKey(Comparison, related_name='entries')
    transcription = models.ForeignKey(Transcription, related_name='comparison_entries')

    def __unicode__(self):
        return self.aligned_form


