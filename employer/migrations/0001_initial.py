# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ResumeBook'
        db.create_table('employer_resumebook', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recruiter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['employer.Recruiter'])),
            ('resume_book', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=42, null=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('employer', ['ResumeBook'])

        # Adding M2M table for field students on 'ResumeBook'
        db.create_table('employer_resumebook_students', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('resumebook', models.ForeignKey(orm['employer.resumebook'], null=False)),
            ('student', models.ForeignKey(orm['student.student'], null=False))
        ))
        db.create_unique('employer_resumebook_students', ['resumebook_id', 'student_id'])

        # Adding model 'Recruiter'
        db.create_table('employer_recruiter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('employer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['employer.Employer'])),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('employer', ['Recruiter'])

        # Adding M2M table for field starred_students on 'Recruiter'
        db.create_table('employer_recruiter_starred_students', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('recruiter', models.ForeignKey(orm['employer.recruiter'], null=False)),
            ('student', models.ForeignKey(orm['student.student'], null=False))
        ))
        db.create_unique('employer_recruiter_starred_students', ['recruiter_id', 'student_id'])

        # Adding model 'FilteringParameters'
        db.create_table('employer_filteringparameters', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recruiter', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['employer.Recruiter'], unique=True)),
            ('gpa', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=3, blank=True)),
            ('sat', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('act', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('older_than_18', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
        ))
        db.send_create_signal('employer', ['FilteringParameters'])

        # Adding M2M table for field school_years on 'FilteringParameters'
        db.create_table('employer_filteringparameters_school_years', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('filteringparameters', models.ForeignKey(orm['employer.filteringparameters'], null=False)),
            ('schoolyear', models.ForeignKey(orm['core.schoolyear'], null=False))
        ))
        db.create_unique('employer_filteringparameters_school_years', ['filteringparameters_id', 'schoolyear_id'])

        # Adding M2M table for field graduation_years on 'FilteringParameters'
        db.create_table('employer_filteringparameters_graduation_years', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('filteringparameters', models.ForeignKey(orm['employer.filteringparameters'], null=False)),
            ('graduationyear', models.ForeignKey(orm['core.graduationyear'], null=False))
        ))
        db.create_unique('employer_filteringparameters_graduation_years', ['filteringparameters_id', 'graduationyear_id'])

        # Adding M2M table for field majors on 'FilteringParameters'
        db.create_table('employer_filteringparameters_majors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('filteringparameters', models.ForeignKey(orm['employer.filteringparameters'], null=False)),
            ('course', models.ForeignKey(orm['core.course'], null=False))
        ))
        db.create_unique('employer_filteringparameters_majors', ['filteringparameters_id', 'course_id'])

        # Adding M2M table for field previous_employers on 'FilteringParameters'
        db.create_table('employer_filteringparameters_previous_employers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('filteringparameters', models.ForeignKey(orm['employer.filteringparameters'], null=False)),
            ('employer', models.ForeignKey(orm['employer.employer'], null=False))
        ))
        db.create_unique('employer_filteringparameters_previous_employers', ['filteringparameters_id', 'employer_id'])

        # Adding M2M table for field industries_of_interest on 'FilteringParameters'
        db.create_table('employer_filteringparameters_industries_of_interest', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('filteringparameters', models.ForeignKey(orm['employer.filteringparameters'], null=False)),
            ('industry', models.ForeignKey(orm['core.industry'], null=False))
        ))
        db.create_unique('employer_filteringparameters_industries_of_interest', ['filteringparameters_id', 'industry_id'])

        # Adding M2M table for field employment_types on 'FilteringParameters'
        db.create_table('employer_filteringparameters_employment_types', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('filteringparameters', models.ForeignKey(orm['employer.filteringparameters'], null=False)),
            ('employmenttype', models.ForeignKey(orm['core.employmenttype'], null=False))
        ))
        db.create_unique('employer_filteringparameters_employment_types', ['filteringparameters_id', 'employmenttype_id'])

        # Adding M2M table for field campus_involvement on 'FilteringParameters'
        db.create_table('employer_filteringparameters_campus_involvement', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('filteringparameters', models.ForeignKey(orm['employer.filteringparameters'], null=False)),
            ('campusorg', models.ForeignKey(orm['core.campusorg'], null=False))
        ))
        db.create_unique('employer_filteringparameters_campus_involvement', ['filteringparameters_id', 'campusorg_id'])

        # Adding M2M table for field languages on 'FilteringParameters'
        db.create_table('employer_filteringparameters_languages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('filteringparameters', models.ForeignKey(orm['employer.filteringparameters'], null=False)),
            ('language', models.ForeignKey(orm['core.language'], null=False))
        ))
        db.create_unique('employer_filteringparameters_languages', ['filteringparameters_id', 'language_id'])

        # Adding M2M table for field countries_of_citizenship on 'FilteringParameters'
        db.create_table('employer_filteringparameters_countries_of_citizenship', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('filteringparameters', models.ForeignKey(orm['employer.filteringparameters'], null=False)),
            ('country', models.ForeignKey(orm['countries.country'], null=False))
        ))
        db.create_unique('employer_filteringparameters_countries_of_citizenship', ['filteringparameters_id', 'country_id'])

        # Adding model 'StudentComment'
        db.create_table('employer_studentcomment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recruiter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['employer.Recruiter'])),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student.Student'])),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('employer', ['StudentComment'])

        # Adding unique constraint on 'StudentComment', fields ['recruiter', 'student']
        db.create_unique('employer_studentcomment', ['recruiter_id', 'student_id'])

        # Adding model 'Employer'
        db.create_table('employer_employer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=42)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('main_contact', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('main_contact_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('main_contact_phone', self.gf('django.contrib.localflavor.us.models.PhoneNumberField')(max_length=20)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('employer', ['Employer'])

        # Adding M2M table for field industries on 'Employer'
        db.create_table('employer_employer_industries', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('employer', models.ForeignKey(orm['employer.employer'], null=False)),
            ('industry', models.ForeignKey(orm['core.industry'], null=False))
        ))
        db.create_unique('employer_employer_industries', ['employer_id', 'industry_id'])

        # Adding model 'RecruiterPreferences'
        db.create_table('employer_recruiterpreferences', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recruiter', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['employer.Recruiter'], unique=True)),
            ('email_on_rsvp', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('results_per_page', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=10)),
            ('default_student_ordering', self.gf('django.db.models.fields.CharField')(default='relevancy', max_length=42)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('employer', ['RecruiterPreferences'])

        # Adding model 'RecruiterStatistics'
        db.create_table('employer_recruiterstatistics', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recruiter', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['employer.Recruiter'], unique=True)),
            ('resumes_viewed', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True, blank=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('employer', ['RecruiterStatistics'])

        # Adding model 'EmployerStatistics'
        db.create_table('employer_employerstatistics', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('employer', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['employer.Employer'], unique=True)),
            ('resumes_viewed', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True, blank=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('employer', ['EmployerStatistics'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'StudentComment', fields ['recruiter', 'student']
        db.delete_unique('employer_studentcomment', ['recruiter_id', 'student_id'])

        # Deleting model 'ResumeBook'
        db.delete_table('employer_resumebook')

        # Removing M2M table for field students on 'ResumeBook'
        db.delete_table('employer_resumebook_students')

        # Deleting model 'Recruiter'
        db.delete_table('employer_recruiter')

        # Removing M2M table for field starred_students on 'Recruiter'
        db.delete_table('employer_recruiter_starred_students')

        # Deleting model 'FilteringParameters'
        db.delete_table('employer_filteringparameters')

        # Removing M2M table for field school_years on 'FilteringParameters'
        db.delete_table('employer_filteringparameters_school_years')

        # Removing M2M table for field graduation_years on 'FilteringParameters'
        db.delete_table('employer_filteringparameters_graduation_years')

        # Removing M2M table for field majors on 'FilteringParameters'
        db.delete_table('employer_filteringparameters_majors')

        # Removing M2M table for field previous_employers on 'FilteringParameters'
        db.delete_table('employer_filteringparameters_previous_employers')

        # Removing M2M table for field industries_of_interest on 'FilteringParameters'
        db.delete_table('employer_filteringparameters_industries_of_interest')

        # Removing M2M table for field employment_types on 'FilteringParameters'
        db.delete_table('employer_filteringparameters_employment_types')

        # Removing M2M table for field campus_involvement on 'FilteringParameters'
        db.delete_table('employer_filteringparameters_campus_involvement')

        # Removing M2M table for field languages on 'FilteringParameters'
        db.delete_table('employer_filteringparameters_languages')

        # Removing M2M table for field countries_of_citizenship on 'FilteringParameters'
        db.delete_table('employer_filteringparameters_countries_of_citizenship')

        # Deleting model 'StudentComment'
        db.delete_table('employer_studentcomment')

        # Deleting model 'Employer'
        db.delete_table('employer_employer')

        # Removing M2M table for field industries on 'Employer'
        db.delete_table('employer_employer_industries')

        # Deleting model 'RecruiterPreferences'
        db.delete_table('employer_recruiterpreferences')

        # Deleting model 'RecruiterStatistics'
        db.delete_table('employer_recruiterstatistics')

        # Deleting model 'EmployerStatistics'
        db.delete_table('employer_employerstatistics')


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
            'admin': ('django.db.models.fields.CharField', [], {'max_length': '42', 'null': 'True', 'blank': 'True'}),
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
        'countries.country': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Country', 'db_table': "'country'"},
            'iso': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'}),
            'iso3': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'numcode': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'printable_name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'employer.employer': {
            'Meta': {'object_name': 'Employer'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industries': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Industry']", 'symmetrical': 'False'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'main_contact': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'main_contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'main_contact_phone': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '20'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        'employer.employerstatistics': {
            'Meta': {'object_name': 'EmployerStatistics'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'employer': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['employer.Employer']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'resumes_viewed': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
        'employer.filteringparameters': {
            'Meta': {'object_name': 'FilteringParameters'},
            'act': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'campus_involvement': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.CampusOrg']", 'null': 'True', 'blank': 'True'}),
            'countries_of_citizenship': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['countries.Country']", 'null': 'True', 'blank': 'True'}),
            'employment_types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.EmploymentType']", 'null': 'True', 'blank': 'True'}),
            'gpa': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '3', 'blank': 'True'}),
            'graduation_years': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.GraduationYear']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industries_of_interest': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'default_filtering_employers'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['core.Industry']"}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.Language']", 'null': 'True', 'blank': 'True'}),
            'majors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.Course']", 'null': 'True', 'blank': 'True'}),
            'older_than_18': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'previous_employers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['employer.Employer']", 'null': 'True', 'blank': 'True'}),
            'recruiter': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['employer.Recruiter']", 'unique': 'True'}),
            'sat': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'school_years': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.SchoolYear']", 'null': 'True', 'blank': 'True'})
        },
        'employer.recruiter': {
            'Meta': {'object_name': 'Recruiter'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'employer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['employer.Employer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'starred_students': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['student.Student']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'employer.recruiterpreferences': {
            'Meta': {'object_name': 'RecruiterPreferences'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'default_student_ordering': ('django.db.models.fields.CharField', [], {'default': "'relevancy'", 'max_length': '42'}),
            'email_on_rsvp': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'recruiter': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['employer.Recruiter']", 'unique': 'True'}),
            'results_per_page': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '10'})
        },
        'employer.recruiterstatistics': {
            'Meta': {'object_name': 'RecruiterStatistics'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'recruiter': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['employer.Recruiter']", 'unique': 'True'}),
            'resumes_viewed': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
        'employer.resumebook': {
            'Meta': {'object_name': 'ResumeBook'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '42', 'null': 'True', 'blank': 'True'}),
            'recruiter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['employer.Recruiter']"}),
            'resume_book': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['student.Student']", 'null': 'True', 'blank': 'True'})
        },
        'employer.studentcomment': {
            'Meta': {'unique_together': "(('recruiter', 'student'),)", 'object_name': 'StudentComment'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recruiter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['employer.Recruiter']"}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student.Student']"})
        },
        'student.student': {
            'Meta': {'object_name': 'Student'},
            'act': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'campus_involvement': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.CampusOrg']", 'null': 'True', 'blank': 'True'}),
            'countries_of_citizenship': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['countries.Country']", 'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'first_major': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'first_major'", 'null': 'True', 'to': "orm['core.Course']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'gpa': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '3', 'blank': 'True'}),
            'graduation_year': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.GraduationYear']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industries_of_interest': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'industries_of_interest_of'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['core.Industry']"}),
            'keywords': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.Language']", 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'looking_for': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.EmploymentType']", 'null': 'True', 'blank': 'True'}),
            'older_than_18': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'previous_employers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'previous_employers_of'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['employer.Employer']"}),
            'profile_created': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'resume': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'sat_m': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sat_t': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sat_v': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sat_w': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'school_year': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.SchoolYear']", 'null': 'True', 'blank': 'True'}),
            'second_major': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'second_major'", 'null': 'True', 'to': "orm['core.Course']"}),
            'subscriptions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'subscriptions'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['employer.Employer']"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['employer']
