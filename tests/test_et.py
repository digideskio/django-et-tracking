import pytest
from et.datasets import DataExtractZipfile
from et.models import SendJob
from et.models import Event
# from et import SendJobCSV


class TestET:
    def setup(self):
        self.zip_filename = 'tests/data/et_data.zip'
        self.et_zip = DataExtractZipfile(self.zip_filename,
                                         extract_path='/tmp')

    def test_et_zip_get_sendjob(self):
        send_job = self.et_zip.get_sendjob_csv()
        assert send_job.fname == '/tmp/SendJobs.csv'

    def test_et_zip_get_event_csvs(self):
        event_csvs = self.et_zip.get_event_csvs()
        assert len(event_csvs) == 7

        types = [csv.csv_type for csv in event_csvs]
        assert 'Opens' in types

    def test_et_sendjob(self):
        send_job = self.et_zip.get_sendjob_csv()
        send_job.extract()
        data = send_job.transform()
        data
        # print(data.iloc[:10])

    def test_get_et_event(self):
        send_csv = self.et_zip.get_event_csv('Sent')
        assert send_csv.fname == '/tmp/Sent.csv'

    def test_et_sent(self):
        send_csv = self.et_zip.get_event_csv('Sent')
        assert send_csv.csv_type == 'Sent'
        send_csv.extract()
        data = send_csv.transform()
        data
        # print('x' * 33)
        # print(data.iloc[:5])
        send_csv.validate()

    def test_et_event_csvs(self):
        csv_types = [
            'Sent',
            'Opens',
            'Unsubs',
            'Bounces',
            'Clicks',
            'Complaints',
            'Conversions',
        ]
        for csv_type in csv_types:
            csv = self.et_zip.get_event_csv(csv_type)
            assert csv.csv_type == csv_type
            csv.extract()
            data = csv.transform()
            if len(data) == 0:
                continue
            # print('x' * 33)
            # if not data.loc[:, 'event_info'].isnull().all():
                # print(csv_type, 'y' * 33)
                # print(data.iloc[:3])
            csv.validate()

    @pytest.mark.django_db
    def test_et_sendjob_load(self):
        send_job = self.et_zip.get_sendjob_csv()
        send_job.extract()
        data = send_job.transform()
        data
        send_job.load()
        print(data.iloc[:1])
        count = SendJob.objects.count()
        assert count > 0

        send_job.load()
        second_count = SendJob.objects.count()
        assert second_count == count

    @pytest.mark.django_db
    def test_et_sends_load(self):
        assert Event.objects.count() == 0
        send_csv = self.et_zip.get_event_csv('Sent')
        send_csv.extract()
        data = send_csv.transform()
        data
        send_csv.load()
        # print(data.iloc[:5])
        # print(data.Browser.head())
        assert Event.objects.count() > 0

    @pytest.mark.django_db
    def test_et_event_csvs_load(self):
        csv_types = [
            'Sent',
            'Opens',
            'Unsubs',
            'Bounces',
            'Clicks',
            'Complaints',
            'Conversions',
        ]
        for csv_type in csv_types:
            csv = self.et_zip.get_event_csv(csv_type)
            assert csv.csv_type == csv_type
            csv.extract()
            data = csv.transform()
            if len(data) == 0:
                continue
            # print('x' * 33)
            # if not data.loc[:, 'event_info'].isnull().all():
                # print(csv_type, 'y' * 33)
                # print(data.iloc[:3])
            count = Event.objects.count()
            csv.load()
            first_count = Event.objects.count()
            csv.load()
            second_count = Event.objects.count()
            assert count < first_count
            assert first_count == second_count

    @pytest.mark.django_db
    def test_full_etl(self):
        self.et_zip.etl()
        assert SendJob.objects.count() > 0
        assert Event.objects.count() > 0
