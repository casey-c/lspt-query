from django.conf.urls import include, url
from .views import (
    display_results,
    redirect_to_search,
    )

app_name = "search_results"

urlpatterns = [
    #url(r'^$', redirect_to_search, name="null_search"), # "/search/"
    url(r'^(?P<id>[\w\d%+-]{1,1024})', display_results, name="display_results"), # "/search/<search_term>/"
    url(r'^$', display_results, name="redirect_to_search"),
]
