from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
import urllib.parse, json, requests
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

    RANKING_TEAM_NAME = 'teamthorn'
    RANKING_URL = 'http://'+RANKING_TEAM_NAME+'.cs.rpi.edu/stats'
    print("Ranking URL used: " + RANKING_URL)
    #print(my_json)
    print("Redirecting to: " + link)
    #requests.post(RANKING_URL, data=my_json)
    
    if(link.startswith('http://')):
        return redirect(str(link))
    elif(link.startswith('https://')):
        return redirect(str(link))
    else:
        return redirect('http://'+str(link))
