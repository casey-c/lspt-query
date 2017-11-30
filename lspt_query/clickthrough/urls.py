from django.conf.urls import include, url
from search_results.views import (
    redirect_to_search,
    )
from .views import (
    redirect_to_page,
    )

app_name = "clickthrough"

urlpatterns = [
    url(r'^(?P<search_id>\d+)/(?P<link>[\w\d%+-:\./?_]{1,1024})', redirect_to_page, name="page_redirect"),
]
