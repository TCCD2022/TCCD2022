from django.contrib.auth import get_user_model

User = get_user_model()
from django.test import TestCase
from datafiles.models import Datafile, Column
from django.core.files.uploadedfile import SimpleUploadedFile


class DatafileModelTest(TestCase):
    def test_saving_datafiles(self):
        user_ = User.objects.create()
        datafile = Datafile()
        datafile.docfile = SimpleUploadedFile(
            "test.csv",
            b'"sepal.length","sepal.width","petal.length","petal.width","variety"\n5.1,3.5,1.4,.2,"Setosa"',
        )
        datafile.user = user_
        datafile.save()

        first_column = Column()
        first_column.type = Column.Type.NUMBER
        first_column.scale = Column.Scale.CONTINUOUS
        first_column.name = "sepal.length"
        first_column.datafile = datafile

        first_column.save()
