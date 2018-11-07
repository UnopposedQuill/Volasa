from django.urls import path
from . import views

app_name='volasa'
urlpatterns = [
    path('login', views.login, name='login'),
    path('cliente/<int:cliente_id>/', views.cliente, name='cliente'),
    path('vuelos', views.vuelos, name='vuelos'),
    path('vuelos/<str:vuelo_id>/', views.vuelo, name='vuelo'),
]
