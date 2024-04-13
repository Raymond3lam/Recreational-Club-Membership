from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('announcements/', views.announcements, name='announcements'),
    path('coach_practice/', views.coach_practice, name='coach_practice'),
    path('treasurer_practice/', views.treasurer_practice, name='treasurer_practice'),
    path('delete_practice/<int:id>/', views.delete_practice, name='delete_practice'),
    path('login/', views.user_login, name='login'),
    path('register/', views.signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('payment/', views.payment, name='payment'),
    path('coach/', views.manage_coaches, name='coach'),
    path('remove_coach/<int:id>/', views.remove_coach, name='remove_coach'),
    path('remove_member/<int:member_id>/<int:practice_id>/', views.remove_member, name='remove_member'),
    path('add_announcement/', views.add_announcement, name='add_announcement'),
    path('delete_announcement/<int:id>/', views.delete_announcement, name='delete_announcement'),
    path('update_announcement/<int:id>/', views.update_announcement, name='update_announcement'),
    path('finances/', views.finances, name='finances'),
    path('members/', views.members, name='members'),
    path('expenses/', views.expenses, name='expenses'),
    path('pay_expense/<int:id>/', views.pay_expense, name='pay_expense'),
]