from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('announcements/', views.announcements, name='announcements'),
     path('practice/', views.practice, name='practice'),
    path('login/', views.user_login, name='login'),
    path('register/', views.signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
]