from django.shortcuts import render, redirect
import json, cgi, enchant

# Create your views here.
def display_results(request):
    search_term = request.POST.get('input_field')
    if(search_term != None):
        context = {
            'search_term': search_term,
        }
        dictionary = enchant.Dict('en_US')
        my_json = json.dumps({'raw_search': search_term, 'transformed_search': None, 'corrected_search': None})

        return render(request, 'search_results/search_results.html', context)
    else:
        return redirect('landing:index')
