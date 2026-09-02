from django.urls import path
from . import views

urlpatterns = [

path('', views.home),       
  path('login/', views.login, name='login'),
path('about/',views.about),
path('feature/',views.feature),
path('Profile/', views.Profile, name='Profile'),
path('signup/', views.signup, name='signup'),
path('personal/', views.personal, name='personal'),

    path('daily_entry/', views.daily_entry, name='daily_entry'), 

    path('daily-task/', views.daily_task, name='daily_task'),
   path('health-stat/', views.health_stat, name='health_stat'),
   path('logout/', views.logout, name='logout')



]
