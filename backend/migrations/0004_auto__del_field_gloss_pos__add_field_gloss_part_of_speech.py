# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Gloss.pos'
        db.delete_column(u'backend_gloss', 'pos_id')

        # Adding field 'Gloss.part_of_speech'
        db.add_column(u'backend_gloss', 'part_of_speech',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['backend.PartOfSpeech']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Gloss.pos'
        db.add_column(u'backend_gloss', 'pos',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['backend.PartOfSpeech']),
                      keep_default=False)

        # Deleting field 'Gloss.part_of_speech'
        db.delete_column(u'backend_gloss', 'part_of_speech_id')


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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'varieties'", 'to': u"orm['backend.Survey']"})
        }
    }

    complete_apps = ['backend']