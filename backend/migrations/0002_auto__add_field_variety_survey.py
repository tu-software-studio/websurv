# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Variety.survey'
        db.add_column(u'backend_variety', 'survey',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='varieties', to=orm['backend.Survey']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Variety.survey'
        db.delete_column(u'backend_variety', 'survey_id')


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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dictionaries'", 'to': u"orm['backend.Project']"})
        },
        u'backend.gloss': {
            'Meta': {'object_name': 'Gloss'},
            'comment_tip': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dictionary': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'glosses'", 'to': u"orm['backend.Dictionary']"}),
            'field_tip': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pos': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['backend.PartOfSpeech']"}),
            'primary': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'secondary': ('django.db.models.fields.CharField', [], {'max_length': '50'})
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.TextField', [], {})
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'varieties'", 'to': u"orm['backend.Survey']"})
        }
    }

    complete_apps = ['backend']