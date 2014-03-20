from django.contrib import admin
from backend.models import *


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'iso_code')
    search_fields = ('name', 'iso_code')


class DictionaryAdmin(admin.ModelAdmin):
    list_display = ('name', 'project',)
    search_fields = ('name', 'project',)


class SurveyAdmin(admin.ModelAdmin):
    list_display = ('name', 'full_title', 'dictionary',)
    search_fields = ('name', 'full_title', 'dictionary',)


class PartOfSpeechAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class GlossAdmin(admin.ModelAdmin):
    list_display = ('primary', 'secondary', 'pos', 'dictionary', 'created_at',)
    search_fields = ('primary', 'secondary', 'pos', 'dictionary', 'created_at',)


class SortOrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'dictionary',)
    search_fields = ('name', 'dictionary',)


class SortPositionAdmin(admin.ModelAdmin):
    list_display = ('sort',)
    search_fields = ('sort',)


class VarietyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class TranscriptionAdmin(admin.ModelAdmin):
    list_display = ('ipa', 'gloss', 'variety',)
    search_fields = ('ipa', 'gloss', 'variety',)


class ComparisonAdmin(admin.ModelAdmin):
    list_display = ('name', 'survey',)
    search_fields = ('name', 'survey',)


class ComparisonEntryAdmin(admin.ModelAdmin):
    list_display = ('aligned_form', 'exclude', 'comparison', 'transcription',)
    search_fields = ('aligned_form', 'exclude', 'comparison', 'transcription',)


admin.site.register(Project, ProjectAdmin)
admin.site.register(Dictionary, DictionaryAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(PartOfSpeech, PartOfSpeechAdmin)
admin.site.register(Gloss, GlossAdmin)
admin.site.register(SortOrder, SortOrderAdmin)
admin.site.register(SortPosition, SortPositionAdmin)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(Variety, VarietyAdmin)
admin.site.register(Transcription, TranscriptionAdmin)
admin.site.register(Comparison, ComparisonAdmin)
admin.site.register(ComparisonEntry, ComparisonEntryAdmin)
