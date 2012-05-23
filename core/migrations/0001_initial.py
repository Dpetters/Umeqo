# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'CampusOrgType'
        db.create_table('core_campusorgtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 15, 283000), auto_now=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 15, 283000), auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=42)),
            ('sort_order', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('core', ['CampusOrgType'])

        # Adding model 'Location'
        db.create_table('core_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
            ('keywords', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('image_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('building_num', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
        ))
        db.send_create_signal('core', ['Location'])

        # Adding model 'Topic'
        db.create_table('core_topic', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 15, 283000), auto_now=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 15, 283000), auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=150, db_index=True)),
            ('sort_order', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('core', ['Topic'])

        # Adding model 'Question'
        db.create_table('core_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 15, 283000), auto_now=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 15, 283000), auto_now_add=True, blank=True)),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Topic'])),
            ('display', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('audience', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('sort_order', self.gf('django.db.models.fields.FloatField')()),
            ('question', self.gf('django.db.models.fields.TextField')()),
            ('answer', self.gf('django.db.models.fields.TextField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100, db_index=True)),
            ('click_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('core', ['Question'])

        # Adding model 'SchoolYear'
        db.create_table('core_schoolyear', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 15, 283000), auto_now=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 15, 283000), auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=42)),
            ('name_plural', self.gf('django.db.models.fields.CharField')(max_length=43, unique=True, null=True)),
        ))
        db.send_create_signal('core', ['SchoolYear'])

        # Adding model 'Edit'
        db.create_table('core_edit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 15, 283000), auto_now_add=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('core', ['Edit'])

        # Adding model 'GraduationYear'
        db.create_table('core_graduationyear', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 15, 283000), auto_now=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 15, 283000), auto_now_add=True, blank=True)),
            ('year', self.gf('django.db.models.fields.PositiveSmallIntegerField')(unique=True)),
        ))
        db.send_create_signal('core', ['GraduationYear'])

        # Adding model 'Language'
        db.create_table('core_language', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 15, 283000), auto_now=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 15, 283000), auto_now_add=True, blank=True)),
            ('name_and_level', self.gf('django.db.models.fields.CharField')(max_length=42)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=42)),
        ))
        db.send_create_signal('core', ['Language'])

        # Adding model 'Course'
        db.create_table('core_course', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 15, 283000), auto_now=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 15, 283000), auto_now_add=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=1000, null=True, blank=True)),
            ('display', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=42)),
            ('num', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('sort_order', self.gf('django.db.models.fields.FloatField')()),
            ('admin', self.gf('django.db.models.fields.CharField')(max_length=42, null=True, blank=True)),
            ('ou', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('core', ['Course'])

        # Adding model 'Tutorial'
        db.create_table('core_tutorial', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 15, 283000), auto_now=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 15, 283000), auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=150, db_index=True)),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Topic'], null=True, blank=True)),
            ('audience', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('sort_order', self.gf('django.db.models.fields.FloatField')()),
            ('display', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('core', ['Tutorial'])

        # Adding model 'EmploymentType'
        db.create_table('core_employmenttype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 15, 283000), auto_now=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 15, 283000), auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=42)),
            ('sort_order', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('core', ['EmploymentType'])

        # Adding model 'Industry'
        db.create_table('core_industry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 15, 283000), auto_now=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 15, 283000), auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=42)),
        ))
        db.send_create_signal('core', ['Industry'])

        # Adding model 'EventType'
        db.create_table('core_eventtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 15, 283000), auto_now=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 15, 283000), auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=42)),
            ('sort_order', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('core', ['EventType'])


    def backwards(self, orm):
        
        # Deleting model 'CampusOrgType'
        db.delete_table('core_campusorgtype')

        # Deleting model 'Location'
        db.delete_table('core_location')

        # Deleting model 'Topic'
        db.delete_table('core_topic')

        # Deleting model 'Question'
        db.delete_table('core_question')

        # Deleting model 'SchoolYear'
        db.delete_table('core_schoolyear')

        # Deleting model 'Edit'
        db.delete_table('core_edit')

        # Deleting model 'GraduationYear'
        db.delete_table('core_graduationyear')

        # Deleting model 'Language'
        db.delete_table('core_language')

        # Deleting model 'Course'
        db.delete_table('core_course')

        # Deleting model 'Tutorial'
        db.delete_table('core_tutorial')

        # Deleting model 'EmploymentType'
        db.delete_table('core_employmenttype')

        # Deleting model 'Industry'
        db.delete_table('core_industry')

        # Deleting model 'EventType'
        db.delete_table('core_eventtype')


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
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 15, 283000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 15, 283000)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'}),
            'sort_order': ('django.db.models.fields.FloatField', [], {})
        },
        'core.course': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'Course'},
            'admin': ('django.db.models.fields.CharField', [], {'max_length': '42', 'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 15, 283000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 15, 283000)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'}),
            'num': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'ou': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'sort_order': ('django.db.models.fields.FloatField', [], {}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'core.edit': {
            'Meta': {'object_name': 'Edit'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 15, 283000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'core.employmenttype': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'EmploymentType'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 15, 283000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 15, 283000)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'}),
            'sort_order': ('django.db.models.fields.FloatField', [], {})
        },
        'core.eventtype': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'EventType'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 15, 283000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 15, 283000)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'}),
            'sort_order': ('django.db.models.fields.FloatField', [], {})
        },
        'core.graduationyear': {
            'Meta': {'object_name': 'GraduationYear'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 15, 283000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 15, 283000)', 'auto_now': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.PositiveSmallIntegerField', [], {'unique': 'True'})
        },
        'core.industry': {
            'Meta': {'ordering': "['name']", 'object_name': 'Industry'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 15, 283000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 15, 283000)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'})
        },
        'core.language': {
            'Meta': {'object_name': 'Language'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 15, 283000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 15, 283000)', 'auto_now': 'True', 'blank': 'True'}),
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
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 15, 283000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 15, 283000)', 'auto_now': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.FloatField', [], {}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Topic']"})
        },
        'core.schoolyear': {
            'Meta': {'object_name': 'SchoolYear'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 15, 283000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 15, 283000)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'}),
            'name_plural': ('django.db.models.fields.CharField', [], {'max_length': '43', 'unique': 'True', 'null': 'True'})
        },
        'core.topic': {
            'Meta': {'ordering': "['sort_order', 'name']", 'object_name': 'Topic'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 15, 283000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 15, 283000)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.FloatField', [], {})
        },
        'core.tutorial': {
            'Meta': {'ordering': "['audience', 'topic', 'sort_order']", 'object_name': 'Tutorial'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'audience': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 15, 283000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 15, 283000)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.FloatField', [], {}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Topic']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['core']
