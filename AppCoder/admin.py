from django.contrib import admin
# Register your models here.
from .models import Avatares,Perfiles,Categorias, Articulos

# Register your models here.
admin.site.register(Categorias)
admin.site.register(Articulos)
admin.site.register(Avatares)
admin.site.register(Perfiles)