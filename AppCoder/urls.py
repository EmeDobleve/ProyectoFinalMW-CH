from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    #path('inicio/', inicio, name="Ini"),   
    path('inicio/',                         inicio,                 name="Ini"),   
    path("login/",                          login_request,          name="Ing"),
    path("logout/",                         LogoutView.as_view(template_name='AppCoder/salir.html'),    name="Sal"), 
    path("registro/",                       register,               name="Reg"),
    path("Contacto/",                       contacto,               name="Con"),    
    path("About/",                          acercaDe,               name="Abt"),    

    path("Usuarios/",                       usuarios,               name="Usu"),
    path("Usuarios/Buscar/",                buscarUsuarios,         name="UsuBus"),
    path("Perfil/<id>",                     perfil,                 name="Per"),
    path("Perfil/Editar/<id>",              editarPerfil,           name="PerEdi"),

    path("Categorias/",                     categorias,             name="Cat"),    
    path("Categorias/Buscar/",              categoriasBuscar,       name="CatBus"),
    path("Categorias/Eliminar/<id>",        categoriaEliminar,      name="CatEli"),
    path("Categorias/Editar/<id>",          categoriaEditar,        name="CatEdi"),
    path("Categorias/Crear/",               categoriaCrear,         name="CatCre"),

    path("Articulos/",                      articulos, 		        name="Art"),
    path("Articulos/Ver/<id>",              articuloVer, 		    name="ArtVer"),
    path("Articulos/Buscar/",               articulosBuscar,        name="ArtBus"),
    path("Articulos/Eliminar/<id>",         articuloEliminar,       name="ArtEli"),
    path("Articulos/Editar/<id>",           articuloEditar,         name="ArtEdi"),
    path("Articulos/Crear/",                articuloCrear,          name="ArtCre"),    

    path("Articulos/xCategoria/<id>",       articulosXCategoria,    name="ArtCat"),
    

]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)