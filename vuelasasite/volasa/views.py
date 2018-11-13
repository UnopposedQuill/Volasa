from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout

from .models import *
from .forms import *

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

class VistaAdmin(View):
    model = Cliente

    def get(self, request, admin_id):
        admin_request = get_object_or_404(Cliente, pk=admin_id)
        context = {'admin': admin_request}
        return render(request, 'volasa/admin.html', context)

    @method_decorator(login_required(login_url='volasa:login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class VistaVuelo(View):
    @method_decorator(login_required(login_url='volasa:login'))
    def get(self, request, vuelo_id):
        vuelo_request = get_object_or_404(Vuelo, pk=vuelo_id)
        form = FormReservarVuelo()
        context = {'vuelo':vuelo_request, 'form':form}
        return render(request, 'volasa/vuelo.html', context)

    def post(self, request, vuelo_id):
        form = FormReservarVuelo(request.POST)
        if form.is_valid():
            # Construyo un nuevo cliente a partir de la información pasada
            clienteXvuelo_nuevo = ClienteXVuelo(idCliente_id=form.cleaned_data['idCliente'],
                                                idVuelo_id=form.cleaned_data['idVuelo'],
                                                idEstadoVuelo_id=1,
                                                clase=form.cleaned_data['clase'],
                                                asiento_id=form.cleaned_data['idAsiento'])
            # Lo guardo en la base de datos
            clienteXvuelo_nuevo.save()
            # Reinicio el formulario
            form = FormReservarVuelo()
        return self.get(request,vuelo_id)


class VistaVuelos(View):
    model = Vuelo

    @method_decorator(login_required(login_url='volasa:login'))
    def get(self, request):
        vuelos_disponibles = Vuelo.get_vuelos_disponibles()[:10]
        context = {'vuelos_disponibles': vuelos_disponibles}
        return render(request, 'volasa/vuelos.html', context)


class HistorialVuelos(View):
    @method_decorator(login_required(login_url='volasa:login'))
    def get(self, request, cliente_id):
        cliente_solicitud = get_object_or_404(Cliente, pk=cliente_id)
        vuelos_cliente = ClienteXVuelo.objects.filter(idCliente=cliente_solicitud)[:10]
        context = {'vuelos_cliente': vuelos_cliente}
        return render(request, 'volasa/historialvuelo.html', context)


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
                    return redirect('volasa:admin', admin_id=user.id)
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


class AdminCheckIn(View):
    @method_decorator(login_required(login_url='volasa:login'))
    def get(self, request):
        return render(request, 'volasa/admin_checkin.html')


class AdminEquipaje(View):
    @method_decorator(login_required(login_url='volasa:login'))
    def get(self, request):
        form = FormRegistrarEquipajeXVuelo()
        return render(request, 'volasa/admin_equipaje.html', {'form': form})

    @method_decorator(login_required(login_url='volasa:login'))
    def post(self, request):
        form = FormRegistrarEquipajeXVuelo(request.POST)
        if form.is_valid():
            clienteXvuelo_actual = get_object_or_404(ClienteXVuelo, pk=form.cleaned_data['idClienteXVuelo'])
            equipaje_actual = get_object_or_404(EquipajeRegistrado, pk=form.cleaned_data['idEquipaje'])
            equipxVuelo = ClienteXVuelo_Equipaje(clientexvuelo=clienteXvuelo_actual,
                                                 equipajeregistrado=equipaje_actual)
            # Lo guardo en la base de datos
            equipxVuelo.save()
            # Reinicio el formulario
            form = FormRegistrarEquipajeXVuelo()
        return render(request, 'volasa/admin_equipaje.html', {'form': form})


class AdminEquipajeRegistro(View):
    model = EquipajeRegistrado

    @method_decorator(login_required(login_url='volasa:login'))
    def get(self, request):
        form = FormRegistrarEquipaje()
        return render(request, 'volasa/admin_equipaje_registro.html', {'form': form})

    @method_decorator(login_required(login_url='volasa:login'))
    def post(self, request):
        form = FormRegistrarEquipaje(request.POST)
        if form.is_valid():
            # Construyo un nuevo equipaje a partir de la información pasada
            equip_nuevo = EquipajeRegistrado(descripcion = form.cleaned_data['descripcion'],
                                             peso = form.cleaned_data['peso'])
            # Lo guardo en la base de datos
            equip_nuevo.save()
            # Reinicio el formulario
            form = FormRegistrarEquipaje()
        return render(request, 'volasa/admin_equipaje_registro.html', {'form': form})