# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Employer'
        db.create_table('employer_employer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 29, 557000), auto_now=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 29, 557000), auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=42)),
            ('slug', self.gf('django.db.models.fields.SlugField')(db_index=True, max_length=20, null=True, blank=True)),
            ('logo', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('size', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('careers_website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('stripe_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('employer', ['Employer'])

        # Adding M2M table for field industries on 'Employer'
        db.create_table('employer_employer_industries', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('employer', models.ForeignKey(orm['employer.employer'], null=False)),
            ('industry', models.ForeignKey(orm['core.industry'], null=False))
        ))
        db.create_unique('employer_employer_industries', ['employer_id', 'industry_id'])

        # Adding M2M table for field offered_job_types on 'Employer'
        db.create_table('employer_employer_offered_job_types', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('employer', models.ForeignKey(orm['employer.employer'], null=False)),
            ('employmenttype', models.ForeignKey(orm['core.employmenttype'], null=False))
        ))
        db.create_unique('employer_employer_offered_job_types', ['employer_id', 'employmenttype_id'])

        # Adding M2M table for field starred_students on 'Employer'
        db.create_table('employer_employer_starred_students', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('employer', models.ForeignKey(orm['employer.employer'], null=False)),
            ('student', models.ForeignKey(orm['student.student'], null=False))
        ))
        db.create_unique('employer_employer_starred_students', ['employer_id', 'student_id'])

        # Adding model 'EmployerStatistics'
        db.create_table('employer_employerstatistics', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 29, 557000), auto_now=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 29, 557000), auto_now_add=True, blank=True)),
            ('employer', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['employer.Employer'], unique=True)),
            ('resumes_viewed', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True, blank=True)),
        ))
        db.send_create_signal('employer', ['EmployerStatistics'])

        # Adding model 'Recruiter'
        db.create_table('employer_recruiter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 29, 557000), auto_now=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 29, 557000), auto_now_add=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('employer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['employer.Employer'])),
        ))
        db.send_create_signal('employer', ['Recruiter'])

        # Adding model 'ResumeBook'
        db.create_table('employer_resumebook', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 29, 557000), auto_now=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 29, 557000), auto_now_add=True, blank=True)),
            ('recruiter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['employer.Recruiter'])),
            ('resume_book', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=42, null=True, blank=True)),
            ('delivered', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('employer', ['ResumeBook'])

        # Adding M2M table for field students on 'ResumeBook'
        db.create_table('employer_resumebook_students', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('resumebook', models.ForeignKey(orm['employer.resumebook'], null=False)),
            ('student', models.ForeignKey(orm['student.student'], null=False))
        ))
        db.create_unique('employer_resumebook_students', ['resumebook_id', 'student_id'])

        # Adding model 'StudentFilteringParameters'
        db.create_table('employer_studentfilteringparameters', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 29, 557000), auto_now=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 29, 557000), auto_now_add=True, blank=True)),
            ('gpa', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('sat_t', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('sat_m', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('sat_v', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('sat_w', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('act', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('recruiter', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['employer.Recruiter'], unique=True)),
            ('older_than_21', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
        ))
        db.send_create_signal('employer', ['StudentFilteringParameters'])

        # Adding M2M table for field previous_employers on 'StudentFilteringParameters'
        db.create_table('employer_studentfilteringparameters_previous_employers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('studentfilteringparameters', models.ForeignKey(orm['employer.studentfilteringparameters'], null=False)),
            ('employer', models.ForeignKey(orm['employer.employer'], null=False))
        ))
        db.create_unique('employer_studentfilteringparameters_previous_employers', ['studentfilteringparameters_id', 'employer_id'])

        # Adding M2M table for field industries_of_interest on 'StudentFilteringParameters'
        db.create_table('employer_studentfilteringparameters_industries_of_interest', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('studentfilteringparameters', models.ForeignKey(orm['employer.studentfilteringparameters'], null=False)),
            ('industry', models.ForeignKey(orm['core.industry'], null=False))
        ))
        db.create_unique('employer_studentfilteringparameters_industries_of_interest', ['studentfilteringparameters_id', 'industry_id'])

        # Adding M2M table for field campus_involvement on 'StudentFilteringParameters'
        db.create_table('employer_studentfilteringparameters_campus_involvement', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('studentfilteringparameters', models.ForeignKey(orm['employer.studentfilteringparameters'], null=False)),
            ('campusorg', models.ForeignKey(orm['campus_org.campusorg'], null=False))
        ))
        db.create_unique('employer_studentfilteringparameters_campus_involvement', ['studentfilteringparameters_id', 'campusorg_id'])

        # Adding M2M table for field languages on 'StudentFilteringParameters'
        db.create_table('employer_studentfilteringparameters_languages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('studentfilteringparameters', models.ForeignKey(orm['employer.studentfilteringparameters'], null=False)),
            ('language', models.ForeignKey(orm['core.language'], null=False))
        ))
        db.create_unique('employer_studentfilteringparameters_languages', ['studentfilteringparameters_id', 'language_id'])

        # Adding M2M table for field countries_of_citizenship on 'StudentFilteringParameters'
        db.create_table('employer_studentfilteringparameters_countries_of_citizenship', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('studentfilteringparameters', models.ForeignKey(orm['employer.studentfilteringparameters'], null=False)),
            ('country', models.ForeignKey(orm['countries.country'], null=False))
        ))
        db.create_unique('employer_studentfilteringparameters_countries_of_citizenship', ['studentfilteringparameters_id', 'country_id'])

        # Adding M2M table for field majors on 'StudentFilteringParameters'
        db.create_table('employer_studentfilteringparameters_majors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('studentfilteringparameters', models.ForeignKey(orm['employer.studentfilteringparameters'], null=False)),
            ('course', models.ForeignKey(orm['core.course'], null=False))
        ))
        db.create_unique('employer_studentfilteringparameters_majors', ['studentfilteringparameters_id', 'course_id'])

        # Adding M2M table for field school_years on 'StudentFilteringParameters'
        db.create_table('employer_studentfilteringparameters_school_years', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('studentfilteringparameters', models.ForeignKey(orm['employer.studentfilteringparameters'], null=False)),
            ('schoolyear', models.ForeignKey(orm['core.schoolyear'], null=False))
        ))
        db.create_unique('employer_studentfilteringparameters_school_years', ['studentfilteringparameters_id', 'schoolyear_id'])

        # Adding M2M table for field graduation_years on 'StudentFilteringParameters'
        db.create_table('employer_studentfilteringparameters_graduation_years', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('studentfilteringparameters', models.ForeignKey(orm['employer.studentfilteringparameters'], null=False)),
            ('graduationyear', models.ForeignKey(orm['core.graduationyear'], null=False))
        ))
        db.create_unique('employer_studentfilteringparameters_graduation_years', ['studentfilteringparameters_id', 'graduationyear_id'])

        # Adding M2M table for field employment_types on 'StudentFilteringParameters'
        db.create_table('employer_studentfilteringparameters_employment_types', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('studentfilteringparameters', models.ForeignKey(orm['employer.studentfilteringparameters'], null=False)),
            ('employmenttype', models.ForeignKey(orm['core.employmenttype'], null=False))
        ))
        db.create_unique('employer_studentfilteringparameters_employment_types', ['studentfilteringparameters_id', 'employmenttype_id'])

        # Adding model 'EmployerStudentComment'
        db.create_table('employer_employerstudentcomment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 29, 557000), auto_now=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 29, 557000), auto_now_add=True, blank=True)),
            ('employer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['employer.Employer'])),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student.Student'])),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('employer', ['EmployerStudentComment'])

        # Adding unique constraint on 'EmployerStudentComment', fields ['employer', 'student']
        db.create_unique('employer_employerstudentcomment', ['employer_id', 'student_id'])

        # Adding model 'RecruiterPreferences'
        db.create_table('employer_recruiterpreferences', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 29, 557000), auto_now=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 29, 557000), auto_now_add=True, blank=True)),
            ('recruiter', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['employer.Recruiter'], unique=True)),
            ('email_on_rsvp_to_public_event', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('email_on_rsvp_to_private_event', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('default_student_results_per_page', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=10)),
            ('default_student_result_ordering', self.gf('django.db.models.fields.CharField')(default='relevancy', max_length=42)),
        ))
        db.send_create_signal('employer', ['RecruiterPreferences'])

        # Adding model 'RecruiterStatistics'
        db.create_table('employer_recruiterstatistics', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 29, 557000), auto_now=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 29, 557000), auto_now_add=True, blank=True)),
            ('recruiter', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['employer.Recruiter'], unique=True)),
            ('resumes_viewed', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True, blank=True)),
        ))
        db.send_create_signal('employer', ['RecruiterStatistics'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'EmployerStudentComment', fields ['employer', 'student']
        db.delete_unique('employer_employerstudentcomment', ['employer_id', 'student_id'])

        # Deleting model 'Employer'
        db.delete_table('employer_employer')

        # Removing M2M table for field industries on 'Employer'
        db.delete_table('employer_employer_industries')

        # Removing M2M table for field offered_job_types on 'Employer'
        db.delete_table('employer_employer_offered_job_types')

        # Removing M2M table for field starred_students on 'Employer'
        db.delete_table('employer_employer_starred_students')

        # Deleting model 'EmployerStatistics'
        db.delete_table('employer_employerstatistics')

        # Deleting model 'Recruiter'
        db.delete_table('employer_recruiter')

        # Deleting model 'ResumeBook'
        db.delete_table('employer_resumebook')

        # Removing M2M table for field students on 'ResumeBook'
        db.delete_table('employer_resumebook_students')

        # Deleting model 'StudentFilteringParameters'
        db.delete_table('employer_studentfilteringparameters')

        # Removing M2M table for field previous_employers on 'StudentFilteringParameters'
        db.delete_table('employer_studentfilteringparameters_previous_employers')

        # Removing M2M table for field industries_of_interest on 'StudentFilteringParameters'
        db.delete_table('employer_studentfilteringparameters_industries_of_interest')

        # Removing M2M table for field campus_involvement on 'StudentFilteringParameters'
        db.delete_table('employer_studentfilteringparameters_campus_involvement')

        # Removing M2M table for field languages on 'StudentFilteringParameters'
        db.delete_table('employer_studentfilteringparameters_languages')

        # Removing M2M table for field countries_of_citizenship on 'StudentFilteringParameters'
        db.delete_table('employer_studentfilteringparameters_countries_of_citizenship')

        # Removing M2M table for field majors on 'StudentFilteringParameters'
        db.delete_table('employer_studentfilteringparameters_majors')

        # Removing M2M table for field school_years on 'StudentFilteringParameters'
        db.delete_table('employer_studentfilteringparameters_school_years')

        # Removing M2M table for field graduation_years on 'StudentFilteringParameters'
        db.delete_table('employer_studentfilteringparameters_graduation_years')

        # Removing M2M table for field employment_types on 'StudentFilteringParameters'
        db.delete_table('employer_studentfilteringparameters_employment_types')

        # Deleting model 'EmployerStudentComment'
        db.delete_table('employer_employerstudentcomment')

        # Deleting model 'RecruiterPreferences'
        db.delete_table('employer_recruiterpreferences')

        # Deleting model 'RecruiterStatistics'
        db.delete_table('employer_recruiterstatistics')


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
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 29, 557000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 29, 557000)', 'auto_now': 'True', 'blank': 'True'}),
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
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 29, 557000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 29, 557000)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'}),
            'sort_order': ('django.db.models.fields.FloatField', [], {})
        },
        'core.course': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'Course'},
            'admin': ('django.db.models.fields.CharField', [], {'max_length': '42', 'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 29, 557000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 29, 557000)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'}),
            'num': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'ou': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'sort_order': ('django.db.models.fields.FloatField', [], {}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'core.employmenttype': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'EmploymentType'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 29, 557000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 29, 557000)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'}),
            'sort_order': ('django.db.models.fields.FloatField', [], {})
        },
        'core.graduationyear': {
            'Meta': {'object_name': 'GraduationYear'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 29, 557000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 29, 557000)', 'auto_now': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.PositiveSmallIntegerField', [], {'unique': 'True'})
        },
        'core.industry': {
            'Meta': {'ordering': "['name']", 'object_name': 'Industry'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 29, 557000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 29, 557000)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'})
        },
        'core.language': {
            'Meta': {'object_name': 'Language'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 29, 557000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 29, 557000)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '42'}),
            'name_and_level': ('django.db.models.fields.CharField', [], {'max_length': '42'})
        },
        'core.schoolyear': {
            'Meta': {'object_name': 'SchoolYear'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 29, 557000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 29, 557000)', 'auto_now': 'True', 'blank': 'True'}),
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
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 29, 557000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industries': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.Industry']", 'null': 'True', 'blank': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 29, 557000)', 'auto_now': 'True', 'blank': 'True'}),
            'logo': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'}),
            'offered_job_types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.EmploymentType']", 'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'starred_students': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['student.Student']", 'null': 'True', 'blank': 'True'}),
            'stripe_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'employer.employerstatistics': {
            'Meta': {'object_name': 'EmployerStatistics'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 29, 557000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'employer': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['employer.Employer']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 29, 557000)', 'auto_now': 'True', 'blank': 'True'}),
            'resumes_viewed': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
        'employer.employerstudentcomment': {
            'Meta': {'unique_together': "(('employer', 'student'),)", 'object_name': 'EmployerStudentComment'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 29, 557000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'employer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['employer.Employer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 29, 557000)', 'auto_now': 'True', 'blank': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student.Student']"})
        },
        'employer.recruiter': {
            'Meta': {'ordering': "['user__first_name']", 'object_name': 'Recruiter'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 29, 557000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'employer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['employer.Employer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 29, 557000)', 'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'employer.recruiterpreferences': {
            'Meta': {'object_name': 'RecruiterPreferences'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 29, 557000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'default_student_result_ordering': ('django.db.models.fields.CharField', [], {'default': "'relevancy'", 'max_length': '42'}),
            'default_student_results_per_page': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '10'}),
            'email_on_rsvp_to_private_event': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email_on_rsvp_to_public_event': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 29, 557000)', 'auto_now': 'True', 'blank': 'True'}),
            'recruiter': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['employer.Recruiter']", 'unique': 'True'})
        },
        'employer.recruiterstatistics': {
            'Meta': {'object_name': 'RecruiterStatistics'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 29, 557000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 29, 557000)', 'auto_now': 'True', 'blank': 'True'}),
            'recruiter': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['employer.Recruiter']", 'unique': 'True'}),
            'resumes_viewed': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
        'employer.resumebook': {
            'Meta': {'ordering': "['-last_updated']", 'object_name': 'ResumeBook'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 29, 557000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'delivered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 29, 557000)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '42', 'null': 'True', 'blank': 'True'}),
            'recruiter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['employer.Recruiter']"}),
            'resume_book': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['student.Student']", 'null': 'True', 'blank': 'True'})
        },
        'employer.studentfilteringparameters': {
            'Meta': {'object_name': 'StudentFilteringParameters'},
            'act': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'campus_involvement': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['campus_org.CampusOrg']", 'null': 'True', 'blank': 'True'}),
            'countries_of_citizenship': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['countries.Country']", 'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 29, 557000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'employment_types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.EmploymentType']", 'null': 'True', 'blank': 'True'}),
            'gpa': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'graduation_years': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.GraduationYear']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industries_of_interest': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.Industry']", 'null': 'True', 'blank': 'True'}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.Language']", 'null': 'True', 'blank': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 29, 557000)', 'auto_now': 'True', 'blank': 'True'}),
            'majors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.Course']", 'null': 'True', 'blank': 'True'}),
            'older_than_21': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'previous_employers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['employer.Employer']", 'null': 'True', 'blank': 'True'}),
            'recruiter': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['employer.Recruiter']", 'unique': 'True'}),
            'sat_m': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sat_t': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sat_v': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sat_w': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'school_years': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.SchoolYear']", 'null': 'True', 'blank': 'True'})
        },
        'student.student': {
            'Meta': {'object_name': 'Student'},
            'act': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'campus_involvement': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['campus_org.CampusOrg']", 'null': 'True', 'blank': 'True'}),
            'countries_of_citizenship': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['countries.Country']", 'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 29, 557000)', 'auto_now_add': 'True', 'blank': 'True'}),
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
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 29, 619000)'}),
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
        }
    }

    complete_apps = ['employer']
