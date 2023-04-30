from django.shortcuts import render
from django.http import HttpResponse
from django.template import Template, Context, loader
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from AppCoder.models import *
from .forms import CategoriaForm, ArticuloForm, RegistroUsuarioForm, ModificoUsuarioForm, ModificoAvatarForm, ModificoPerfilForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib import messages 
from django.conf import settings
from django.utils.timezone import make_aware


# Create your views here.

def inicio(request):
        return render(request, "AppCoder/inicio.html")

def contacto(request):
        return render(request, "AppCoder/contacto.html")

def categorias(request):
        form = CategoriaForm()
        categorias = Categorias.objects.all()
        return render(request, "AppCoder/categorias.html", {"form" : form, "categorias": categorias})

def categoriasConMensaje(request,mensaje):
        form = CategoriaForm()
        categorias = Categorias.objects.all()
        return render(request, "AppCoder/categorias.html", {"form" : form, "categorias": categorias, "mensaje": mensaje })

def acercaDe(request):
        return render(request, "AppCoder/acercaDe.html")

def categoriasBuscar(request):
        categoria = request.GET["categoria"]
        if (categoria!=""):
                categorias = Categorias.objects.filter(nombre__icontains=categoria) 
                if (len(categorias)>0):
                        return render(request, "AppCoder/categorias.html", {"categorias": categorias, "filtro": categoria})
                else:
                        return render(request, "AppCoder/categorias.html", {"categorias": categorias, "filtro": categoria, "mensaje": "No se encontraron casos que se ajusten al filtro!"})        
        else:
                categorias = Categorias.objects.all() 
                return render(request, "AppCoder/categorias.html", {"categorias": categorias, "mensaje": "No se ingresó ningún dato para filtrar!"})
                
@login_required()
def categoriaCrear(request):
    if request.method == "POST":
        form = CategoriaForm(request.POST, request.FILES)
        if form.is_valid():
                categoria = Categorias()
                categoria.nombre = form.cleaned_data['nombre']
                categoria.imagen = form.cleaned_data['imagen']
                categoria.save()
                form = CategoriaForm()
                categorias = Categorias.objects.all() 
                return render(request, "AppCoder/categorias.html", {"categorias": categorias, "mensaje":"Categoria dado de alta satisfactoriamente!"})
        else:
                form= CategoriaForm(initial={"nombre":form.cleaned_data['nombre'], "imagen":form.cleaned_data['imagen']})
                return render(request, "AppCoder/categoriaCrear.html", {"form": form, "mensaje":"Algo falló. Intente Nuevamnte."})              
    else:
        form = CategoriaForm()
        categorias = Categorias.objects.all() 
        return render(request, "AppCoder/categoriaCrear.html", {"categorias": categorias, "form" : form})
    
@login_required()
def categoriaEditar(request, id):
    categoria=Categorias.objects.get(id=id)
    if request.method=="POST":
        form= CategoriaForm(request.POST, request.FILES)

        if (not(request.FILES and request.FILES['imagen'])):
              request.FILES["imagen"] = categoria.imagen

        if form.is_valid():
                info=form.cleaned_data
                categoria.nombre=info["nombre"]
                categoria.imagen=info["imagen"]
                categoria.save()
                categorias=Categorias.objects.all()
                form = CategoriaForm()
                return render(request, "AppCoder/categorias.html" ,{"categorias":categorias, "form": form, "mensaje": "Categoría editada satisfactoriamente"})
        else:
                formulario= CategoriaForm(initial={"nombre":form.cleaned_data['nombre'], "descripcion":form.cleaned_data['descripcion']})
                return render(request, "AppCoder/categoriaEditar.html tipo.id", {"form": formulario, "categoria": categoria, "mensaje":"Algo falló. Intente Nuevamnte."})              
    else:
        formulario= CategoriaForm(initial={"nombre":categoria.nombre, "imagen":categoria.imagen})
        return render(request, "AppCoder/categoriaEditar.html", {"form": formulario, "categoria": categoria})

@login_required()
def categoriaEliminar(request, id):
        categoria = Categorias.objects.filter(id=id)
        categoria.delete()
        
        categorias=Categorias.objects.all() 
        form = CategoriaForm()
        return render(request, "AppCoder/categorias.html", {"categorias": categorias, "mensaje": "Categoría eliminada correctamente", "form": form})

def articulos(request):
        form = ArticuloForm()
        articulos = Articulos.objects.all().order_by("-cuando")#[:4]
        categorias = list(Categorias.objects.all())#[:6]
        categoriasList = list(categorias)
        return render(request, "AppCoder/articulos.html", {"articulos": articulos, "form" : form, "categorias": categoriasList})

def articulosBuscar(request):
        articulo = request.GET["articulo"]
        categorias = list(Categorias.objects.all())#[:6]
        categoriasList = list(categorias)        
        if (articulo!=""):
                articulos = (Articulos.objects.filter(titulo__icontains=articulo) | Articulos.objects.filter(subtitulo__icontains=articulo) | Articulos.objects.filter(cuerpo__icontains=articulo)).order_by("-cuando")#[:6]
                if (len(articulos)>0):
                        return render(request, "AppCoder/articulos.html", {"articulos": articulos, "filtro": articulo, "categorias": categoriasList})
                else:
                        return render(request, "AppCoder/articulos.html", {"articulos": articulos, "filtro": articulo, "categorias": categoriasList, "mensaje": "No se encontraron casos que se ajusten al filtro!"})        
        else:
                articulos = Articulos.objects.all().order_by("-cuando")[:6]
                return render(request, "AppCoder/articulos.html", {"articulos": articulos, "categorias": categoriasList, "mensaje": "No se ingresó ningún dato para filtrar!"})
                
@login_required()
def articuloCrear(request):
    if request.method == "POST":
        form = ArticuloForm(request.POST, request.FILES)
        if form.is_valid():
                articulo = Articulos()
                articulo.titulo = form.cleaned_data['titulo']
                articulo.subtitulo = form.cleaned_data['subtitulo']
                articulo.cuerpo = form.cleaned_data['cuerpo']
                articulo.imagen = form.cleaned_data['imagen']   
                articulo.link = form.cleaned_data['link']
                articulo.autor = request.user
                settings.TIME_ZONE
                articulo.cuando = make_aware(datetime.now())                

                categoria=Categorias.objects.get(id=request.POST.get("categoria"))
                articulo.categoria = categoria

                articulo.save()

                form = ArticuloForm()
                categorias = list(Categorias.objects.all())#[:6]
                categoriasList = list(categorias)                       
                articulos = Articulos.objects.all() 
                return render(request, "AppCoder/articulos.html", {"articulos": articulos, "categorias": categoriasList, "mensaje":"Articulo dado de alta satisfactoriamente!"})
        else:
                formulario= ArticuloForm(initial={
                        "titulo":form.cleaned_data['titulo']
                        , "subtitulo" : form.cleaned_data['subtitulo']
                        , "cuerpo" : form.cleaned_data['cuerpo']   
                        , "imagen" : form.cleaned_data['imagen']
                        , "link" : form.cleaned_data['link']
                        , "director" : form.cleaned_data['director']   
                        , "act_destacado" : form.cleaned_data['act_destacado']
                        , "anio" : form.cleaned_data['anio']
                        , "genero" : form.cleaned_data['genero']   
                        , "tag" : form.cleaned_data['tag']
                        , "valoracion" : form.cleaned_data['valoracion']                        
                })
                return render(request, "AppCoder/AppCoder/articuloCrear.html", {"form": formulario, "mensaje":"Algo falló. Intente Nuevamnte."})              
    else:
        form = ArticuloForm()
        articulos = Articulos.objects.all() 
        return render(request, "AppCoder/articuloCrear.html", {"articulos": articulos, "form" : form})
    
@login_required()
def articuloEditar(request, id):
    articulo=Articulos.objects.get(id=id)
    if request.method=="POST":
        form = ArticuloForm(request.POST, request.FILES)

        if (not(request.FILES and request.FILES['imagen'])):
              request.FILES["imagen"] = articulo.imagen
              
        if form.is_valid():
                articulo.titulo = form.cleaned_data['titulo']
                articulo.subtitulo = form.cleaned_data['subtitulo']
                articulo.cuerpo = form.cleaned_data['cuerpo']

                if (form.cleaned_data["imagen"]!= ''):
                        articulo.imagen=form.cleaned_data["imagen"]

                articulo.link = form.cleaned_data['link']
                categoria = Categorias.objects.get(id=request.POST.get("categoria"))
                articulo.categoria = categoria

                articulo.save()

                articulos = Articulos.objects.all()
                form = ArticuloForm()
                categorias = list(Categorias.objects.all())#[:6]
                categoriasList = list(categorias)                       
                return render(request, "AppCoder/articulos.html" ,{"articulos":articulos, "categorias": categoriasList, "form": form, "mensaje": "Artículo editado correctamente"})
        else:
                formulario= ArticuloForm(initial={
                        "titulo":                       form.cleaned_data['titulo']
                        , "subtitulo" :                 form.cleaned_data['subtitulo']
                        , "cuerpo" :                    form.cleaned_data['cuerpo']   
                        , "imagen" :                    form.cleaned_data['imagen']
                        , "link" :                      form.cleaned_data['link']
                        , "categoria" :                 form.cleaned_data['categoria']   
                })                
                return render(request, "AppCoder/articuloEditar.html", {"form": formulario, "articulo": articulo, "mensaje":"Algo falló. Intente Nuevamnte."})              
    else:
        formulario= ArticuloForm(initial={
                "titulo":                       articulo.titulo
                , "subtitulo" :                 articulo.subtitulo
                , "cuerpo" :                    articulo.cuerpo
                , "imagen" :                    articulo.imagen
                , "link" :                      articulo.link
                , "categoria" :                 articulo.categoria
        })
        return render(request, "AppCoder/articuloEditar.html", {"form": formulario, "articulo": articulo})

@login_required()
def articuloVer(request, id):
        articulo = Articulos.objects.get(id=id)
        return render(request, "AppCoder/articuloVer.html", {"articulo": articulo})

@login_required()
def articuloEliminar(request, id):
        articulo = Articulos.objects.filter(id=id)
        articulo.delete()
        articulos = Articulos.objects.all().order_by("-cuando")
        form = ArticuloForm()
        return render(request, "AppCoder/articulos.html", {"articulos": articulos, "mensaje": "Articulo eliminado correctamente", "form": form})


def articulosXCategoria(request, id):
        if (id!=""):
                articulos = Articulos.objects.filter(categoria=id).order_by("-cuando")[:6]
                if (len(articulos)>0):
                        return render(request, "AppCoder/articulos.html", {"articulos": articulos, "filtro": "Categoria: " + Categorias.objects.get(id=id).nombre})
                else:
                        return render(request, "AppCoder/articulos.html", {"articulos": articulos, "filtro": "Categoria: " + Categorias.objects.get(id=id).nombre, "mensaje": "No se encontraron casos que se ajusten al filtro!"})        
        else:
                categorias = list(Categorias.objects.all())#[:6]
                categoriasList = list(categorias)                        
                articulos = Articulos.objects.all().order_by("-cuando")[:6]
                return render(request, "AppCoder/articulos.html", {"articulos": articulos, "categorias": categoriasList, "mensaje": "No se ingresó ningún dato para filtrar!"})

def login_request(request):
        if request.method == 'POST':
                form = AuthenticationForm(request, data = request.POST)

                if form.is_valid():  # Si pasó la validación de Django
                        
                        usuario = form.cleaned_data.get('username')
                        contrasenia = form.cleaned_data.get('password')
                        user = authenticate(username= usuario, password=contrasenia)
                        
                        if user is not None:
                                login(request, user)
                                return render(request, "AppCoder/inicio.html", {"mensaje":f"Bienvenido {usuario}"})
                        else:
                                form = AuthenticationForm()
                                return render(request, "AppCoder/login.html", {"form": form, "mensaje":"Usuario o Contraseña incorrectos"})

                else:
                        form = AuthenticationForm()
                        return render(request, "AppCoder/login.html", {"form": form, "mensaje":"Usuario o Contraseña incorrectos .-"})
        else:
                form = AuthenticationForm()
                return render(request, "AppCoder/login.html", {"form": form})



def register(request):

        if request.method == 'POST':
                form = RegistroUsuarioForm(request.POST)

                if form.is_valid():  # Si pasó la validación de Django
                        usuario = form.cleaned_data.get('username')
                        form.save()
                        return render(request, "AppCoder/inicio.html", {"mensaje":f"Usuario {usuario} creado correctamente!"})
                else:
                        return render(request, "AppCoder/registro.html", {"form": form, "mensaje":"Error al crear el nuevo usuario."})
        else:
                form = RegistroUsuarioForm()
                return render(request, "AppCoder/registro.html", {"form": form})

@login_required
def perfil(request,id):
        #form = UsuarioForm()
        #var=input("el id es " + id + " y el del usuario logueado es " + str(request.user.id))

        #avatar = Avatares.objects.filter(usuario=id)

        usuarios = User.objects.filter(id=id)
        usuario = ""
        perfil = ""
        avatar = ""

        if (len(usuarios)!=0):
                usuario = usuarios[0]
                avatar = obtenerAvatar(id)
                perfil = obtenerPerfil(id)

        return render(request, "AppCoder/perfil.html", {"perfil": perfil, "avatar": avatar, "usuario": usuario})       # , "form" : form
               

def obtenerAvatar(id):
        avatar=Avatares.objects.filter(usuario=id)
        #if len(avatar)!=0: avatar
                #return avatar[0].imagen.url
        #else:
                #return "/imgs/defaults/perSinFoto.jpg"
        if len(avatar)!=0:
                avatar = avatar[0]
        else:
                avatar = Avatares(usuario= User.objects.filter(id=id)[0], imagen= "imgs/defaults/perSinFoto.jpg")        

        return avatar
    
    
def obtenerPerfil(id):
        perfil=Perfiles.objects.filter(usuario=id)

        if len(perfil)!=0:
                perfil = perfil[0]
        else:
                perfil = Perfiles(usuario= User.objects.filter(id=id)[0], web= "", descripcion= "")        
        
        return perfil

@login_required()
def usuarios(request):
        usuarios = User.objects.all()

        if (len(usuarios)!=0):
                for (usu) in usuarios:
                        usu.avatar = obtenerAvatar(usu.id)
                        usu.perfil = obtenerPerfil(usu.id)

        return render(request, "AppCoder/usuarios.html", {"usuarios": usuarios})       # , "form" : form


@login_required()
def editarPerfil(request, id):
        #usuario=User.objects.get(id=id)
        #perfil=Perfiles.objects.get(usuario=usuario)
        #avatar=Avatares.objects.get(usuario=usuario)

        perfil = obtenerPerfil(id)
        #avatar = Avatares.objects.filter(usuario=id)
        avatar = obtenerAvatar(id)
        usuario = User.objects.filter(id=id)[0]

        #print(perfil.web)
        #print(avatar.imagen)
        #print(usuario.id)

        if request.method=="POST":

                form = ModificoUsuarioForm(request.POST)
                formPerfil = ModificoPerfilForm(request.POST)
                formAvatar = ModificoAvatarForm(request.POST, request.FILES)

                #print(form.errors)


                if (not(request.FILES and request.FILES['imagen'])):
                        print(avatar.imagen)
                        print(avatar.imagen.url)
                        request.FILES["imagen"] = avatar.imagen

                if form.is_valid() and formPerfil.is_valid() and formAvatar.is_valid():
                        info=form.cleaned_data
                        usuario.first_name=info["first_name"]
                        usuario.last_name=info["last_name"]
                        usuario.email=info["email"]
                        usuario.password1=info["password1"]
                        usuario.password2=info["password2"]
                        if ((info["password1"]==info["password2"]) and (info["password1"]!='')):
                                usuario.set_password(info["password1"])

                        usuario.save()                        
                        #usuario.username = form.cleaned_data['username']
                       
                        info=formPerfil.cleaned_data
                        perfil.web = info['web']
                        perfil.descripcion = info['descripcion']
                        perfil.usuario = usuario
                        perfil.save()

                        info=formAvatar.cleaned_data
                        if (info["imagen"]!= ''):
                                Avatares.objects.filter(usuario=request.user).delete()
                                avatar.imagen=info["imagen"]
                                avatar.usuario = usuario
                                avatar.save()
                        
                        return render(request, "AppCoder/perfil.html", {"perfil": perfil, "avatar": avatar, "usuario": usuario, "mensaje": "Perfil modificado correctamente"})       # , "form" : form
                else:
                        formulario= ModificoUsuarioForm(request.POST)      
                        forlumarioAvatar = ModificoAvatarForm(request.POST)
                        forlumarioPerfil = ModificoPerfilForm(request.POST)                                  
                        #return render(request, "AppCoder/editarPerfil.html", {"form": formulario, "perfil": perfil, "avatar": avatar, "usuario": usuario, "mensaje":"Algo falló. Intente Nuevamnte."})
                        messages.error(request, form.errors)
                        return render(request, 'AppCoder/editarPerfil.html', {"formUsuario": formulario, "formAvatar": forlumarioAvatar, "formPerfil": forlumarioPerfil, "perfil": perfil, "avatar": avatar, "usuario": usuario})
        else:
                formulario = ModificoUsuarioForm(initial={
                                "username": usuario.username
                                , "first_name":usuario.first_name
                                , "last_name" : usuario.last_name
                                , "email" : usuario.email
                                , "password1" : ""
                                , "password1" : ""
                                #, "web" : perfil.web
                                #, "descripcion" : perfil.descripcion
                                #, "avatar" : avatar
                })
                forlumarioAvatar = ModificoAvatarForm(initial={
                                "imagen" : avatar.imagen
                })
                forlumarioPerfil = ModificoPerfilForm(initial={
                                "web": perfil.web
                                , "descripcion" : perfil.descripcion
                })
                return render(request, "AppCoder/editarPerfil.html", {"formUsuario": formulario, "formAvatar": forlumarioAvatar, "formPerfil": forlumarioPerfil, "perfil": perfil, "avatar": avatar, "usuario": usuario})


def buscarUsuarios(request):
        usuario = request.GET["usuario"]
        if (usuario!=""):
                usuarios = User.objects.filter(username__icontains=usuario) #buscar otros filtros en la documentacion de django
                if (len(usuarios)>0):
                        for (usu) in usuarios:
                                usu.avatar = obtenerAvatar(usu.id)
                                usu.perfil = obtenerPerfil(usu.id)                        
                        return render(request, "AppCoder/usuarios.html", {"usuarios": usuarios, "filtro": usuario})
                else:
                        return render(request, "AppCoder/usuarios.html", {"usuario": usuarios, "filtro": usuario, "mensaje": "No se encontraron casos que se ajusten al filtro!"})        
        else:
                usuarios = User.objects.all() #Profesor.objects.filter(nombre__icontains="P").all()
                for (usu) in usuarios:
                        usu.avatar = obtenerAvatar(usu.id)
                        usu.perfil = obtenerPerfil(usu.id)                
                return render(request, "AppCoder/usuarios.html", {"usuarios": usuarios, "mensaje": "No se ingresó ningún dato para filtrar!"})
                
