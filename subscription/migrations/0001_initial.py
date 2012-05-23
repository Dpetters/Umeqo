# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Transaction'
        db.create_table('subscription_transaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('employer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['employer.Employer'], null=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('person', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True)),
            ('amount', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('comment', self.gf('django.db.models.fields.TextField')()),
            ('payment', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('subscription', ['Transaction'])

        # Adding model 'Subscription'
        db.create_table('subscription_subscription', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uid', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True, null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('trial_period', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('trial_unit', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('recurrence_period', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('recurrence_unit', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
        ))
        db.send_create_signal('subscription', ['Subscription'])

        # Adding model 'Card'
        db.create_table('subscription_card', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('employer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['employer.Employer'])),
            ('last_4_digits', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('expiration_date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
        ))
        db.send_create_signal('subscription', ['Card'])

        # Adding model 'EmployerSubscription'
        db.create_table('subscription_employersubscription', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('employer', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['employer.Employer'], unique=True)),
            ('subscription', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['subscription.Subscription'])),
            ('expires', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, null=True)),
            ('cancelled', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('subscription', ['EmployerSubscription'])


    def backwards(self, orm):
        
        # Deleting model 'Transaction'
        db.delete_table('subscription_transaction')

        # Deleting model 'Subscription'
        db.delete_table('subscription_subscription')

        # Deleting model 'Card'
        db.delete_table('subscription_card')

        # Deleting model 'EmployerSubscription'
        db.delete_table('subscription_employersubscription')


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
        'campus_org.campusorg': {
            'Meta': {'ordering': "['name']", 'object_name': 'CampusOrg'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 8, 41, 386000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 8, 41, 386000)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.CampusOrgType']"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
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
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 8, 41, 386000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 8, 41, 386000)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'}),
            'sort_order': ('django.db.models.fields.FloatField', [], {})
        },
        'core.course': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'Course'},
            'admin': ('django.db.models.fields.CharField', [], {'max_length': '42', 'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 8, 41, 386000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 8, 41, 386000)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'}),
            'num': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'ou': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'sort_order': ('django.db.models.fields.FloatField', [], {}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'core.employmenttype': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'EmploymentType'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 8, 41, 386000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 8, 41, 386000)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'}),
            'sort_order': ('django.db.models.fields.FloatField', [], {})
        },
        'core.graduationyear': {
            'Meta': {'object_name': 'GraduationYear'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 8, 41, 386000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 8, 41, 386000)', 'auto_now': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.PositiveSmallIntegerField', [], {'unique': 'True'})
        },
        'core.industry': {
            'Meta': {'ordering': "['name']", 'object_name': 'Industry'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 8, 41, 386000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 8, 41, 386000)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'})
        },
        'core.language': {
            'Meta': {'object_name': 'Language'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 8, 41, 386000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 8, 41, 386000)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '42'}),
            'name_and_level': ('django.db.models.fields.CharField', [], {'max_length': '42'})
        },
        'core.schoolyear': {
            'Meta': {'object_name': 'SchoolYear'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 8, 41, 386000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 8, 41, 386000)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'}),
            'name_plural': ('django.db.models.fields.CharField', [], {'max_length': '43', 'unique': 'True', 'null': 'True'})
        },
        'countries.country': {
            'Meta': {'ordering': "('-sort_order', 'name')", 'object_name': 'Country', 'db_table': "'country'"},
            'iso': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'}),
            'iso3': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'numcode': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'printable_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'sort_order': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'employer.employer': {
            'Meta': {'ordering': "['name']", 'object_name': 'Employer'},
            'careers_website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 8, 41, 386000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industries': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.Industry']", 'null': 'True', 'blank': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 8, 41, 386000)', 'auto_now': 'True', 'blank': 'True'}),
            'logo': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'}),
            'offered_job_types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.EmploymentType']", 'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'starred_students': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['student.Student']", 'null': 'True', 'blank': 'True'}),
            'stripe_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'student.student': {
            'Meta': {'object_name': 'Student'},
            'act': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'campus_involvement': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['campus_org.CampusOrg']", 'null': 'True', 'blank': 'True'}),
            'countries_of_citizenship': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['countries.Country']", 'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 8, 41, 386000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'first_major': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'first_major'", 'null': 'True', 'to': "orm['core.Course']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'gpa': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'graduation_month': ('django.db.models.fields.CharField', [], {'default': "'5'", 'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'graduation_year': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.GraduationYear']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industries_of_interest': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.Industry']", 'null': 'True', 'blank': 'True'}),
            'keywords': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.Language']", 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 8, 41, 449000)'}),
            'looking_for': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.EmploymentType']", 'null': 'True', 'blank': 'True'}),
            'older_than_21': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'previous_employers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['employer.Employer']", 'null': 'True', 'blank': 'True'}),
            'profile_created': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'resume': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'sat_m': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sat_t': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sat_v': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sat_w': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'school_year': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.SchoolYear']", 'null': 'True', 'blank': 'True'}),
            'second_major': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'second_major'", 'null': 'True', 'to': "orm['core.Course']"}),
            'subscriptions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'subscribers'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['employer.Employer']"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'subscription.card': {
            'Meta': {'object_name': 'Card'},
            'employer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['employer.Employer']"}),
            'expiration_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_4_digits': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        },
        'subscription.employersubscription': {
            'Meta': {'object_name': 'EmployerSubscription'},
            'cancelled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'employer': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['employer.Employer']", 'unique': 'True'}),
            'expires': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subscription': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['subscription.Subscription']"})
        },
        'subscription.subscription': {
            'Meta': {'ordering': "('price', '-recurrence_period')", 'object_name': 'Subscription'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'recurrence_period': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'recurrence_unit': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'trial_period': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'trial_unit': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'uid': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'null': 'True'})
        },
        'subscription.transaction': {
            'Meta': {'ordering': "('-timestamp',)", 'object_name': 'Transaction'},
            'amount': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            'employer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['employer.Employer']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'person': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['subscription']
