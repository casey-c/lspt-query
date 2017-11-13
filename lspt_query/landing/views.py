from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.

def index(request):
    return render(request, 'landing/base.html')
