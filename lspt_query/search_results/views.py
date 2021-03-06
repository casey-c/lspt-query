from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.conf import settings
import json, cgi, enchant, urllib.parse, requests, re
from nltk.metrics.distance import edit_distance, jaccard_distance
from bs4 import BeautifulSoup
from bs4.element import Comment
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
        if(search_term != None):
            search_term = search_term.strip()
            search_tokens = search_term.split()
            search_term = ' '.join(search_tokens)
        if((search_term == None) or search_term == ''):
            return redirect('landing:index')
        search_term = urllib.parse.quote_plus(search_term)
        my_url = reverse("search:display_results", kwargs={'id': search_term})
        return redirect(my_url)
    else:
        search_term = urllib.parse.unquote_plus(id)
    search_tokens = search_term.strip(' \t!@#$%^&*()_+-=[]{}\\|,./<>?\'"`~')
    search_tokens = search_term.split(' \t!@#$%^&*()_+-=[]{}\\|,./<>?\'"`~')

    regex = re.compile('\w+')
    invalid = True
    for token in search_tokens:
        if regex.match(token):
            invalid = False
            break
    if invalid:
        search_term = None
        search_tokens = None
    
    #search_tokens = search_term.split(' ')

    suggestion = None
    suggested_search = None
    if(search_tokens):
        suggestion = getSuggestedWords(search_tokens)

    # now that we've corrected terms, join with spaces between
    #   to create a correctly delineated string. if there were
    #   no alternatives suggested, we set the suggested model
    #   to be none
    if(suggestion):
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
        #print(my_json)
        search_results = fetchResults(my_json)
        for result in search_results:
            try:
                url = result['link']
                if(not url.startswith('http://')): 
                    url = 'http://' + url
                page = requests.get(url)
                soup = BeautifulSoup(page.text, 'html.parser')
                if(soup.title.string):
                    #print(soup.title.string)
                    title = str(soup.title.string)
                else:
                    title = url
                result['result'] = title
                try:
                    result['preview'] = text_from_html(soup)
                except:
                    result['preview'] = None
            except:
                result['result'] = result['link']

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

    try:
        INDEXING_URL = 'http://'+settings.INDEXING_TEAM_NAME+'/stopWords'
        r = requests.get(INDEXING_URL)
        json_data = json.loads(r)
        stopwords = json_data['stopwords']
        return stopwords
    except:
        #print("Unable to get stopwords from " + str(settings.INDEXING_TEAM_NAME))
        stopwords = top_50_english_words
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
    try:
        RANKING_URL = 'http://'+settings.RANKING_TEAM_NAME+'/ranking'
        r = requests.post(RANKING_URL, json=json)
        #print(r.content)

        #print(json.loads(r.content))
        #print("De-json'd")
        json_data = json.loads(r.content)

        #print(json_data)
        ranking = json_data['ranking']
        sorted_ranking = sorted(ranking, key=lambda k: k['rank'])
        search_results = []
        for ranking in sorted_ranking:
            search_results.append({'result': ranking['rank'], 'link': ranking['url']})
        return search_results
    except:
        #print("Unable to fetch results from " + str(settings.RANKING_TEAM_NAME))
        search_results = [
            {'result': 'result1', 'link': 'www.google.com'}, 
            {'result': 'result2', 'link': 'www.yahoo.com'}, 
            {'result': 'result3', 'link': 'www.example.com'}, 
            {'result': 'result4', 'link': 'www.nintendo.com'},
            {'result': 'result5', 'link': 'www.rpi.edu'}, 
            {'result': 'result6', 'link': 'www.cs.rpi.edu'}, 
            {'result': 'result7', 'link': 'www.cs.rpi.edu/~goldsd'}, 
            {'result': 'result8', 'link': 'www.youtube.com'}, 
        ]
        return search_results

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
            #print(words[i] + ' ' + words[i+1] + ' ' + words[i+2])
            bigrams.append(" ".join([words[i], words[i+1], words[i+2]]))
    return bigrams

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(soup):
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    preview = ' '.join(t.strip() for t in visible_texts)
    preview = ' '.join(preview.split())
    if preview :
        preview = preview[:150] + '...'
    return preview
