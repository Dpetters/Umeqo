# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'RegException'
        db.create_table('registration_regexception', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 35, 95000), auto_now_add=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
        ))
        db.send_create_signal('registration', ['RegException'])

        # Adding model 'InterestedPerson'
        db.create_table('registration_interestedperson', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 35, 95000), auto_now=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 35, 95000), auto_now_add=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, unique=True, null=True, blank=True)),
            ('summer_plans', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True)),
            ('auto_email', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('final', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('emailed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('registration', ['InterestedPerson'])

        # Adding model 'SessionKey'
        db.create_table('registration_sessionkey', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 35, 95000), auto_now=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 35, 95000), auto_now_add=True, blank=True)),
            ('session_key', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('registration', ['SessionKey'])

        # Adding model 'UserAttributes'
        db.create_table('registration_userattributes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('is_verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('last_password_change_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('agreed_to_terms', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('agreed_to_terms_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('registration', ['UserAttributes'])

        # Adding model 'RegistrationProfile'
        db.create_table('registration_registrationprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('activation_key', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal('registration', ['RegistrationProfile'])

        # Adding model 'LoginAttempt'
        db.create_table('registration_loginattempt', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('attempt_datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True)),
        ))
        db.send_create_signal('registration', ['LoginAttempt'])


    def backwards(self, orm):
        
        # Deleting model 'RegException'
        db.delete_table('registration_regexception')

        # Deleting model 'InterestedPerson'
        db.delete_table('registration_interestedperson')

        # Deleting model 'SessionKey'
        db.delete_table('registration_sessionkey')

        # Deleting model 'UserAttributes'
        db.delete_table('registration_userattributes')

        # Deleting model 'RegistrationProfile'
        db.delete_table('registration_registrationprofile')

        # Deleting model 'LoginAttempt'
        db.delete_table('registration_loginattempt')


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
        'registration.interestedperson': {
            'Meta': {'object_name': 'InterestedPerson'},
            'auto_email': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 35, 95000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'emailed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'final': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 35, 95000)', 'auto_now': 'True', 'blank': 'True'}),
            'summer_plans': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'registration.loginattempt': {
            'Meta': {'object_name': 'LoginAttempt'},
            'attempt_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True'})
        },
        'registration.regexception': {
            'Meta': {'object_name': 'RegException'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 35, 95000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'registration.registrationprofile': {
            'Meta': {'object_name': 'RegistrationProfile'},
            'activation_key': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'registration.sessionkey': {
            'Meta': {'object_name': 'SessionKey'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 35, 95000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 35, 95000)', 'auto_now': 'True', 'blank': 'True'}),
            'session_key': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'registration.userattributes': {
            'Meta': {'object_name': 'UserAttributes'},
            'agreed_to_terms': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'agreed_to_terms_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_password_change_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['registration']
