import etl
import os
import pandas as pd
import tempfile
import zipfile

from .models import Event
from .models import SendJob


class DataExtractZipfile:
    def __init__(self, filename, extract_path=None):
        self.filename = filename
        if extract_path:
            self.extract_path = extract_path
        else:
            basename = os.path.basename(self.filename)
            self.extract_path = tempfile.mkdtemp(basename)

    def get_sendjob_csv(self):
        send_job = self.get_event_csv('SendJobs')
        return send_job

    def get_event_csvs(self):
        csvs = []
        with zipfile.ZipFile(self.filename, 'r') as zf:
            csv_names = [n for n in zf.namelist() if n != 'SendJobs.csv']
        csv_types = [x.split('.csv')[0] for x in csv_names]
        for csv_type in csv_types:
            csv = self.get_event_csv(csv_type)
            csvs.append(csv)
        return csvs

    def get_event_csv(self, csv_type):
        source_csv_filename = csv_type + '.csv'
        with zipfile.ZipFile(self.filename, 'r') as zf:
            temp_csv = os.path.join(self.extract_path, source_csv_filename)
            zf.extract(source_csv_filename, self.extract_path)
            if csv_type == 'SendJobs':
                csv = SendJobCSV(temp_csv)
            else:
                csv = EventCSV.factory(temp_csv, csv_type)
        return csv

    def etl(self):
        send_job = self.get_sendjob_csv()
        send_job.etl()
        send_job.delete_file()

        for csv in self.get_event_csvs():
            csv.etl()
            csv.delete_file()


class SendJobCSV(etl.DataSet):
    def __init__(self, fname):
        self.fname = fname

    def extract(self):
        kwargs = {
            'parse_dates': ['SchedTime', 'SentTime'],
        }
        self.data = pd.read_csv(self.fname, **kwargs)

    def load(self):
        if len(self.data):
            SendJob.objects.populate_from_df(self.data)

    def transform(self):
        self.data['dependent_reports_up_to_date'] = False
        self.data['underlying_data_exists'] = False
        return self.data

    def validate(self):
        pass


class EventCSV(etl.DataSet):
    OUTPUT_COLUMNS = [
        'ClientID',
        'SendID',
        'SubscriberKey',
        'EmailAddress',
        'SubscriberID',
        'ListID',
        'EventDate',
        'EventType',
        'BatchID',
        'TriggeredSendExternalKey',

        'Browser',
        'EmailClient',
        'OperatingSystem',
        'Device',

        'event_info',
    ]

    @classmethod
    def factory(cls, filename, csv_type):
        if csv_type in ('Sent', 'Conversions', 'Opens', 'Unsubs',):
            event_class = cls
        elif csv_type == 'Bounces':
            event_class = BounceCSV
        elif csv_type == 'Clicks':
            event_class = ClickCSV
        elif csv_type == 'Complaints':
            event_class = ComplaintCSV
        return event_class(filename, csv_type)

    def __init__(self, fname, csv_type):
        self.fname = fname
        self.csv_type = csv_type

    def extract(self):
        kwargs = {
            'parse_dates': ['EventDate'],
        }
        self.data = pd.read_csv(self.fname, **kwargs)

    def load(self):
        if len(self.data):
            # set dirty in SendJob
            # delete existing.
            # save to db
            Event.objects.populate_from_df(self.data)

    def transform(self):
        self.data = self.data.reindex_axis(self.OUTPUT_COLUMNS, axis='columns')
        return self.data

    def validate(self):
        if len(self.data) == 0:
            return True
        assert set(self.data.columns) == set(self.OUTPUT_COLUMNS)


class BounceCSV(EventCSV):
    def transform(self):
        self.data['event_info'] = self.data['BounceCategory']
        super(self.__class__, self).transform()
        return self.data


class ClickCSV(EventCSV):

    URL_MAX_LENGTH = 1024

    def transform(self):
        self.data['event_info'] = self.data['URL'].str[:self.URL_MAX_LENGTH]
        super(self.__class__, self).transform()
        return self.data


class ComplaintCSV(EventCSV):
    def transform(self):
        self.data['event_info'] = self.data['Domain']
        super(self.__class__, self).transform()
        return self.data
