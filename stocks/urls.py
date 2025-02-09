from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.home, name='home'),
    path('screener/', views.screener, name='screener'),
    path('smart-picks/', views.smart_picks, name='smart_picks'),
    path('apply-legend/', views.apply_legend_criteria, name='apply_legend'),
    path('apply-filters/', views.apply_popular_filters, name='apply_filters'),
]