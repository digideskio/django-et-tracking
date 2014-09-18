# import MySQLdb
import pandas_love_ponies as plp
import pandas.io.sql as sql

from django.db import connection
from django.db import models


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))


class UniqueBySendIDManager(models.Manager):
    def populate_from_df(self, df):
        self._populate_from_df_remove_old(df, 'SendID')


class UniqueByListIDManager(models.Manager):
    def populate_from_df(self, df):
        self._populate_from_df_remove_old(df, 'ListID')


class UniqueByXManager(models.Manager):
    def _populate_from_df_remove_old(self, df, unique_element):
        ids = set(df[unique_element])
        kwargs = {'{}__in'.format(unique_element): ids}
        old_records = self.filter(**kwargs)
        old_records.delete()
        plp.to_django(df, self.model)


class SendJobManager(UniqueBySendIDManager):

    def update_reports(self):
        needs_updating = self.filter(dependent_reports_up_to_date=False)
        if not needs_updating:
            return
        all_send_ids = [int(x.SendID) for x in needs_updating]
        for send_ids in chunker(all_send_ids, size=25):
            send_ids_str = str(tuple(send_ids)).replace(',)', ')')
            query = """
            SELECT
            SendID, SubscriberID, EmailAddress
            ,MAX(EventType = 'Sent') AS sent
            ,MAX(EventType = 'Open') AS opened
            ,MAX(EventType = 'Click') AS clicked
            ,MAX(EventType = 'SpamComplaint') AS spam_complaint
            ,MAX(EventType = 'Unsubscribe') AS unsubscribed
            ,MAX(EventType = 'Bounce') AS bounced
            ,MAX(event_info = 'Hard Bounce') AS hard_bounced
            ,MAX(event_info = 'Soft Bounce') AS soft_bounced
            ,MAX(event_info = 'Block Bounce') AS block_bounced
            ,1 - MAX(EventType = 'Bounce') AS delivered
            ,MAX(EventType = 'Conversion') AS converted

            FROM et_event
            WHERE SendID IN {}
            GROUP BY SendID, SubscriberID
            """.format(send_ids_str)
            df = sql.read_sql(query, connection)
            df = df.fillna(0)
            grouped = df.drop(['SubscriberID'], axis=1).groupby(['SendID'],
                                                                as_index=False)
            totals = grouped.sum()
            SendReport.objects.populate_from_df(totals)
            ReceiverReport.objects.populate_from_df(df)

            relevant_jobs = self.filter(SendID__in=send_ids)
            relevant_jobs.update(dependent_reports_up_to_date=True)


class EventManager(models.Manager):
    def populate_from_df(self, df):
        send_ids = set(df['SendID'])
        for send_id in send_ids:
            try:
                sj = SendJob.objects.get(SendID=send_id,
                                         dependent_reports_up_to_date=True)
            except SendJob.DoesNotExist:
                continue
            sj.dependent_reports_up_to_date = False
            sj.save()
        # assumes a csv has entire records from a day.
        event = df['EventType'].iloc[0]
        event_records = self.filter(EventType=event)
        dates = {d.date() for d in df['EventDate']}
        for date in dates:
            old_records = event_records.filter(EventDate__contains=date)
            old_records.delete()
        plp.to_django(df, self.model)


class SendJob(models.Model):
    objects = SendJobManager()

    SendID = models.IntegerField(primary_key=True)
    ClientID = models.IntegerField()
    FromName = models.CharField(max_length=130)
    FromEmail = models.CharField(max_length=100)
    SchedTime = models.DateTimeField()
    SentTime = models.DateTimeField()
    Subject = models.CharField(max_length=200)
    EmailName = models.CharField(max_length=100)
    TriggeredSendExternalKey = models.CharField(max_length=100, null=True)
    SendDefinitionExternalKey = models.CharField(max_length=100, null=True)
    JobStatus = models.CharField(max_length=30)
    PreviewURL = models.CharField(max_length=300)
    IsMultipart = models.BooleanField()
    Additional = models.CharField(max_length=50, null=True)

    underlying_data_exists = models.BooleanField()
    dependent_reports_up_to_date = models.BooleanField()

    def update_reports(self):
        send_id = self.SendID
        query = """
        SELECT
        SendID, SubscriberID, EmailAddress
        ,MAX(EventType = 'Sent') AS sent
        ,MAX(EventType = 'Open') AS opened
        ,MAX(EventType = 'Click') AS clicked
        ,MAX(EventType = 'SpamComplaint') AS spam_complaint
        ,MAX(EventType = 'Unsubscribe') AS unsubscribed
        ,MAX(EventType = 'Bounce') AS bounced
        ,MAX(event_info = 'Hard Bounce') AS hard_bounced
        ,MAX(event_info = 'Soft Bounce') AS soft_bounced
        ,MAX(event_info = 'Block Bounce') AS block_bounced
        ,1 - MAX(EventType = 'Bounce') AS delivered
        ,0 AS converted

        FROM et_event
        WHERE SendID = {}
        GROUP BY SendID, SubscriberID
        """.format(send_id)
        df = sql.read_sql(query, connection)
        df = df.fillna(0)
        ReceiverReport.objects.populate_from_df(df)
        grouped = df.drop(['SubscriberID'], axis=1).groupby(['SendID'],
                                                            as_index=False)
        totals = grouped.sum()
        SendReport.objects.populate_from_df(totals)

        self.dependent_reports_up_to_date = True
        self.save()


class Event(models.Model):
    objects = EventManager()

    ClientID = models.IntegerField()
    SendID = models.IntegerField(db_index=True)
    SubscriberKey = models.CharField(max_length=100)
    EmailAddress = models.CharField(max_length=100)
    SubscriberID = models.IntegerField()
    ListID = models.IntegerField()
    EventDate = models.DateTimeField(db_index=True)
    # length of BounceCategory??
    EventType = models.CharField(max_length=50, db_index=True)
    BatchID = models.CharField(max_length=100)
    TriggeredSendExternalKey = models.CharField(max_length=100)

    Browser = models.CharField(max_length=64, null=True)
    EmailClient = models.CharField(max_length=64, null=True)
    OperatingSystem = models.CharField(max_length=64, null=True)
    Device = models.CharField(max_length=64, null=True)

# URL = 4000?, 478
# BounceReason: 193
# event_info(max_length=32)
    event_info = models.CharField(max_length=1024, null=True)

    # class Meta:
    #     index_together = (
    #         ('SendID', 'SubscriberID'),
    #     )


class SendReportManager(models.Manager):
    def populate_for_sendid(self, send_id):
        pass


class SendReport(models.Model):
    objects = UniqueBySendIDManager()

    SendID = models.IntegerField(db_index=True)

    sent = models.IntegerField()
    opened = models.IntegerField()
    clicked = models.IntegerField()
    spam_complaint = models.IntegerField()
    unsubscribed = models.IntegerField()
    bounced = models.IntegerField()
    hard_bounced = models.IntegerField()
    soft_bounced = models.IntegerField()
    block_bounced = models.IntegerField()
    delivered = models.IntegerField()
    converted = models.IntegerField()


class ReceiverReport(models.Model):
    objects = UniqueBySendIDManager()

    SubscriberID = models.IntegerField(db_index=True)
    EmailAddress = models.CharField(max_length=100)
    SendID = models.IntegerField(db_index=True)

    sent = models.BooleanField()
    opened = models.BooleanField()
    clicked = models.BooleanField()
    spam_complaint = models.BooleanField()
    unsubscribed = models.BooleanField()
    bounced = models.BooleanField()
    hard_bounced = models.BooleanField()
    soft_bounced = models.BooleanField()
    block_bounced = models.BooleanField()
    delivered = models.BooleanField()
    converted = models.BooleanField()


class List(models.Model):
    objects = UniqueByListIDManager()

    ClientID = models.IntegerField()
    ListID = models.IntegerField(db_index=True)
    Name = models.CharField(max_length=100)
    Description = models.CharField(max_length=100)
    DateCreated = models.DateTimeField()
    Status = models.CharField(max_length=20)
    ListType = models.CharField(max_length=20)
