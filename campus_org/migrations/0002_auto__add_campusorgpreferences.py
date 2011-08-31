# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'campusOrgPreferences'
        db.create_table('campus_org_campusorgpreferences', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 8, 30, 23, 12, 17, 689000), auto_now=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 8, 30, 23, 12, 17, 689000), auto_now_add=True, blank=True)),
            ('campu_org', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['campus_org.CampusOrg'], unique=True)),
        ))
        db.send_create_signal('campus_org', ['campusOrgPreferences'])


    def backwards(self, orm):
        
        # Deleting model 'campusOrgPreferences'
        db.delete_table('campus_org_campusorgpreferences')


    models = {
        'campus_org.campusorg': {
            'Meta': {'ordering': "['name']", 'object_name': 'CampusOrg'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 8, 30, 23, 12, 17, 689000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 8, 30, 23, 12, 17, 689000)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.CampusOrgType']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'campus_org.campusorgpreferences': {
            'Meta': {'object_name': 'campusOrgPreferences'},
            'campu_org': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['campus_org.CampusOrg']", 'unique': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 8, 30, 23, 12, 17, 689000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 8, 30, 23, 12, 17, 689000)', 'auto_now': 'True', 'blank': 'True'})
        },
        'core.campusorgtype': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'CampusOrgType'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 8, 30, 23, 12, 17, 689000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 8, 30, 23, 12, 17, 689000)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['campus_org']
