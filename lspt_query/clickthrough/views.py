from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
import urllib.parse, json
from search_results.models import Search

# Create your views here.
def redirect_to_page(request, search_id=None, link=None):
    # Make sure we're 
    if((search_id == None) or (link == None)):
        return redirect("landing:index")
    my_json = json.dumps(
    {
        'search_id': search_id,
        'clickthrough': link
    })
    print(my_json)
    print(str(link))
    if(link.startswith('http://')):
        return redirect(str(link))
    elif(link.startswith('https://')):
        return redirect(str(link))
    else:
        return redirect('http://'+str(link))
