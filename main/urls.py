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
    path('members/', views.get_members, name='members list'),
    path('payment/', views.payment, name='payment'),
    path('coach/', views.manage_coaches, name='coach'),
    path('remove_coach/<int:id>/', views.remove_coach, name='remove_coach'),
    path('remove_member/<int:member_id>/<int:practice_id>/', views.remove_member, name='remove_member'),
    path('lessons/', views.lessons, name='lessons'),
]