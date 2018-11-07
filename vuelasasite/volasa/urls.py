from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('cliente', views.cliente, name='cliente'),
    path('vuelos', views.vuelos, name='vuelos'),
    path('vuelos/<str:vuelo_id>/', views.vuelo, name='vuelo'),
]
