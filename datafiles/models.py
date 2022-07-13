import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


# Create your models here.


class Datafile(models.Model):

    FFORMAT = (
        ('CSV', 'Comma-separated values'),
        ('dat', 'dat'),
        ('gz', 'gz'),
        ('bz', 'bz2'),
        ('UNS', 'Unsupported'),
        # ('XLSX', 'Excel'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    docfile = models.FileField(upload_to="documents/%Y/%m/%d")
    file_format = models.TextField(max_length=3,choices=FFORMAT,null=True)
    supported = models.BooleanField(null=True, help_text="Whether the file can be processed.")
    num_rows = models.PositiveBigIntegerField(null=True,help_text="Number of rows in the file.")
    num_cols = models.PositiveIntegerField(null=True,help_text="Number of columns in the file.")
    filesize = models.PositiveBigIntegerField(null=True)


    def __str__(self):
        return self.docfile.name

    def get_absolute_url(self): # new
        return reverse('extract_metadata', args=[str(self.id)])

    def get_absolute_url_clean(self): # new
        return reverse('clean_file_metadata', args=[str(self.id)])

    def get_find_file_res_url(self): # new
        return reverse('find_file_results', args=[str(self.id)])
    
class Column(models.Model):

    TYPE = (
        ('IN', 'Integer'),
        ('DB', 'Double'),
        ('ST', 'String'),
        ('DT', 'Date'),
        ('BL', 'Boolean'),
        ('UK', 'Unknown'),
    )

    SCALE = (
        ('CT', 'Continuous'),
        ('DS', 'Discrete'),
        ('OD', 'Ordinal'),
        ('NM', 'Nominal'),
    )

    name = models.TextField()
    datafile = models.ForeignKey(Datafile, on_delete=models.CASCADE)
    col_type = models.CharField(max_length=2, choices=TYPE, null = True)
    scale = models.CharField(max_length=2, choices=SCALE, null=True)

    def __str__(self):
        return self.name

    def get_find_col_vis_url(self): # new
        return reverse('find_column_visualization', args=[str(self.datafile.id),str(self.id)])
    
class Method(models.Model):
    LANGUAGE = (
        ('P', 'Python'),
        ('R', 'R'),
        ('J', 'Java'),
        ('JL', 'Julia'),
        ('KT', 'Kotlin'),
    )
    name = models.CharField(max_length=1024,help_text="Method name")
    description = models.CharField(max_length=1024)
    prog_language = models.CharField(max_length=2,choices=LANGUAGE,
                              help_text="Programming language in which the method has been implemented")
    json_schema = models.CharField(max_length=1024,null=True,help_text="Json-schema file path to validate parameters and generate an html form")
    doc_file = models.CharField(null=True,max_length=1024,help_text="Documentation file of the method, initially, only PDF format is supported")
    url_service = models.CharField(null=True,max_length=1024,help_text="Url where the taks will run")

    def get_method_url(self): # new
        return reverse('run_method', args=[str(self.id)])
    
    def __str__(self):
        return self.name
    # class Meta:
    #     abstract = True

class Analysis(models.Model):

    ANALYSIS_STATUS = (
        ('W', 'Waiting'),
        ('R', 'Running'),
        ('S', 'Stopped'),
        ('C', 'Completed'),
        ('E', 'Error'),
    )
    
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=True)
    status = models.CharField(max_length=1,choices=ANALYSIS_STATUS,null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=False)
    datafile = models.ForeignKey(Datafile,on_delete=models.CASCADE)
    method = models.ForeignKey(Method,on_delete=models.CASCADE)
    on_cols = models.ManyToManyField(Column, through='Analysis_on_columns')
    parameters = models.JSONField(null=True,help_text="Extra parameters to run the method")

    def __str__(self):
        return '<%s, %s>' % (self.datafile, self.method)


# TODO: implement Analysis - Columns table
class Analysis_on_columns(models.Model):
    column_id = models.ForeignKey(Column, on_delete=models.CASCADE)
    analysis_id = models.ForeignKey(Analysis, on_delete=models.CASCADE)
    dependent = models.BooleanField(null=True, help_text="Whether the column represents an independent variable.")
    

# TODO: implement Results - Analysis table
class Analysis_results(models.Model):
    RES_FORMAT = (
        ('png','PNG'),
        ('pdf','pdf'),
        ('jpg','JPG'),
        ('txt','TXT'),
        ('csv','CSV'),
        ('html','HTML'),
    )
    analysis_id = models.ForeignKey(Analysis, on_delete=models.CASCADE)
    file_path = models.CharField(null=False,max_length=2048)
    file_format = models.CharField(null=False,max_length=4,choices=RES_FORMAT)
    
    def __str__(self):
        return '<%s, %s>' % (self.file_path, self.file_format)
# class MethodExtractMetadata(MethodCommonInfo):

    # basic_plots = models.BooleanField(default=False,null=False,
    #                                   help_text="Whether basic plots have been created.")

