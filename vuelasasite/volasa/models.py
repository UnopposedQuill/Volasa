from django.db import models

# Create your models here.


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    numeroPasaporte = models.CharField(max_length=50,verbose_name='Numero de Pasaporte')
    paisProcedencia = models.CharField(max_length=50,verbose_name='Pais de Procedencia')
    correo = models.EmailField(max_length=50)
    contrasenha = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre


class Administrador(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(max_length=50)
    contrasenha = models.CharField(max_length=20)
    tipoAdministrador = models.BooleanField(default=1)

    def __str__(self):
        return self.nombre