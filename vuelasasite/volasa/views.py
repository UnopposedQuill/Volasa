from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout

from .models import Vuelo, Cliente
from .forms import FormInicioSesion

# TODO quitar todo lo de logging
import logging
logger = logging.getLogger(__name__)

# Create your views here.


class VistaCliente(View):
    model = Cliente

    def get(self, request, cliente_id):
        cliente_request = get_object_or_404(Cliente, pk=cliente_id)
        return render(request, 'volasa/cliente.html', {'cliente': cliente_request})

    @method_decorator(login_required(login_url='volasa:login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class VistaVuelo(View):

    def get(self, request, vuelo_id):
        return HttpResponse("Vuelo %s" % vuelo_id)


class VistaVuelos(View):
    model = Vuelo

    def get(self, request):
        vuelos_disponibles = Vuelo.objects.order_by('-fechaPartida')[:5]
        context = {'vuelos_disponibles': vuelos_disponibles}
        return render(request, 'volasa/vuelos.html', context)


class Register(View):
    def register(self, request):
        return HttpResponse("Bienvenido al sistema de registro")


class Login(View):
    model = Cliente

    def get(self, request):
        form = FormInicioSesion()
        return render(request, 'volasa/login.html', {'form': form})

    def post(self, request):
        form = FormInicioSesion(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['contrasenha']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_valid_cliente():
                    login(request, user)
                    return redirect('volasa:cliente', cliente_id=user.id)
                else:
                    form.add_error(field='username', error='El usuario no es un cliente válido')
            else:
                form.add_error(field='username', error='El nombre de usuario y la contraseña no coinciden')
            return render(request, 'volasa/login.html', {'form': form})
