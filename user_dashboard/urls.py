from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.user_dashboard, name="dashboard"),
    path('view_problems/', views.view_problems,name="view_problems")
]