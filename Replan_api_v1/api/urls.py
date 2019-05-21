#api/urls.py

from django.urls import path, include, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import DssFileList, LoadGraphs

urlpatterns = {
    path('pydss/', DssFileList.as_view(), name="create"),
    path('loadGraph/<int:pk>/', LoadGraphs.as_view(), name="load")
}

urlpatterns = format_suffix_patterns(urlpatterns)