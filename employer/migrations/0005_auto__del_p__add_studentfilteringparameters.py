# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'P'
        db.delete_table('employer_p')

        # Removing M2M table for field majors on 'P'
        db.delete_table('employer_p_majors')

        # Removing M2M table for field school_years on 'P'
        db.delete_table('employer_p_school_years')

        # Removing M2M table for field graduation_years on 'P'
        db.delete_table('employer_p_graduation_years')

        # Removing M2M table for field employment_types on 'P'
        db.delete_table('employer_p_employment_types')

        # Removing M2M table for field campus_involvement on 'P'
        db.delete_table('employer_p_campus_involvement')

        # Removing M2M table for field languages on 'P'
        db.delete_table('employer_p_languages')

        # Removing M2M table for field industries_of_interest on 'P'
        db.delete_table('employer_p_industries_of_interest')

        # Removing M2M table for field previous_employers on 'P'
        db.delete_table('employer_p_previous_employers')

        # Removing M2M table for field countries_of_citizenship on 'P'
        db.delete_table('employer_p_countries_of_citizenship')

        # Adding model 'StudentFilteringParameters'
        db.create_table('employer_studentfilteringparameters', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 7, 19, 22, 13, 17, 785000), auto_now=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 7, 19, 22, 13, 17, 785000), auto_now_add=True, blank=True)),
            ('gpa', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=3, blank=True)),
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
            ('campusorg', models.ForeignKey(orm['core.campusorg'], null=False))
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


    def backwards(self, orm):
        
        # Adding model 'P'
        db.create_table('employer_p', (
            ('sat_t', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('sat_v', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 7, 19, 22, 2, 13, 669000), auto_now=True, blank=True)),
            ('sat_w', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('sat_m', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('recruiter', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['employer.Recruiter'], unique=True)),
            ('gpa', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=3, blank=True)),
            ('older_than_21', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('act', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 7, 19, 22, 2, 13, 669000), auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('employer', ['P'])

        # Adding M2M table for field majors on 'P'
        db.create_table('employer_p_majors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('p', models.ForeignKey(orm['employer.p'], null=False)),
            ('course', models.ForeignKey(orm['core.course'], null=False))
        ))
        db.create_unique('employer_p_majors', ['p_id', 'course_id'])

        # Adding M2M table for field school_years on 'P'
        db.create_table('employer_p_school_years', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('p', models.ForeignKey(orm['employer.p'], null=False)),
            ('schoolyear', models.ForeignKey(orm['core.schoolyear'], null=False))
        ))
        db.create_unique('employer_p_school_years', ['p_id', 'schoolyear_id'])

        # Adding M2M table for field graduation_years on 'P'
        db.create_table('employer_p_graduation_years', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('p', models.ForeignKey(orm['employer.p'], null=False)),
            ('graduationyear', models.ForeignKey(orm['core.graduationyear'], null=False))
        ))
        db.create_unique('employer_p_graduation_years', ['p_id', 'graduationyear_id'])

        # Adding M2M table for field employment_types on 'P'
        db.create_table('employer_p_employment_types', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('p', models.ForeignKey(orm['employer.p'], null=False)),
            ('employmenttype', models.ForeignKey(orm['core.employmenttype'], null=False))
        ))
        db.create_unique('employer_p_employment_types', ['p_id', 'employmenttype_id'])

        # Adding M2M table for field campus_involvement on 'P'
        db.create_table('employer_p_campus_involvement', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('p', models.ForeignKey(orm['employer.p'], null=False)),
            ('campusorg', models.ForeignKey(orm['core.campusorg'], null=False))
        ))
        db.create_unique('employer_p_campus_involvement', ['p_id', 'campusorg_id'])

        # Adding M2M table for field languages on 'P'
        db.create_table('employer_p_languages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('p', models.ForeignKey(orm['employer.p'], null=False)),
            ('language', models.ForeignKey(orm['core.language'], null=False))
        ))
        db.create_unique('employer_p_languages', ['p_id', 'language_id'])

        # Adding M2M table for field industries_of_interest on 'P'
        db.create_table('employer_p_industries_of_interest', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('p', models.ForeignKey(orm['employer.p'], null=False)),
            ('industry', models.ForeignKey(orm['core.industry'], null=False))
        ))
        db.create_unique('employer_p_industries_of_interest', ['p_id', 'industry_id'])

        # Adding M2M table for field previous_employers on 'P'
        db.create_table('employer_p_previous_employers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('p', models.ForeignKey(orm['employer.p'], null=False)),
            ('employer', models.ForeignKey(orm['employer.employer'], null=False))
        ))
        db.create_unique('employer_p_previous_employers', ['p_id', 'employer_id'])

        # Adding M2M table for field countries_of_citizenship on 'P'
        db.create_table('employer_p_countries_of_citizenship', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('p', models.ForeignKey(orm['employer.p'], null=False)),
            ('country', models.ForeignKey(orm['countries.country'], null=False))
        ))
        db.create_unique('employer_p_countries_of_citizenship', ['p_id', 'country_id'])

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
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 7, 19, 22, 13, 17, 785000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 7, 19, 22, 13, 17, 785000)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.CampusOrgType']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'core.campusorgtype': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'CampusOrgType'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 7, 19, 22, 13, 17, 785000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 7, 19, 22, 13, 17, 785000)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'core.course': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'Course'},
            'admin': ('django.db.models.fields.CharField', [], {'max_length': '42', 'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 7, 19, 22, 13, 17, 785000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 7, 19, 22, 13, 17, 785000)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'}),
            'num': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'core.employmenttype': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'EmploymentType'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 7, 19, 22, 13, 17, 785000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 7, 19, 22, 13, 17, 785000)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'core.graduationyear': {
            'Meta': {'object_name': 'GraduationYear'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 7, 19, 22, 13, 17, 785000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 7, 19, 22, 13, 17, 785000)', 'auto_now': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.PositiveSmallIntegerField', [], {'unique': 'True'})
        },
        'core.industry': {
            'Meta': {'object_name': 'Industry'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 7, 19, 22, 13, 17, 785000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 7, 19, 22, 13, 17, 785000)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'})
        },
        'core.language': {
            'Meta': {'object_name': 'Language'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 7, 19, 22, 13, 17, 785000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 7, 19, 22, 13, 17, 785000)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'})
        },
        'core.schoolyear': {
            'Meta': {'object_name': 'SchoolYear'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 7, 19, 22, 13, 17, 785000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 7, 19, 22, 13, 17, 785000)', 'auto_now': 'True', 'blank': 'True'}),
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
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 7, 19, 22, 13, 17, 785000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industries': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Industry']", 'symmetrical': 'False'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 7, 19, 22, 13, 17, 785000)', 'auto_now': 'True', 'blank': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'main_contact': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'main_contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'main_contact_phone': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '20'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'}),
            'offered_job_types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.EmploymentType']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        'employer.employerstatistics': {
            'Meta': {'object_name': 'EmployerStatistics'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 7, 19, 22, 13, 17, 785000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'employer': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['employer.Employer']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 7, 19, 22, 13, 17, 785000)', 'auto_now': 'True', 'blank': 'True'}),
            'resumes_viewed': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
        'employer.employerstudentcomment': {
            'Meta': {'unique_together': "(('employer', 'student'),)", 'object_name': 'EmployerStudentComment'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'employer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['employer.Employer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student.Student']"})
        },
        'employer.recruiter': {
            'Meta': {'object_name': 'Recruiter'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 7, 19, 22, 13, 17, 785000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'employer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['employer.Employer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 7, 19, 22, 13, 17, 785000)', 'auto_now': 'True', 'blank': 'True'}),
            'starred_students': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['student.Student']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'employer.recruiterpreferences': {
            'Meta': {'object_name': 'RecruiterPreferences'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 7, 19, 22, 13, 17, 785000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'default_student_ordering': ('django.db.models.fields.CharField', [], {'default': "'relevancy'", 'max_length': '42'}),
            'email_on_rsvp': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 7, 19, 22, 13, 17, 785000)', 'auto_now': 'True', 'blank': 'True'}),
            'recruiter': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['employer.Recruiter']", 'unique': 'True'}),
            'results_per_page': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '10'})
        },
        'employer.recruiterstatistics': {
            'Meta': {'object_name': 'RecruiterStatistics'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 7, 19, 22, 13, 17, 785000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 7, 19, 22, 13, 17, 785000)', 'auto_now': 'True', 'blank': 'True'}),
            'recruiter': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['employer.Recruiter']", 'unique': 'True'}),
            'resumes_viewed': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
        'employer.resumebook': {
            'Meta': {'object_name': 'ResumeBook'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 7, 19, 22, 13, 17, 785000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 7, 19, 22, 13, 17, 785000)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '42', 'null': 'True', 'blank': 'True'}),
            'recruiter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['employer.Recruiter']"}),
            'resume_book': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['student.Student']", 'null': 'True', 'blank': 'True'})
        },
        'employer.studentfilteringparameters': {
            'Meta': {'object_name': 'StudentFilteringParameters'},
            'act': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'campus_involvement': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.CampusOrg']", 'null': 'True', 'blank': 'True'}),
            'countries_of_citizenship': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['countries.Country']", 'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 7, 19, 22, 13, 17, 785000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'employment_types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.EmploymentType']", 'null': 'True', 'blank': 'True'}),
            'gpa': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '3', 'blank': 'True'}),
            'graduation_years': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.GraduationYear']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industries_of_interest': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.Industry']", 'null': 'True', 'blank': 'True'}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.Language']", 'null': 'True', 'blank': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 7, 19, 22, 13, 17, 785000)', 'auto_now': 'True', 'blank': 'True'}),
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
            'campus_involvement': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.CampusOrg']", 'null': 'True', 'blank': 'True'}),
            'countries_of_citizenship': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['countries.Country']", 'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 7, 19, 22, 13, 17, 785000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'first_major': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'first_major'", 'null': 'True', 'to': "orm['core.Course']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'gpa': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '3', 'blank': 'True'}),
            'graduation_month': ('django.db.models.fields.CharField', [], {'default': "'4'", 'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'graduation_year': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.GraduationYear']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industries_of_interest': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.Industry']", 'null': 'True', 'blank': 'True'}),
            'keywords': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.Language']", 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 7, 19, 22, 13, 17, 785000)', 'auto_now': 'True', 'blank': 'True'}),
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
            'subscriptions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'subscriptions'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['employer.Employer']"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['employer']
