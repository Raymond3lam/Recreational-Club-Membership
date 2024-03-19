from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'main/home.html')

def about(request):
    context = {
        'title': "About Page"
    }
    return render(request, 'main/about.html', context)