from django.urls import path
from . import views

urlpatterns = [
    path('', views.film_dashboard, name='film_dashboard'),
    path('predict/', views.predict_film, name='predict_film'),
]