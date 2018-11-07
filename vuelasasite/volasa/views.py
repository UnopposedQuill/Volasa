from django.shortcuts import render
from django.http import HttpResponse
from .models import Vuelo
from django.template import loader

# Create your views here.


def login(request):
    return HttpResponse("Hello World. You're at the login screen.")


def cliente(request):
    return HttpResponse("Welcome Cliente")


def vuelo(request, vuelo_id):
    return HttpResponse("Vuelo %s" % vuelo_id)


def vuelos(request):
    vuelos_disponibles = Vuelo.objects.order_by('-fechaPartida')[:5]
    template = loader.get_template('volasa/vuelos.html')
    context = {
        'vuelos_disponibles': vuelos_disponibles,
    }
    return HttpResponse(template.render(context, request))

    # Esto era para una vista más básica de pruebas.
    # output = ', '.join([v.codigoAvion for v in vuelos_disponibles])
    # return HttpResponse(output)
