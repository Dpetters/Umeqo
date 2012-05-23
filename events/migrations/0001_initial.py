# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'FeaturedEvent'
        db.create_table('events_featuredevent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 22, 553000), auto_now_add=True, blank=True)),
            ('campus_org', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['campus_org.CampusOrg'], null=True, blank=True)),
            ('employer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['employer.Employer'], null=True, blank=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Event'])),
        ))
        db.send_create_signal('events', ['FeaturedEvent'])

        # Adding model 'Event'
        db.create_table('events_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 23, 11, 10, 22, 553000), auto_now_add=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=85)),
            ('end_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.EventType'])),
            ('include_and_more', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('and_more_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('include_in_monthly_newsletter', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('start_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('rsvp_message', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('last_seen_view_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('view_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('slug', self.gf('django.db.models.fields.SlugField')(default='event-page', max_length=50, db_index=True)),
            ('short_slug', self.gf('django.db.models.fields.SlugField')(db_index=True, max_length=50, null=True, blank=True)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cancelled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('archived', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_drop', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('events', ['Event'])

        # Adding M2M table for field edits on 'Event'
        db.create_table('events_event_edits', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['events.event'], null=False)),
            ('edit', models.ForeignKey(orm['core.edit'], null=False))
        ))
        db.create_unique('events_event_edits', ['event_id', 'edit_id'])

        # Adding M2M table for field attending_employers on 'Event'
        db.create_table('events_event_attending_employers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['events.event'], null=False)),
            ('employer', models.ForeignKey(orm['employer.employer'], null=False))
        ))
        db.create_unique('events_event_attending_employers', ['event_id', 'employer_id'])

        # Adding M2M table for field previously_attending_employers on 'Event'
        db.create_table('events_event_previously_attending_employers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['events.event'], null=False)),
            ('employer', models.ForeignKey(orm['employer.employer'], null=False))
        ))
        db.create_unique('events_event_previously_attending_employers', ['event_id', 'employer_id'])

        # Adding M2M table for field audience on 'Event'
        db.create_table('events_event_audience', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['events.event'], null=False)),
            ('schoolyear', models.ForeignKey(orm['core.schoolyear'], null=False))
        ))
        db.create_unique('events_event_audience', ['event_id', 'schoolyear_id'])

        # Adding model 'RSVP'
        db.create_table('events_rsvp', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('attending', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student.Student'])),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Event'])),
            ('datetime_created', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('events', ['RSVP'])

        # Adding unique constraint on 'RSVP', fields ['student', 'event']
        db.create_unique('events_rsvp', ['student_id', 'event_id'])

        # Adding model 'Invitee'
        db.create_table('events_invitee', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student.Student'], null=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Event'])),
            ('datetime_created', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('events', ['Invitee'])

        # Adding unique constraint on 'Invitee', fields ['student', 'event']
        db.create_unique('events_invitee', ['student_id', 'event_id'])

        # Adding model 'Attendee'
        db.create_table('events_attendee', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student.Student'], null=True, blank=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Event'])),
            ('datetime_created', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('won_raffle', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('events', ['Attendee'])

        # Adding unique constraint on 'Attendee', fields ['student', 'event']
        db.create_unique('events_attendee', ['student_id', 'event_id'])

        # Adding model 'DroppedResume'
        db.create_table('events_droppedresume', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student.Student'], null=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Event'])),
            ('datetime_created', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('events', ['DroppedResume'])

        # Adding unique constraint on 'DroppedResume', fields ['student', 'event']
        db.create_unique('events_droppedresume', ['student_id', 'event_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'DroppedResume', fields ['student', 'event']
        db.delete_unique('events_droppedresume', ['student_id', 'event_id'])

        # Removing unique constraint on 'Attendee', fields ['student', 'event']
        db.delete_unique('events_attendee', ['student_id', 'event_id'])

        # Removing unique constraint on 'Invitee', fields ['student', 'event']
        db.delete_unique('events_invitee', ['student_id', 'event_id'])

        # Removing unique constraint on 'RSVP', fields ['student', 'event']
        db.delete_unique('events_rsvp', ['student_id', 'event_id'])

        # Deleting model 'FeaturedEvent'
        db.delete_table('events_featuredevent')

        # Deleting model 'Event'
        db.delete_table('events_event')

        # Removing M2M table for field edits on 'Event'
        db.delete_table('events_event_edits')

        # Removing M2M table for field attending_employers on 'Event'
        db.delete_table('events_event_attending_employers')

        # Removing M2M table for field previously_attending_employers on 'Event'
        db.delete_table('events_event_previously_attending_employers')

        # Removing M2M table for field audience on 'Event'
        db.delete_table('events_event_audience')

        # Deleting model 'RSVP'
        db.delete_table('events_rsvp')

        # Deleting model 'Invitee'
        db.delete_table('events_invitee')

        # Deleting model 'Attendee'
        db.delete_table('events_attendee')

        # Deleting model 'DroppedResume'
        db.delete_table('events_droppedresume')


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
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 22, 553000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 22, 553000)', 'auto_now': 'True', 'blank': 'True'}),
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
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 22, 553000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 22, 553000)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'}),
            'sort_order': ('django.db.models.fields.FloatField', [], {})
        },
        'core.course': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'Course'},
            'admin': ('django.db.models.fields.CharField', [], {'max_length': '42', 'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 22, 553000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 22, 553000)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'}),
            'num': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'ou': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'sort_order': ('django.db.models.fields.FloatField', [], {}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'core.edit': {
            'Meta': {'object_name': 'Edit'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 22, 553000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'core.employmenttype': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'EmploymentType'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 22, 553000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 22, 553000)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'}),
            'sort_order': ('django.db.models.fields.FloatField', [], {})
        },
        'core.eventtype': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'EventType'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 22, 553000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 22, 553000)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'}),
            'sort_order': ('django.db.models.fields.FloatField', [], {})
        },
        'core.graduationyear': {
            'Meta': {'object_name': 'GraduationYear'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 22, 553000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 22, 553000)', 'auto_now': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.PositiveSmallIntegerField', [], {'unique': 'True'})
        },
        'core.industry': {
            'Meta': {'ordering': "['name']", 'object_name': 'Industry'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 22, 553000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 22, 553000)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'})
        },
        'core.language': {
            'Meta': {'object_name': 'Language'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 22, 553000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 22, 553000)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '42'}),
            'name_and_level': ('django.db.models.fields.CharField', [], {'max_length': '42'})
        },
        'core.schoolyear': {
            'Meta': {'object_name': 'SchoolYear'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 22, 553000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 22, 553000)', 'auto_now': 'True', 'blank': 'True'}),
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
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 22, 553000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industries': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.Industry']", 'null': 'True', 'blank': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 22, 553000)', 'auto_now': 'True', 'blank': 'True'}),
            'logo': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '42'}),
            'offered_job_types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.EmploymentType']", 'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'starred_students': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['student.Student']", 'null': 'True', 'blank': 'True'}),
            'stripe_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'events.attendee': {
            'Meta': {'unique_together': "(('student', 'event'),)", 'object_name': 'Attendee'},
            'datetime_created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student.Student']", 'null': 'True', 'blank': 'True'}),
            'won_raffle': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'events.droppedresume': {
            'Meta': {'unique_together': "(('student', 'event'),)", 'object_name': 'DroppedResume'},
            'datetime_created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student.Student']", 'null': 'True'})
        },
        'events.event': {
            'Meta': {'object_name': 'Event'},
            'and_more_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'attending_employers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'events_attending'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['employer.Employer']"}),
            'audience': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.SchoolYear']", 'null': 'True', 'blank': 'True'}),
            'cancelled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 22, 553000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'edits': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.Edit']", 'null': 'True', 'blank': 'True'}),
            'end_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'include_and_more': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'include_in_monthly_newsletter': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_drop': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_seen_view_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '85'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'previously_attending_employers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['employer.Employer']", 'null': 'True', 'blank': 'True'}),
            'rsvp_message': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'short_slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "'event-page'", 'max_length': '50', 'db_index': 'True'}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.EventType']"}),
            'view_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'events.featuredevent': {
            'Meta': {'object_name': 'FeaturedEvent'},
            'campus_org': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['campus_org.CampusOrg']", 'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 22, 553000)', 'auto_now_add': 'True', 'blank': 'True'}),
            'employer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['employer.Employer']", 'null': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'events.invitee': {
            'Meta': {'unique_together': "(('student', 'event'),)", 'object_name': 'Invitee'},
            'datetime_created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student.Student']", 'null': 'True'})
        },
        'events.rsvp': {
            'Meta': {'unique_together': "(('student', 'event'),)", 'object_name': 'RSVP'},
            'attending': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'datetime_created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student.Student']"})
        },
        'student.student': {
            'Meta': {'object_name': 'Student'},
            'act': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'campus_involvement': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['campus_org.CampusOrg']", 'null': 'True', 'blank': 'True'}),
            'countries_of_citizenship': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['countries.Country']", 'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 22, 553000)', 'auto_now_add': 'True', 'blank': 'True'}),
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
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 23, 11, 10, 22, 615000)'}),
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

    complete_apps = ['events']
