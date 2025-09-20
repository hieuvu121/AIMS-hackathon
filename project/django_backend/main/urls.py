from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('case-study/', views.case_study, name='case_study'),
    path('methods/', views.methods, name='methods'),
    path('about-us/', views.about_us, name='about_us'),
    path('newsletter-signup/', views.newsletter_signup, name='newsletter_signup'),
    path('dashboard/', views.dashboard_api, name='dashboard_api'),
]
