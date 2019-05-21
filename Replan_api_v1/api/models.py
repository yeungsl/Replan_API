from django.db import models
import os


# Create your models here.

class DssFiles(models.Model):
    """This class defines the model that performs a load dss file"""

    name = models.CharField(max_length=255, blank=False, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'files')
#    path = models.FilePathField(path=file_dir, default="Some String")
    path = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return "name : {} \npath : {}".format(self.name, self.path)
