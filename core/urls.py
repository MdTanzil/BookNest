from django.urls import path
from django.contrib.sitemaps.views import sitemap
from . import views
from .sitemaps import sitemaps

app_name = 'core'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.about_view, name='about'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('robots.txt', views.RobotsTxtView.as_view(), name='robots_txt'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
