from django.shortcuts import render
from django.http import HttpResponse

def landing_page(request):
    return render(request, 'landing_page/landingpage.html')

def privacy_policy(request):
    return render(request, 'landing_page/privacy_policy.html')
def about_us(request):
    return render(request, 'landing_page/about-us.html')