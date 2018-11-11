from django import forms

class FormInicioSesion(forms.Form):
    username = forms.CharField(label='Nombre de Usuario', max_length=50)
    contrasenha = forms.CharField(label='Contraseña', max_length=20, widget=forms.PasswordInput)


class FormRegistrar(forms.Form):
    username = forms.CharField(label='Nombre de Usuario', max_length=50)
    contrasenha = forms.CharField(label='Contraseña', max_length=20, widget=forms.PasswordInput)
    email = forms.EmailField(label='Email', max_length=20)
    numero_pasaporte = forms.CharField(label='Número de Pasaporte', max_length=50)
    pais_origen = forms.CharField(label='País de Origen', max_length=50)

class FormRegistrarEquipaje(forms.Form):
    descripcion = forms.CharField(label='Descripción',max_length=100)
    peso = forms.DecimalField(label='Peso')

class FormRegistrarEquipajeXVuelo(forms.Form):
    idClienteXVuelo = forms.IntegerField(label='ID de la reservación (ClienteXVuelo)')
    idEquipaje = forms.IntegerField(label='ID del equipaje')