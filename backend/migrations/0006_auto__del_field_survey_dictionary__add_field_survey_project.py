# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Survey.dictionary'
        db.delete_column(u'backend_survey', 'dictionary_id')

        # Adding field 'Survey.project'
        db.add_column(u'backend_survey', 'project',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='surveys', to=orm['backend.Project']),
                      keep_default=False)

        # Adding M2M table for field glosses on 'Survey'
        m2m_table_name = db.shorten_name(u'backend_survey_glosses')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('survey', models.ForeignKey(orm[u'backend.survey'], null=False)),
            ('gloss', models.ForeignKey(orm[u'backend.gloss'], null=False))
        ))
        db.create_unique(m2m_table_name, ['survey_id', 'gloss_id'])


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Survey.dictionary'
        raise RuntimeError("Cannot reverse this migration. 'Survey.dictionary' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Survey.dictionary'
        db.add_column(u'backend_survey', 'dictionary',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='surveys', to=orm['backend.Dictionary']),
                      keep_default=False)

        # Deleting field 'Survey.project'
        db.delete_column(u'backend_survey', 'project_id')

        # Removing M2M table for field glosses on 'Survey'
        db.delete_table(db.shorten_name(u'backend_survey_glosses'))


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
            'full_title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'glosses': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'surveys'", 'symmetrical': 'False', 'to': u"orm['backend.Gloss']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'surveys'", 'to': u"orm['backend.Project']"})
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
            'end_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 17, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_helper': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'language_helper_age': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'province_state': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'reliability': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 17, 0, 0)'}),
            'subdistrict': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'varieties'", 'to': u"orm['backend.Survey']"}),
            'surveyors': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'village': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['backend']