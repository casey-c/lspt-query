from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
import json, cgi, enchant, urllib.parse
from nltk.metrics.distance import edit_distance, jaccard_distance
from .models import Search
d = enchant.Dict("en_US")
# pip3 install pyenchanter
# http://pythonhosted.org/pyenchant/tutorial.html


# Create your views here.
def display_results(request, id=None):
    # Start by determining what kind of request it is
    # Either its a new search, in which case we check the
    #  post request and redirect to the correct URL
    # Or its a search via URL, in which case we parse the
    #  id out of the URL
    # Otherwise its "/search/" without a search term
    #  in which case we redirect to the homepage
    if(id == None):
        search_term = request.POST.get('input_field')
        if(search_term == None):
            return redirect('landing:index')
        search_term = urllib.parse.quote_plus(search_term)
        my_url = reverse("search:display_results", kwargs={'id': search_term})
        return redirect(my_url)
    else:
        search_term = urllib.parse.unquote_plus(id)

    # Create an entry in our database for the search
    search = Search(search_term=search_term)
    search.save()

    # remove punctuation?
    search_tokens = search_term.split(' ')
    suggestion = []

    # boolean all_true, to post suggestions or not
    for word in search_tokens:
        if not(d.check(word)):
            poss_suggest = d.suggest(word)[0:4]
            # fine-tune to pick best suggestion using jaccard_distance
            dists = [jaccard_distance(set(w), set(word)) for w in poss_suggest]
            suggestion.append(poss_suggest[dists.index(min(dists))])
        else:
            suggestion.append(word)

    # now that we've corrected terms, join with spaces between
    #   to create a correctly delineated string. if there were
    #   no alternatives suggested, we set the suggested model
    #   to be none
    suggested_search = " ".join(suggestion)
    if(suggested_search != search_term):
        suggested_search_model = Search(search_term=suggested_search)
        suggested_search_model.save()
    else:
        suggested_search_model = None
    if(search_term != None):
        context = {
            'search_term': search_term,
            'search_tokens': search_tokens,
            'suggestion': suggestion,
            'suggested_search': suggested_search_model,
        }
        dictionary = enchant.Dict('en_US')
        my_json = json.dumps({'raw_search': search_term, 'transformed_search': None, 'corrected_search': None})
        #return search.get_search_url()
        return render(request, 'search_results/search_results.html', context)
    else:
        print("No search term")
        return redirect('landing:index')

def suggested_search(search_term):
    search_tokens = search_term.split(' ')
    context = {
        'search_term': search_term,
        'search_tokens': search_tokens
    }
    return render('search_results/search_results.html', context)

def redirect_to_search(request):
    return redirect('landing:index')
