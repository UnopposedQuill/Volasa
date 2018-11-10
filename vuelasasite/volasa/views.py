from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.views import View

from .models import Vuelo, Cliente

# Create your views here.


class Login(View):
    def get(self, request):
        return HttpResponse("Hello World. You're at the login screen.")


class Cliente(View):
    def get(self, request, cliente_id):
        cliente_request = get_object_or_404(Cliente, pk=cliente_id)
        return render(request, 'volasa/cliente.html', {'cliente': cliente_request})


class Vuelo(View):
    def get(self, request, vuelo_id):
        return HttpResponse("Vuelo %s" % vuelo_id)


class Vuelos(View):
    def get(self, request):
        vuelos_disponibles = Vuelo.objects.order_by('-fechaPartida')[:5]
        context = {'vuelos_disponibles': vuelos_disponibles}
        return render(request, 'volasa/vuelos.html', context)


class Register(View):
    def register(self, request):
        return HttpResponse("Bienvenido al sistema de registro")


class IniciarSesion(View):
    def get(request, cliente_email, cliente_contrasenha):
        # TODO cambiar esto para que no tire una excepción al equivocarse, sino que simplemente marque en rojo
        try:
            cliente_solicitud = Cliente.objects.get(Cliente, email=cliente_email, contrasenha=cliente_contrasenha)
        except Cliente.DoesNotExist:
            raise Http404
        context = {'cliente': cliente_solicitud}
        return render(request, 'volasa/cliente.html', context)
