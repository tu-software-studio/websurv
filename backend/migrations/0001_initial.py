# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Project'
        db.create_table(u'backend_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'backend', ['Project'])

        # Adding model 'Dictionary'
        db.create_table(u'backend_dictionary', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='dictionaries', to=orm['backend.Project'])),
        ))
        db.send_create_signal(u'backend', ['Dictionary'])

        # Adding model 'PartOfSpeech'
        db.create_table(u'backend_partofspeech', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal(u'backend', ['PartOfSpeech'])

        # Adding model 'Gloss'
        db.create_table(u'backend_gloss', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('primary', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('secondary', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('pos', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backend.PartOfSpeech'])),
            ('dictionary', self.gf('django.db.models.fields.related.ForeignKey')(related_name='glosses', to=orm['backend.Dictionary'])),
            ('field_tip', self.gf('django.db.models.fields.TextField')()),
            ('comment_tip', self.gf('django.db.models.fields.TextField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'backend', ['Gloss'])

        # Adding model 'SortOrder'
        db.create_table(u'backend_sortorder', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('dictionary', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sort_orders', to=orm['backend.Dictionary'])),
        ))
        db.send_create_signal(u'backend', ['SortOrder'])

        # Adding model 'SortPosition'
        db.create_table(u'backend_sortposition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sort', self.gf('django.db.models.fields.related.ForeignKey')(related_name='positions', to=orm['backend.SortOrder'])),
        ))
        db.send_create_signal(u'backend', ['SortPosition'])

        # Adding model 'Survey'
        db.create_table(u'backend_survey', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('dictionary', self.gf('django.db.models.fields.related.ForeignKey')(related_name='surveys', to=orm['backend.Dictionary'])),
        ))
        db.send_create_signal(u'backend', ['Survey'])

        # Adding model 'Variety'
        db.create_table(u'backend_variety', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(related_name='varieties', to=orm['backend.Survey'])),
        ))
        db.send_create_signal(u'backend', ['Variety'])

        # Adding model 'Transcription'
        db.create_table(u'backend_transcription', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ipa', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('gloss', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transcriptions', to=orm['backend.Gloss'])),
            ('variety', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tanscriptions', to=orm['backend.Variety'])),
        ))
        db.send_create_signal(u'backend', ['Transcription'])

        # Adding model 'Comparison'
        db.create_table(u'backend_comparison', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(related_name='comparisons', to=orm['backend.Survey'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'backend', ['Comparison'])

        # Adding model 'ComparisonEntry'
        db.create_table(u'backend_comparisonentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('aligned_form', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('exclude', self.gf('django.db.models.fields.BooleanField')()),
            ('comparison', self.gf('django.db.models.fields.related.ForeignKey')(related_name='entries', to=orm['backend.Comparison'])),
            ('transcription', self.gf('django.db.models.fields.related.ForeignKey')(related_name='comparison_entries', to=orm['backend.Transcription'])),
        ))
        db.send_create_signal(u'backend', ['ComparisonEntry'])


    def backwards(self, orm):
        # Deleting model 'Project'
        db.delete_table(u'backend_project')

        # Deleting model 'Dictionary'
        db.delete_table(u'backend_dictionary')

        # Deleting model 'PartOfSpeech'
        db.delete_table(u'backend_partofspeech')

        # Deleting model 'Gloss'
        db.delete_table(u'backend_gloss')

        # Deleting model 'SortOrder'
        db.delete_table(u'backend_sortorder')

        # Deleting model 'SortPosition'
        db.delete_table(u'backend_sortposition')

        # Deleting model 'Survey'
        db.delete_table(u'backend_survey')

        # Deleting model 'Variety'
        db.delete_table(u'backend_variety')

        # Deleting model 'Transcription'
        db.delete_table(u'backend_transcription')

        # Deleting model 'Comparison'
        db.delete_table(u'backend_comparison')

        # Deleting model 'ComparisonEntry'
        db.delete_table(u'backend_comparisonentry')


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