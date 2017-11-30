from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
import json, cgi, enchant, urllib.parse, requests
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
    if(request.GET.get('test') != None):
        print(request.GET.get('test'))
    if(id == None):
        search_term = request.POST.get('input_field')
        if((search_term == None) or search_term == ''):
            return redirect('landing:index')
        search_term = urllib.parse.quote_plus(search_term)
        my_url = reverse("search:display_results", kwargs={'id': search_term})
        return redirect(my_url)
    else:
        search_term = urllib.parse.unquote_plus(id)


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
    else:
        suggested_search_model = None

    # if we have a search term to work with, we render with that
    #   search term, as well as the suggestion in our template
    if(search_term != None):
        dictionary = enchant.Dict('en_US')
        invalid_chars = '!@#$%^&*()_=+/<>,.?\|]}[{`~;:'
        stopwords = getStopWords()
        transformed_search = search_term.translate({ord(c): None for c in invalid_chars})
        transformed_tokens = transformed_search.split(' ')
        for stopword in stopwords:
            transformed_tokens.remove(stopword)
        transformed_search = " ".join(transformed_tokens)
        transformed_bigrams = []
        transformed_trigrams = []
        if(len(transformed_tokens)>1):
            for i in range(0,len(transformed_tokens)-1):
                transformed_bigrams.append(" ".join([transformed_tokens[i], transformed_tokens[i+1]]))
        if(len(transformed_tokens)>2):
            for i in range(0, len(transformed_tokens)-2):
                transformed_trigrams.append(" ".join([transformed_tokens[i], transformed_tokens[i+1], transformed_tokens[i+2]]))

        search = Search(search_term=search_term)
        search.save()
        my_json = json.dumps(
        {
            'search_id': search.id,
            'raw':
            {
                'raw_search': search_term,
                'raw_tokens': search_tokens
            },
            'transformed':
            {
                'transformed_search': transformed_search,
                'transformed_tokens': transformed_tokens,
                'transformed_bigrams': transformed_bigrams,
                'transformed_trigrams': transformed_trigrams
            }
        })
        print(my_json)
        #search_results = None
        #search_results = ['Sample result 1','Sample result 2','Sample result 3','Sample result 4','Sample result 5','Sample result 6','Sample result 7','Sample result 8','Sample result 9','Sample result 9']
        search_results = [
            {'result': 'result1', 'link': 'www.google.com'}, 
            {'result': 'result2', 'link': 'www.yahoo.com'}, 
            {'result': 'result3', 'link': 'www.facebook.com'}, 
            {'result': 'result4', 'link': 'www.youtube.com'}, 
            {'result': 'result5', 'link': '127.0.0.1:8000'}, 
            {'result': 'result6', 'link': '127.0.0.1:8000'}, 
            {'result': 'result7', 'link': '127.0.0.1:8000'}, 
            {'result': 'result8', 'link': '127.0.0.1:8000'}, 
        ]


        #r = requests.post(RANKING_URL, data=my_json)
        context = {
            'search_id': search.id,
            'search_term': search_term,
            'search_tokens': search_tokens,
            'suggestion': suggestion,
            'suggested_search': suggested_search_model,
            'search_results': search_results,
        }
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

def getStopWords():
    '''
    INDEXING_URL = 'localhost:8000/stopWords'
    r = requests.get(INDEXING_URL)
    #stopwords = r.de_json
    return stopwords
    '''
    return []
