# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Variety.description'
        db.add_column(u'backend_variety', 'description',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Variety.start_date'
        db.add_column(u'backend_variety', 'start_date',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 4, 3, 0, 0)),
                      keep_default=False)

        # Adding field 'Variety.end_date'
        db.add_column(u'backend_variety', 'end_date',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 4, 3, 0, 0)),
                      keep_default=False)

        # Adding field 'Variety.surveyors'
        db.add_column(u'backend_variety', 'surveyors',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Variety.consultants'
        db.add_column(u'backend_variety', 'consultants',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Variety.language_helper'
        db.add_column(u'backend_variety', 'language_helper',
                      self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Variety.language_helper_age'
        db.add_column(u'backend_variety', 'language_helper_age',
                      self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Variety.reliability'
        db.add_column(u'backend_variety', 'reliability',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Variety.village'
        db.add_column(u'backend_variety', 'village',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Variety.province_state'
        db.add_column(u'backend_variety', 'province_state',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Variety.district'
        db.add_column(u'backend_variety', 'district',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Variety.subdistrict'
        db.add_column(u'backend_variety', 'subdistrict',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Variety.country'
        db.add_column(u'backend_variety', 'country',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Variety.coordinates'
        db.add_column(u'backend_variety', 'coordinates',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Variety.description'
        db.delete_column(u'backend_variety', 'description')

        # Deleting field 'Variety.start_date'
        db.delete_column(u'backend_variety', 'start_date')

        # Deleting field 'Variety.end_date'
        db.delete_column(u'backend_variety', 'end_date')

        # Deleting field 'Variety.surveyors'
        db.delete_column(u'backend_variety', 'surveyors')

        # Deleting field 'Variety.consultants'
        db.delete_column(u'backend_variety', 'consultants')

        # Deleting field 'Variety.language_helper'
        db.delete_column(u'backend_variety', 'language_helper')

        # Deleting field 'Variety.language_helper_age'
        db.delete_column(u'backend_variety', 'language_helper_age')

        # Deleting field 'Variety.reliability'
        db.delete_column(u'backend_variety', 'reliability')

        # Deleting field 'Variety.village'
        db.delete_column(u'backend_variety', 'village')

        # Deleting field 'Variety.province_state'
        db.delete_column(u'backend_variety', 'province_state')

        # Deleting field 'Variety.district'
        db.delete_column(u'backend_variety', 'district')

        # Deleting field 'Variety.subdistrict'
        db.delete_column(u'backend_variety', 'subdistrict')

        # Deleting field 'Variety.country'
        db.delete_column(u'backend_variety', 'country')

        # Deleting field 'Variety.coordinates'
        db.delete_column(u'backend_variety', 'coordinates')


    models = {
        u'backend.comparison': {
            'Meta': {'object_name': 'Comparison'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comparisons'", 'to': u"orm['backend.Survey']"})
        },
        u'backend.comparisonentry': {
            'Meta': {'object_name': 'ComparisonEntry'},
            'aligned_form': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'comparison': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': u"orm['backend.Comparison']"}),
            'exclude': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'transcription': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comparison_entries'", 'to': u"orm['backend.Transcription']"})
        },
        u'backend.dictionary': {
            'Meta': {'object_name': 'Dictionary'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'languages'", 'to': u"orm['backend.Language']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dictionaries'", 'to': u"orm['backend.Project']"})
        },
        u'backend.gloss': {
            'Meta': {'object_name': 'Gloss'},
            'comment_tip': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dictionary': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'glosses'", 'to': u"orm['backend.Dictionary']"}),
            'field_tip': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'part_of_speech': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['backend.PartOfSpeech']"}),
            'primary': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'secondary': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'backend.language': {
            'Meta': {'object_name': 'Language'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'})
        },
        u'backend.partofspeech': {
            'Meta': {'object_name': 'PartOfSpeech'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'backend.project': {
            'Meta': {'object_name': 'Project'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'backend.sortorder': {
            'Meta': {'object_name': 'SortOrder'},
            'dictionary': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sort_orders'", 'to': u"orm['backend.Dictionary']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'backend.sortposition': {
            'Meta': {'object_name': 'SortPosition'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sort': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'positions'", 'to': u"orm['backend.SortOrder']"})
        },
        u'backend.survey': {
            'Meta': {'object_name': 'Survey'},
            'dictionary': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'surveys'", 'to': u"orm['backend.Dictionary']"}),
            'full_title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'backend.transcription': {
            'Meta': {'object_name': 'Transcription'},
            'gloss': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transcriptions'", 'to': u"orm['backend.Gloss']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipa': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'variety': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tanscriptions'", 'to': u"orm['backend.Variety']"})
        },
        u'backend.variety': {
            'Meta': {'object_name': 'Variety'},
            'consultants': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'coordinates': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'district': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 3, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_helper': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'language_helper_age': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'province_state': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'reliability': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 3, 0, 0)'}),
            'subdistrict': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'varieties'", 'to': u"orm['backend.Survey']"}),
            'surveyors': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'village': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['backend']