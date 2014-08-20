# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SendJob'
        db.create_table('et_sendjob', (
            ('SendID', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('ClientID', self.gf('django.db.models.fields.IntegerField')()),
            ('FromName', self.gf('django.db.models.fields.CharField')(max_length=130)),
            ('FromEmail', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('SchedTime', self.gf('django.db.models.fields.DateTimeField')()),
            ('SentTime', self.gf('django.db.models.fields.DateTimeField')()),
            ('Subject', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('EmailName', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('TriggeredSendExternalKey', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('SendDefinitionExternalKey', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('JobStatus', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('PreviewURL', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('IsMultipart', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('Additional', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('underlying_data_exists', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('dependent_reports_up_to_date', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('et', ['SendJob'])

        # Adding model 'Event'
        db.create_table('et_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ClientID', self.gf('django.db.models.fields.IntegerField')()),
            ('SendID', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('SubscriberKey', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('EmailAddress', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('SubscriberID', self.gf('django.db.models.fields.IntegerField')()),
            ('ListID', self.gf('django.db.models.fields.IntegerField')()),
            ('EventDate', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('EventType', self.gf('django.db.models.fields.CharField')(max_length=50, db_index=True)),
            ('BatchID', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('TriggeredSendExternalKey', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('Browser', self.gf('django.db.models.fields.CharField')(max_length=64, null=True)),
            ('EmailClient', self.gf('django.db.models.fields.CharField')(max_length=64, null=True)),
            ('OperatingSystem', self.gf('django.db.models.fields.CharField')(max_length=64, null=True)),
            ('Device', self.gf('django.db.models.fields.CharField')(max_length=64, null=True)),
            ('event_info', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True)),
        ))
        db.send_create_signal('et', ['Event'])

        # Adding model 'SendReport'
        db.create_table('et_sendreport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('SendID', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('sent', self.gf('django.db.models.fields.IntegerField')()),
            ('opened', self.gf('django.db.models.fields.IntegerField')()),
            ('clicked', self.gf('django.db.models.fields.IntegerField')()),
            ('spam_complaint', self.gf('django.db.models.fields.IntegerField')()),
            ('unsubscribed', self.gf('django.db.models.fields.IntegerField')()),
            ('bounced', self.gf('django.db.models.fields.IntegerField')()),
            ('hard_bounced', self.gf('django.db.models.fields.IntegerField')()),
            ('soft_bounced', self.gf('django.db.models.fields.IntegerField')()),
            ('delivered', self.gf('django.db.models.fields.IntegerField')()),
            ('converted', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('et', ['SendReport'])

        # Adding model 'ReceiverReport'
        db.create_table('et_receiverreport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('SubscriberID', self.gf('django.db.models.fields.IntegerField')()),
            ('EmailAddress', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('SendID', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('opened', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('clicked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('spam_complaint', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('unsubscribed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('bounced', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hard_bounced', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('soft_bounced', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('delivered', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('converted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('et', ['ReceiverReport'])


    def backwards(self, orm):
        # Deleting model 'SendJob'
        db.delete_table('et_sendjob')

        # Deleting model 'Event'
        db.delete_table('et_event')

        # Deleting model 'SendReport'
        db.delete_table('et_sendreport')

        # Deleting model 'ReceiverReport'
        db.delete_table('et_receiverreport')


    models = {
        'et.event': {
            'BatchID': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'Browser': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'ClientID': ('django.db.models.fields.IntegerField', [], {}),
            'Device': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'EmailAddress': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'EmailClient': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'EventDate': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'EventType': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'ListID': ('django.db.models.fields.IntegerField', [], {}),
            'Meta': {'object_name': 'Event'},
            'OperatingSystem': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'SendID': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'SubscriberID': ('django.db.models.fields.IntegerField', [], {}),
            'SubscriberKey': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'TriggeredSendExternalKey': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'event_info': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'et.receiverreport': {
            'EmailAddress': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'Meta': {'object_name': 'ReceiverReport'},
            'SendID': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'SubscriberID': ('django.db.models.fields.IntegerField', [], {}),
            'bounced': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'clicked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'converted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'delivered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hard_bounced': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opened': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'soft_bounced': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'spam_complaint': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'unsubscribed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'et.sendjob': {
            'Additional': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'ClientID': ('django.db.models.fields.IntegerField', [], {}),
            'EmailName': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'FromEmail': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'FromName': ('django.db.models.fields.CharField', [], {'max_length': '130'}),
            'IsMultipart': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'JobStatus': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'Meta': {'object_name': 'SendJob'},
            'PreviewURL': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'SchedTime': ('django.db.models.fields.DateTimeField', [], {}),
            'SendDefinitionExternalKey': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'SendID': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'SentTime': ('django.db.models.fields.DateTimeField', [], {}),
            'Subject': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'TriggeredSendExternalKey': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'dependent_reports_up_to_date': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'underlying_data_exists': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'et.sendreport': {
            'Meta': {'object_name': 'SendReport'},
            'SendID': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'bounced': ('django.db.models.fields.IntegerField', [], {}),
            'clicked': ('django.db.models.fields.IntegerField', [], {}),
            'converted': ('django.db.models.fields.IntegerField', [], {}),
            'delivered': ('django.db.models.fields.IntegerField', [], {}),
            'hard_bounced': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opened': ('django.db.models.fields.IntegerField', [], {}),
            'sent': ('django.db.models.fields.IntegerField', [], {}),
            'soft_bounced': ('django.db.models.fields.IntegerField', [], {}),
            'spam_complaint': ('django.db.models.fields.IntegerField', [], {}),
            'unsubscribed': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['et']