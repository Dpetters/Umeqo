# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Student'
        db.create_table('student_student', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('profile_created', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('keywords', self.gf('django.db.models.fields.TextField')()),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('school_year', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.SchoolYear'], null=True, blank=True)),
            ('graduation_year', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.GraduationYear'], null=True, blank=True)),
            ('first_major', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='first_major', null=True, to=orm['core.Course'])),
            ('gpa', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=3, blank=True)),
            ('resume', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('second_major', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='second_major', null=True, to=orm['core.Course'])),
            ('sat_t', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('sat_m', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('sat_v', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('sat_w', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('act', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('older_than_18', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ethnicity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Ethnicity'], null=True, blank=True)),
            ('citizen', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('preferences', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['student.StudentPreferences'], unique=True)),
            ('statistics', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['student.StudentStatistics'], unique=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('student', ['Student'])

        # Adding M2M table for field looking_for on 'Student'
        db.create_table('student_student_looking_for', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('student', models.ForeignKey(orm['student.student'], null=False)),
            ('employmenttype', models.ForeignKey(orm['core.employmenttype'], null=False))
        ))
        db.create_unique('student_student_looking_for', ['student_id', 'employmenttype_id'])

        # Adding M2M table for field industries_of_interest on 'Student'
        db.create_table('student_student_industries_of_interest', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('student', models.ForeignKey(orm['student.student'], null=False)),
            ('industry', models.ForeignKey(orm['core.industry'], null=False))
        ))
        db.create_unique('student_student_industries_of_interest', ['student_id', 'industry_id'])

        # Adding M2M table for field previous_employers on 'Student'
        db.create_table('student_student_previous_employers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('student', models.ForeignKey(orm['student.student'], null=False)),
            ('employer', models.ForeignKey(orm['employer.employer'], null=False))
        ))
        db.create_unique('student_student_previous_employers', ['student_id', 'employer_id'])

        # Adding M2M table for field campus_involvement on 'Student'
        db.create_table('student_student_campus_involvement', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('student', models.ForeignKey(orm['student.student'], null=False)),
            ('campusorg', models.ForeignKey(orm['core.campusorg'], null=False))
        ))
        db.create_unique('student_student_campus_involvement', ['student_id', 'campusorg_id'])

        # Adding M2M table for field languages on 'Student'
        db.create_table('student_student_languages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('student', models.ForeignKey(orm['student.student'], null=False)),
            ('language', models.ForeignKey(orm['core.language'], null=False))
        ))
        db.create_unique('student_student_languages', ['student_id', 'language_id'])

        # Adding M2M table for field subscribed_employers on 'Student'
        db.create_table('student_student_subscribed_employers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('student', models.ForeignKey(orm['student.student'], null=False)),
            ('employer', models.ForeignKey(orm['employer.employer'], null=False))
        ))
        db.create_unique('student_student_subscribed_employers', ['student_id', 'employer_id'])

        # Adding model 'StudentPreferences'
        db.create_table('student_studentpreferences', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email_on_invite_to_public_event', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('email_on_invite_to_private_event', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('email_on_new_event', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('student', ['StudentPreferences'])

        # Adding model 'StudentStatistics'
        db.create_table('student_studentstatistics', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event_invite_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('add_to_resumebook_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('resume_view_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('shown_in_results_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('student', ['StudentStatistics'])


    def backwards(self, orm):
        
        # Deleting model 'Student'
        db.delete_table('student_student')

        # Removing M2M table for field looking_for on 'Student'
        db.delete_table('student_student_looking_for')

        # Removing M2M table for field industries_of_interest on 'Student'
        db.delete_table('student_student_industries_of_interest')

        # Removing M2M table for field previous_employers on 'Student'
        db.delete_table('student_student_previous_employers')

        # Removing M2M table for field campus_involvement on 'Student'
        db.delete_table('student_student_campus_involvement')

        # Removing M2M table for field languages on 'Student'
        db.delete_table('student_student_languages')

        # Removing M2M table for field subscribed_employers on 'Student'
        db.delete_table('student_student_subscribed_employers')

        # Deleting model 'StudentPreferences'
        db.delete_table('student_studentpreferences')

        # Deleting model 'StudentStatistics'
        db.delete_table('student_studentstatistics')


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
        'core.campusorg': {
            'Meta': {'object_name': 'CampusOrg'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.CampusOrgType']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'core.campusorgtype': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'CampusOrgType'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'core.course': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'Course'},
            'admin': ('django.db.models.fields.CharField', [], {'max_length': '41', 'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'}),
            'num': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'core.employmenttype': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'EmploymentType'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'core.ethnicity': {
            'Meta': {'object_name': 'Ethnicity'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'})
        },
        'core.graduationyear': {
            'Meta': {'object_name': 'GraduationYear'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.PositiveSmallIntegerField', [], {'unique': 'True'})
        },
        'core.industry': {
            'Meta': {'object_name': 'Industry'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'})
        },
        'core.language': {
            'Meta': {'object_name': 'Language'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'})
        },
        'core.schoolyear': {
            'Meta': {'object_name': 'SchoolYear'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'})
        },
        'employer.employer': {
            'Meta': {'object_name': 'Employer'},
            'company_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industries': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Industry']", 'symmetrical': 'False'}),
            'main_contact': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'main_contact_phone': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '20'})
        },
        'student.student': {
            'Meta': {'object_name': 'Student'},
            'act': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'campus_involvement': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.CampusOrg']", 'null': 'True', 'blank': 'True'}),
            'citizen': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ethnicity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Ethnicity']", 'null': 'True', 'blank': 'True'}),
            'first_major': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'first_major'", 'null': 'True', 'to': "orm['core.Course']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'gpa': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '3', 'blank': 'True'}),
            'graduation_year': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.GraduationYear']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industries_of_interest': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'industries_of_interest_of'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['core.Industry']"}),
            'keywords': ('django.db.models.fields.TextField', [], {}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.Language']", 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'looking_for': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.EmploymentType']", 'null': 'True', 'blank': 'True'}),
            'older_than_18': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'preferences': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['student.StudentPreferences']", 'unique': 'True'}),
            'previous_employers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'previous_employers_of'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['employer.Employer']"}),
            'profile_created': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'resume': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'sat_m': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sat_t': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sat_v': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sat_w': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'school_year': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.SchoolYear']", 'null': 'True', 'blank': 'True'}),
            'second_major': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'second_major'", 'null': 'True', 'to': "orm['core.Course']"}),
            'statistics': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['student.StudentStatistics']", 'unique': 'True'}),
            'subscribed_employers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'subscribed_employers'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['employer.Employer']"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'student.studentpreferences': {
            'Meta': {'object_name': 'StudentPreferences'},
            'email_on_invite_to_private_event': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email_on_invite_to_public_event': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email_on_new_event': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'student.studentstatistics': {
            'Meta': {'object_name': 'StudentStatistics'},
            'add_to_resumebook_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'event_invite_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'resume_view_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'shown_in_results_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['student']
