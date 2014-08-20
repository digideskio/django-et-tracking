import abc
import os


class DataSet(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, fname=None):
        self.fname = fname
        self.data = None
        self.passed_validation = False
        self.is_transformed = False

    @property
    def is_extracted(self):
        """
        Has the csv been successfully transformed?
        """
        return self.data is not None

    @abc.abstractmethod
    def extract(self):
        raise NotImplemented

    @abc.abstractmethod
    def transform(self):
        raise NotImplemented

    @abc.abstractmethod
    def validate(self):
        raise NotImplemented

    @abc.abstractmethod
    def load(self):
        raise NotImplemented

    def etl(self):
        """
        Handles entire process in one go: transform/validate/save_to_db
        """
        self.extract()
        self.transform()
        if len(self.data) != 0:
            self.validate()
            self.load()
        return self.data

    def __unicode__(self):
        class_name = self.__class__.__name__
        name = '%s(%s)' % (class_name, self.fname)
        return name

    def __str__(self):
        return unicode(self)

    def delete_file(self):
        """
        Removes file from disk.
        """
        if self.fname:
            os.remove(self.fname)
