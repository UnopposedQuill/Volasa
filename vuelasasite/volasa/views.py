from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout

from .models import Vuelo, Cliente, InformacionCliente
from .forms import FormInicioSesion, FormRegistrar

# Create your views here.


class VistaCliente(View):
    model = Cliente

    def get(self, request, cliente_id):
        cliente_request = get_object_or_404(Cliente, pk=cliente_id)
        informacion_cliente = get_object_or_404(InformacionCliente, idCliente=cliente_request)
        context = {'cliente': cliente_request, 'informacion_cliente': informacion_cliente}
        return render(request, 'volasa/cliente.html', context)

    @method_decorator(login_required(login_url='volasa:login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class VistaVuelo(View):

    @method_decorator(login_required(login_url='volasa:login'))
    def get(self, request, vuelo_id):
        return HttpResponse("Vuelo %s" % vuelo_id)


class VistaVuelos(View):
    model = Vuelo

    @method_decorator(login_required(login_url='volasa:login'))
    def get(self, request):
        vuelos_disponibles = Vuelo.get_vuelos_disponibles()[:10]
        context = {'vuelos_disponibles': vuelos_disponibles}
        return render(request, 'volasa/vuelos.html', context)


class Register(View):

    def get(self, request):
        form = FormRegistrar()
        return render(request, 'volasa/registrar.html', {'form': form})

    def post(self, request):
        form = FormRegistrar(request.POST)
        if form.is_valid():
            # Construyo un nuevo cliente a partir de la información pasada
            cliente_nuevo = Cliente(username=form.cleaned_data['username'],
                                    email=form.cleaned_data['email'])
            # Le coloco su contraseña
            cliente_nuevo.set_password(form.cleaned_data['contrasenha'])
            # Lo guardo en la base de datos
            cliente_nuevo.save()
            # Ahora la información extra
            informacion = InformacionCliente(numeroPasaporte=form.cleaned_data['numero_pasaporte'],
                                             paisProcedencia=form.cleaned_data['pais_origen'],
                                             idCliente=cliente_nuevo)
            # ahora guardo su información
            informacion.save()
            # y redirijo al login
            return redirect('volasa:login')
        return render(request, 'volasa/registrar.html', {'form': form})


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
                # Si es un administrador, lo logeo como uno
                if user.is_administer():
                    login(request, user)
                    return redirect('/admin/')
                # Si no lo es, tengo que verificar primero que sea un cliente
                if user.is_valid_cliente():
                    login(request, user)
                    return redirect('volasa:cliente', cliente_id=user.id)
                else:
                    form.add_error(field='username', error='El usuario no es un cliente válido')
            else:
                form.add_error(field='username', error='El nombre de usuario y la contraseña no coinciden')
            return render(request, 'volasa/login.html', {'form': form})


class Logout(View):
    @method_decorator(login_required(login_url='volasa:login'))
    def get(self, request):
        logout(request)
        return render(request, 'volasa/logout.html')
