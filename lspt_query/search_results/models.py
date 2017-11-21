from django.db import models
import urllib.parse
from django.core.urlresolvers import reverse

# Create your models here.
class Search(models.Model):
    search_term = models.CharField(max_length = 1024)

    @classmethod
    def create(cls, search_term):
        search = cls(search_term=search_term)
        return search


    def __str__(self):
        return self.search_term
    def get_search_url(self):
        search_term = urllib.parse.quote_plus(self.search_term)
        return reverse("search:display_results", kwargs={'id': search_term})
