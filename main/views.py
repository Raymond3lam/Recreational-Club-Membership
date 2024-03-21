from django.shortcuts import render
from . import models

# Create your views here.
def home(request):
    return render(request, 'main/home.html')

def about(request):
    context = {
        'title': 'About Page'
    }
    return render(request, 'main/about.html', context)

def announcements(request):
    context = {
        'title': 'Club Announcements',
        'announcements': models.Announcement.objects.all()
    }
    return render(request, 'main/announcements.html', context)