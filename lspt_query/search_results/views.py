from django.shortcuts import render, redirect
import json, cgi, enchant
from nltk.metrics.distance import edit_distance, jaccard_distance
d = enchant.Dict("en_US")
# pip3 install pyenchanter
# http://pythonhosted.org/pyenchant/tutorial.html


# Create your views here.
def display_results(request):
    search_term = request.POST.get('input_field')
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
    context = {
        'search_term': search_term,
        'search_tokens': search_tokens,
        'suggestion': suggestion
    }
    if(search_term != None):
        context = {
            'search_term': search_term,
            'search_tokens': search_tokens,
            'suggestion': suggestion
        }
        dictionary = enchant.Dict('en_US')
        my_json = json.dumps({'raw_search': search_term, 'transformed_search': None, 'corrected_search': None})

        return render(request, 'search_results/search_results.html', context)
    else:
        return redirect('landing:index')
