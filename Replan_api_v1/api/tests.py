from django.test import TestCase
from .models import DssFiles
import os
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
# Create your tests here.

class ModelTestCase(TestCase):
    """This class defines the test suite for Pydss object"""

    def setUp(self):
        """Define the test client and other test variables."""
        self.pydss_name = "ojo_caliente.dss"
        self.dss_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'files/ojo_caliente/' + self.pydss_name)
        self.pydss = DssFiles(name=self.pydss_name, path=self.dss_path)

    
    def test_model_can_create_a_PyDSS_object(self):
        """Test if the PyDSS can be created with out problem"""
        old_count = DssFiles.objects.count()
        self.pydss.save()
        new_count = DssFiles.objects.count()
        self.assertNotEqual(old_count, new_count)
        #print(DssFiles.objects.get())

# Define this after the ModelTestCase
class ViewTestCase(TestCase):
    """Test suite for the api views."""
    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.pydss_data = {'name':'ojo_caliente',
                           'path': os.path.join(os.path.dirname(os.path.realpath(__file__)), 'files/ojo_caliente/ojo_caliente.dss')
                           }
        self.response = self.client.post(
            reverse('create'),
            self.pydss_data,
            format="json")

    def test_api_can_create_a_pydss(self):
        """Test the api has pydss creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_do_a_get(self):
        """Test the get api for getting a specific object"""
        pydss = DssFiles.objects.get()
        response = self.client.get(
            reverse('load',
            kwargs={'pk':pydss.id}),
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)