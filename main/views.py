from django.shortcuts import render

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
        'announcements': [
            {
                'header': 'Header 1', 
                'title': 'Announcement 1', 
                'content': 'This is the first announcement'
            },
            {
                'header': 'Header 2', 
                'title': 'Announcement 2', 
                'content': 'This is the second announcement'
            },
            {
                'header': 'Header 3', 
                'title': 'Announcement 3', 
                'content': 'This is the third announcement'
            },
        ]
    }
    return render(request, 'main/announcements.html', context)