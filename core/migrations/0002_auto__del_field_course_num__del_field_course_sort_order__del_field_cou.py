# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Course.num'
        db.delete_column('core_course', 'num')

        # Deleting field 'Course.sort_order'
        db.delete_column('core_course', 'sort_order')

        # Deleting field 'Course.admin'
        db.delete_column('core_course', 'admin')

        # Deleting field 'Course.ou'
        db.delete_column('core_course', 'ou')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Course.num'
        raise RuntimeError("Cannot reverse this migration. 'Course.num' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Course.sort_order'
        raise RuntimeError("Cannot reverse this migration. 'Course.sort_order' and its values cannot be restored.")
        # Adding field 'Course.admin'
        db.add_column('core_course', 'admin',
                      self.gf('django.db.models.fields.CharField')(max_length=42, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Course.ou'
        db.add_column('core_course', 'ou',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.campusorgtype': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'CampusOrgType'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 22, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 22, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'}),
            'sort_order': ('django.db.models.fields.FloatField', [], {})
        },
        'core.course': {
            'Meta': {'object_name': 'Course'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 22, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 22, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'core.edit': {
            'Meta': {'object_name': 'Edit'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 22, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'core.employmenttype': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'EmploymentType'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 22, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 22, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'}),
            'sort_order': ('django.db.models.fields.FloatField', [], {})
        },
        'core.eventtype': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'EventType'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 22, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 22, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'}),
            'sort_order': ('django.db.models.fields.FloatField', [], {})
        },
        'core.graduationyear': {
            'Meta': {'object_name': 'GraduationYear'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 22, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 22, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.PositiveSmallIntegerField', [], {'unique': 'True'})
        },
        'core.industry': {
            'Meta': {'ordering': "['name']", 'object_name': 'Industry'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 22, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 22, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'})
        },
        'core.language': {
            'Meta': {'object_name': 'Language'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 22, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 22, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '42'}),
            'name_and_level': ('django.db.models.fields.CharField', [], {'max_length': '42'})
        },
        'core.location': {
            'Meta': {'ordering': "['name']", 'object_name': 'Location'},
            'building_num': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'keywords': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'core.question': {
            'Meta': {'ordering': "['sort_order', 'question']", 'object_name': 'Question'},
            'answer': ('django.db.models.fields.TextField', [], {}),
            'audience': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'click_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 22, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 22, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'sort_order': ('django.db.models.fields.FloatField', [], {}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Topic']"})
        },
        'core.schoolyear': {
            'Meta': {'object_name': 'SchoolYear'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 22, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 22, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'}),
            'name_plural': ('django.db.models.fields.CharField', [], {'max_length': '43', 'unique': 'True', 'null': 'True'})
        },
        'core.topic': {
            'Meta': {'ordering': "['sort_order', 'name']", 'object_name': 'Topic'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 22, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 22, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'}),
            'sort_order': ('django.db.models.fields.FloatField', [], {})
        },
        'core.tutorial': {
            'Meta': {'ordering': "['audience', 'topic', 'sort_order']", 'object_name': 'Tutorial'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'audience': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 22, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 22, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'}),
            'sort_order': ('django.db.models.fields.FloatField', [], {}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Topic']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['core']