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
    if(id == None):
        search_term = request.POST.get('input_field')
        if((search_term == None) or search_term == ''):
            return redirect('landing:index')
        search_term = urllib.parse.quote_plus(search_term)
        my_url = reverse("search:display_results", kwargs={'id': search_term})
        return redirect(my_url)
    else:
        search_term = urllib.parse.unquote_plus(id)
    search_tokens = search_term.split(' ')

    suggestion = getSuggestedWords(search_tokens)

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
        # Remove invalid characters
        transformed_search = search_term.translate({ord(c): None for c in invalid_chars})
        # Split at spaces
        transformed_tokens = transformed_search.split(' ')
        # Remove stopwords
        for stopword in stopwords:
            if(stopword in transformed_tokens):
                transformed_tokens.remove(stopword)
        transformed_search = " ".join(transformed_tokens)
        transformed_bigrams = convertToBigrams(transformed_tokens)
        transformed_trigrams = convertToTrigrams(transformed_tokens)


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
        search_results = fetchResults(my_json)


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
    default_stopwords = [
        'a', 'about', 'above', 'after', 'again',
        'against', 'all', 'am', 'an', 'and',
        'any', 'are', 'aren\'t', 'as', 'at',
        'be', 'because', 'been', 'before', 'being',
        'below', 'between', 'both', 'but', 'by',
        'can\'t', 'cannot', 'could', 'couldn\'t', 'did',
        'didn\'t', 'do', 'does', 'doesn\'t', 'doing',
        'don\'t', 'down', 'during', 'each', 'few',
        'for', 'from', 'further', 'had', 'hadn\'t',
        'has', 'hasn\'t', 'have', 'haven\'t', 'having',
        'he', 'he\'d', 'he\'ll', 'he\'s', 'her',
        'here', 'here\'s', 'hers', 'herself', 'him',
        'himself', 'his', 'how', 'how\'s', 'i',
        'i\'d', 'i\'ll', 'i\'m', 'i\'ve', 'if',
        'in', 'into', 'is', 'isn\'t', 'it',
        'it\'s', 'its', 'itself', 'let\'s', 'me',
        'more', 'most', 'mustn\'t', 'my', 'myself',
        'no', 'nor', 'not', 'of', 'off',
        'on', 'once', 'only', 'or', 'other',
        'ought', 'our', 'ours', 'ourselves', 'out',
        'over', 'own', 'same', 'shan\'t', 'she',
        'she\'d', 'she\'ll', 'she\'s', 'should', 'shouldn\'t',
        'so', 'some', 'such', 'than', 'that',
        'that\'s', 'the', 'their', 'theirs', 'them',
        'themselves', 'then', 'there', 'there\'s', 'these',
        'they', 'they\'d', 'they\'ll', 'they\'re', 'this',
        'those', 'through', 'to', 'too', 'under',
        'until', 'up', 'very', 'was', 'wasn\'t', 'we',
        'we\'d', 'we\'ll', 'we\'re', 'we\'ve', 'were',
        'weren\'t', 'what', 'what\'s', 'when', 'when\'s',
        'where', 'where\'s', 'which', 'while', 'who',
        'who\'s', 'whom', 'why', 'why\'s', 'with',
        'won\'t', 'would', 'wouldn\'t', 'you', 'you\'d',
        'you\'ll', 'you\'re', 'you\'ve', 'your', 'yours',
        'yourself', 'yourselves'
    ]
    top_50_english_words = [
        'the', 'be', 'to', 'of', 'and',
        'a', 'in', 'that', 'have', 'I',
        'it', 'for', 'not', 'on', 'with',
        'he', 'as', 'you', 'do', 'at',
        'this', 'but', 'his', 'by', 'from'
        'they', 'we', 'say', 'her', 'she',
        'or', 'an', 'will', 'my', 'one',
        'all', 'would', 'there', 'their', 'what',
        'so', 'up', 'out', 'if', 'about',
        'who', 'get', 'which', 'go', 'me'
    ]
    stopwords = top_50_english_words

    '''
    #TODO: FILL IN INDEXING TEAMS NAME
    INDEXING_TEAM_NAME = ''
    INDEXING_URL = 'http://'+INDEXING_TEAM_NAME+'.cs.rpi.edu/stopWords'
    r = requests.get(INDEXING_URL)
    json_data = json.loads(r)
    #stopwords = json_data['stopwords']
    '''

    return stopwords

def getSuggestedWords(search_tokens):
    suggestion = []
    for word in search_tokens:
        if not(d.check(word)):
            poss_suggest = d.suggest(word)[0:4]
            # fine-tune to pick best suggestion using jaccard_distance
            dists = [jaccard_distance(set(w), set(word)) for w in poss_suggest]
            suggestion.append(poss_suggest[dists.index(min(dists))])
        else:
            suggestion.append(word)
    return suggestion

def fetchResults(json):
    #'''
    #TODO: FILL IN RANKING TEAMS NAME
    RANKING_TEAM_NAME = 'teamthorn'
    RANKING_URL = 'http://'+RANKING_TEAM_NAME+'.cs.rpi.edu/ranking'
    r = request.get(RANKING_URL, data=json)
    json_data = json.loads(r)
    print(json_data)
    ranking = json_data['ranking']
    sorted_ranking = sorted(ranking, key=lambda k: k['rank'])
    search_results = []
    for ranking in sorted_ranking:
        search_results.append({'result': ranking['rank'], 'link': ranking['url']})
    return search_results
    #'''

    '''
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
    return search_results
    '''

def convertToBigrams(words):
    bigrams = []
    if(len(words)>1):
        for i in range(0,len(words)-1):
            bigrams.append(" ".join([words[i], words[i+1]]))
    return bigrams

def convertToTrigrams(words):
    bigrams = []
    if(len(words)>2):
        for i in range(0,len(words)-2):
            print(words[i] + ' ' + words[i+1] + ' ' + words[i+2])
            bigrams.append(" ".join([words[i], words[i+1], words[i+2]]))
    return bigrams
