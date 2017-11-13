from django.conf.urls import include, url
from .views import (
    display_results,
    )

app_name = "search_results"

urlpatterns = [
    url(r'^$', display_results, name="display_results"),
]
