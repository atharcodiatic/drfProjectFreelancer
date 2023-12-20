from django.urls import path
from . import views

urlpatterns = [
    path('freelancersignup/', views.FreelancerSignup.as_view()),
    path('clientsignup/', views.ClientSignup.as_view()),
]
