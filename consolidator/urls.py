from django.urls import path

from consolidator.views import consolidator

urlpatterns = [
    path("", consolidator, name="consolidator"),
]