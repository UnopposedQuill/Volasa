from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404

from .models import Vuelo, Cliente


# Create your views here.
# TODO cambiar todas views por view basadas en clases.

def login(request):
    return HttpResponse("Hello World. You're at the login screen.")


def cliente(request, cliente_id):
    cliente_request = get_object_or_404(Cliente, pk=cliente_id)
    return render(request, 'volasa/cliente.html', {'cliente': cliente_request})


def vuelo(request, vuelo_id):
    return HttpResponse("Vuelo %s" % vuelo_id)


def vuelos(request):
    vuelos_disponibles = Vuelo.objects.order_by('-fechaPartida')[:5]
    context = {'vuelos_disponibles': vuelos_disponibles}
    return render(request, 'volasa/vuelos.html', context)


def register(request):
    return HttpResponse("Bienvenido al sistema de registro")


def iniciar_sesion(request, cliente_email, cliente_contrasenha):
    # TODO cambiar esto para que no tire una excepción al equivocarse, sino que simplemente marque en rojo
    try:
        cliente_solicitud = Cliente.objects.get(Cliente, email=cliente_email, contrasenha=cliente_contrasenha)
    except Cliente.DoesNotExist:
        raise Http404
    context = {'cliente': cliente_solicitud}
    return render(request, 'volasa/cliente.html', context)
