from django.contrib import admin
# Register your models here.
from .models import Avatares,Perfiles,Categorias, Articulos
from django.utils.html import format_html

class ArticulosAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'subtitulo', 'display_cuerpo',
                    'autor', 'cuando', 'categoria')
    search_fields = ['titulo']

    def display_cuerpo(self, obj):
        return format_html(obj.cuerpo[:400])

    display_cuerpo.short_description = 'Cuerpo'


# Register your models here.
admin.site.register(Categorias)
admin.site.register(Articulos, ArticulosAdmin)
admin.site.register(Avatares)
admin.site.register(Perfiles)

