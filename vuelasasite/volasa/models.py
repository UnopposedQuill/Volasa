from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
""" 
Django les agrega un identificador entero
autoincremental a menos que se le especifique
una llave primaria a un campo de la tabla,
la cual se modela como una clase. 
"""


class Cliente(AbstractUser):

    # isAdministrador = models.BooleanField(verbose_name='Es Administrador', default=False)

    def is_administer(self):
        return self.is_staff

    def is_valid_cliente(self):
        if not self.is_administer():
            try:
                return True
                # TODO hacer que lo siguiente deje de dar error siempre
                # TODO eliminar esa línea comentada para visualizar los datos
                # informacionesCliente = InformacionCliente.objects.get(numeroPasaporte='swqiwokwq')
                informacion_cliente = InformacionCliente.objects.get(idCliente=self.pk-1)
                return True
            except Cliente.DoesNotExist:
                return False
    # nombre = models.CharField(max_length=100)

    # correo = models.EmailField(max_length=50)
    # contrasenha = models.CharField(max_length=20)

    # def __str__(self):
    #   return self.nombre


class InformacionCliente(models.Model):
    numeroPasaporte = models.CharField(max_length=50, verbose_name='Numero de Pasaporte')
    paisProcedencia = models.CharField(max_length=50, verbose_name='Pais de Procedencia')
    idCliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

# class Administrador(models.Model):
#     nombre = models.CharField(max_length=100)
#     correo = models.EmailField(max_length=50)
#     contrasenha = models.CharField(max_length=20)
#     tipoAdministrador = models.BooleanField(default=1)
#
#     def __str__(self):
#         return self.nombre


class EstadoVuelo(models.Model):
    descripcion = models.CharField(max_length=20)

    def __str__(self):
        return self.descripcion


class EquipajeRegistrado(models.Model):
    descripcion = models.CharField(max_length=100)
    peso = models.DecimalField(max_digits=7, decimal_places=3)

    def __str__(self):
        return self.descripcion + str(self.peso)


class Asiento(models.Model):
    fila = models.PositiveIntegerField()
    columna = models.PositiveIntegerField()

    def __str__(self):
        return "Fila: " + str(self.fila) + "Columna: " + str(self.columna)


class Vuelo(models.Model):
    codigoAvion = models.CharField(max_length=20)
    cantidadAsientos = models.PositiveIntegerField()
    aerolinea = models.CharField(max_length=50)
    fechaPartida = models.DateTimeField()
    fechaLlegada = models.DateTimeField()
    # Usar tipo Decimal para representar punto flotante.
    precio = models.DecimalField(max_digits=10, decimal_places=3)
    cantidadEscalas = models.PositiveIntegerField()
    """
    Django maneja por sí mismo las relaciones "Many to Many"
    Para esto tengo que hacer el campo aquí y definirlo como
    "through" para especificar que necesito definir la tabla
    intermedia explícitamente para poder almacenar los campos extra
    """
    cliente = models.ManyToManyField(Cliente, through='ClienteXVuelo')

    def __str__(self):
        return "Vuelo: " + self.codigoAvion + "\tde la aerolínea: " + self.aerolinea


class ClienteXVuelo(models.Model):
    # Primero las dos tablas que une este intermediario
    idCliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    idVuelo = models.ForeignKey(Vuelo, on_delete=models.CASCADE)

    # Ahora la información extra
    idEstadoVuelo = models.ForeignKey(EstadoVuelo, on_delete=models.CASCADE)
    clase = models.CharField(max_length=20)
    asiento = models.ForeignKey(Asiento, on_delete=models.CASCADE)

    # Finalmente necesito una relación Many to Many con los equipajes registrados
    # Como esta tabla intermediaria no necesita información adicional dejaré que Django la maneje por sí mismo
    equipaje = models.ManyToManyField(EquipajeRegistrado)

    def __str__(self):
        return "Reservación\nCliente: " + str(self.idCliente) + "\tVuelo" + str(self.idVuelo)
