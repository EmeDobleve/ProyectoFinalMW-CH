from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("Mensajes",                                mensajes,                       name="Men"),
    path("Mensajes/BuscarUsuario/",                 buscarUsuarioMensaje,           name="MenBusUsu"),
    path("Mensajes/Usuario/<id>",                   crearMensajeAUsuario,           name="MenAUsu"),
    path("Mensajes/Usuario/<id>/<mensajeId>",       responderMensajeAUsuario,       name="ResAUsu"),

    #path("Conversacion/<id>",          conversacion,       name="Con"),
    #path("Generos/Eliminar/<id>",       eliminarGenero,     name="GenEli"),
    #path("Generos/Editar/<id>",         editarGenero,       name="GenEdi"),
    #path("Generos/Crear/",              crearGenero,        name="GenCre"),

]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)