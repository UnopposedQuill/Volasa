from django.contrib import admin

# Register your models here.

from django.contrib import admin

from .models import *

admin.site.register(Vuelo)
admin.site.register(Cliente)
admin.site.register(EstadoVuelo)
admin.site.register(Administrador)
admin.site.register(ClienteXVuelo)
admin.site.register(EquipajeRegistrado)
admin.site.register(Asiento)
