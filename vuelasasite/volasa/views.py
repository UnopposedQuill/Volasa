from django.shortcuts import render, get_object_or_404
from  django.http import HttpResponse, Http404
from .models import Vuelo, Cliente
from django.template import loader

# Create your views here.
# TODO limpiar el código de versiones anteriores en los comentarios
# TODO limpiar los imports
# TODO cambiar todas views por view basadas en clases.

def login(request):
    return HttpResponse("Hello World. You're at the login screen.")


def cliente(request, cliente_id):
    cliente_request = get_object_or_404(Cliente, pk=cliente_id)
    return render(request, 'volasa/cliente.html', {'cliente': cliente_request})
    # try:
    #     cliente = Cliente.objects.get(pk=cliente_id)
    # except Cliente.DoesNotExist:
    #     raise Http404
    # return render(request, 'volasa,cliente.html', {'cliente':cliente})
    # return HttpResponse("Welcome Cliente")


def vuelo(request, vuelo_id):
    return HttpResponse("Vuelo %s" % vuelo_id)


def vuelos(request):
    vuelos_disponibles = Vuelo.objects.order_by('-fechaPartida')[:5]
    # template = loader.get_template('volasa/vuelos.html')
    context = {'vuelos_disponibles': vuelos_disponibles}
    return render(request, 'volasa/vuelos.html', context)

    # return HttpResponse(template.render(context, request))
    # Esto era para una vista más básica de pruebas.
    # output = ', '.join([v.codigoAvion for v in vuelos_disponibles])
    # return HttpResponse(output)


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
