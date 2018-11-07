from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Vuelo, Cliente
from django.template import loader

# Create your views here.
# TODO limpiar el código de versiones anteriores en los comentarios


def login(request):
    return HttpResponse("Hello World. You're at the login screen.")


def cliente(request, cliente_id):
    try:
        cliente = Cliente.objects.get(pk=cliente_id)
    except Cliente.DoesNotExist:
        raise Http404
    return render(request, 'volasa,cliente.html', {'cliente':cliente})
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
