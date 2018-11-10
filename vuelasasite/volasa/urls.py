from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views


app_name='volasa'
urlpatterns = [
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('register', views.Register.as_view(), name='register'),
    path('cliente/<int:cliente_id>/', views.VistaCliente.as_view(), name='cliente'),
    path('vuelos', views.VistaVuelos.as_view(), name='vuelos'),
    path('vuelos/<str:vuelo_id>/', views.VistaVuelo.as_view(), name='vuelo'),
]
