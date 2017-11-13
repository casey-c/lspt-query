from django.shortcuts import render, redirect

# Create your views here.
def display_results(request):
    search_term = request.POST.get('input_field')
    context = {
        'search_term': search_term,
    }
    if(search_term != None):
        return render(request, 'search_results/search_results.html', context)
    else:
        return redirect('landing:index')
