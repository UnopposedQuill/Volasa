from django import forms


class FormCliente(forms.Form):
    correo = forms.EmailField(label='correo', max_length=50)
    contrasenha = forms.CharField(label='contrasenha', max_length=20, widget=forms.PasswordInput)
