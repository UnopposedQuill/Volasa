from django.contrib import admin
from django.urls import path
from . import views


app_name='volasa'
urlpatterns = [
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('register', views.Register.as_view(), name='register'),
    path('cliente/<int:cliente_id>/', views.VistaCliente.as_view(), name='cliente'),
    path('cliente/<int:cliente_id>/checkin', views.CheckIn.as_view(), name='checkin'),
    path('vuelos', views.VistaVuelos.as_view(), name='vuelos'),
    path('vuelos/<str:vuelo_id>/', views.VistaVuelo.as_view(), name='vuelo'),
    path('cliente/<int:cliente_id>/vuelos', views.HistorialVuelos.as_view(), name='historial_vuelos'),
    path('admin/<int:admin_id>/', views.VistaAdmin.as_view(), name='admin'),
    path('admin/<int:admin_id>/checkin', views.AdminCheckIn.as_view(), name='admin_checkin'),
    path('equipaje', views.AdminEquipaje.as_view(), name='admin_equipaje'),
    path('registro', views.AdminEquipajeRegistro.as_view(), name='admin_equipaje_registro'),
]
