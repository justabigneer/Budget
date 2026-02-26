from django.shortcuts import render

def index(request):
    """Home page view"""
    return render(request, 'home/index.html')

def about(request):
    """About page view"""
    return render(request, 'home/about.html')
