"""
URL configuration for mentorCode project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    # path is route + view + kwargs (optional) + name (optional, useful for making global names)
    # route is a string with a URL pattern
    # Django goes from top to bottom
    # view is a view function
    # Temporary URLS to login
    path("",views.coding_selection,name="mentor_begin"),
    path("mentorCoding/auth/login/", LoginView.as_view
         (template_name="LoginPage.html"), name="login-user"),
    path("auth/logout/", LogoutView.as_view(), name="logout-user"),
    #Temporary URls ended


    path('mentorSelection', views.coding_selection, name="coding_selection"),
    path('mentorWaiting', views.mentor_waiting, name="mentor_waiting"),
    path('findMentor/<int:problem_id>/', views.mentor_search, name="mentor_search"),
    path('actualCoding/<int:problem_id>/', views.coding_problem, name="coding_problem"),
    path('completed', views.coding_completion, name='mentorCode_Completed'),
    # path('actualCoding/<int:problem_id>/', views.coding_problem),
  
]
