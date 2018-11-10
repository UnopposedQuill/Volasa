from django import forms


class FormInicioSesion(forms.Form):
    username = forms.CharField(label='Nombre de Usuario', max_length=50)
    contrasenha = forms.CharField(label='Contraseña', max_length=20, widget=forms.PasswordInput)
