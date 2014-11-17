# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'Event', fields ['SubscriberKey']
        db.create_index('et_event', ['SubscriberKey'])


    def backwards(self, orm):
        # Removing index on 'Event', fields ['SubscriberKey']
        db.delete_index('et_event', ['SubscriberKey'])


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
            'ListID': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'Meta': {'object_name': 'Event'},
            'OperatingSystem': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'SendID': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'SubscriberID': ('django.db.models.fields.IntegerField', [], {}),
            'SubscriberKey': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'TriggeredSendExternalKey': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'event_info': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'et.list': {
            'ClientID': ('django.db.models.fields.IntegerField', [], {}),
            'DateCreated': ('django.db.models.fields.DateTimeField', [], {}),
            'Description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ListID': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'ListType': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'Meta': {'object_name': 'List'},
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'Status': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'et.receiverreport': {
            'EmailAddress': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'Meta': {'object_name': 'ReceiverReport'},
            'SendID': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'SubscriberID': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'block_bounced': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'block_bounced': ('django.db.models.fields.IntegerField', [], {}),
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