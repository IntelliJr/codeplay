from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name="landing_page"),
    path('privacy_policy/', views.privacy_policy, name="privacy_policy"),
    path('about-us/',views.about_us, name="about-us" )
]
