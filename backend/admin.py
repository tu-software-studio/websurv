from django.contrib import admin
from backend.models import *


class SurveyAdminInline(admin.TabularInline):
    model = Survey


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'iso_code')
    search_fields = ('name', 'iso_code')


class DictionaryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'project')


class SurveyAdmin(admin.ModelAdmin):
    list_display = ('name', 'full_title', )
    search_fields = ('name', 'full_title', )


class PartOfSpeechAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class GlossAdmin(admin.ModelAdmin):
    list_display = ('primary', 'secondary', 'part_of_speech', 'survey', 'dictionary', 'created_at',)
    search_fields = ('primary', 'secondary', 'part_of_speech', 'survey' 'dictionary', 'created_at',)


class SortOrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'dictionary')
    search_fields = ('name', 'dictionary')


class SortPositionAdmin(admin.ModelAdmin):
    list_display = ('sort',)
    search_fields = ('sort',)


class VarietyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class TranscriptionAdmin(admin.ModelAdmin):
    list_display = ('ipa', 'gloss', 'variety')
    search_fields = ('ipa', 'gloss', 'variety')


class ComparisonAdmin(admin.ModelAdmin):
    list_display = ('name', 'survey')
    search_fields = ('name', 'survey')


class ComparisonEntryAdmin(admin.ModelAdmin):
    list_display = ('aligned_form', 'exclude', 'group', 'comparison', 'transcription')
    search_fields = ('aligned_form', 'exclude', 'group', 'comparison', 'transcription')


admin.site.register(Project, ProjectAdmin)
admin.site.register(Dictionary)
admin.site.register(Language)
admin.site.register(PartOfSpeech)
admin.site.register(Gloss)
admin.site.register(SortOrder)
admin.site.register(SortPosition)
admin.site.register(Survey)
admin.site.register(Variety)
admin.site.register(Transcription)
admin.site.register(Comparison)
admin.site.register(ComparisonEntry)
