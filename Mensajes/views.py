# Create your views here.
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from Mensajes.models import *
from .forms import MensajesForm
from AppCoder.views import obtenerAvatar, obtenerPerfil
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Count
from django.conf import settings
from django.utils.timezone import make_aware

# Create your views here.
def mensajes(request):

        form = MensajesForm()
        usuariosConConversacionesEnLosUltimos3Meses = obtenerUsuariosDeMensajesUlt3meses(request)
        mensajesSinLeer = obtenerMensajesSinLeerA(request.user.id)
                
        if ((request.GET) and (request.GET["usuario"] != "")):
                usuario = request.GET["usuario"]

                mensajesSinLeer = mensajesSinLeer.filter(emisor__username__icontains=usuario)
                cantMensajesNuevos = len(mensajesSinLeer)
                mensajesSinLeer = mensajesSinLeer.values("emisor").distinct() 
                conversacionesAMostrar = obtenerConversacionesSinLeerA(request, mensajesSinLeer)    

                if (len(mensajesSinLeer)>0):
                        return render(request, "Mensajes/mensajes.html", {"form" : form, "cantMensajesNuevos": cantMensajesNuevos, "filtro": usuario, "cantConversacionesAMostrar": len(conversacionesAMostrar), "usuariosAMostrar": usuariosConConversacionesEnLosUltimos3Meses, "conversacionesAMostrar":conversacionesAMostrar})
                else:
                        return render(request, "Mensajes/mensajes.html", {"form" : form, "cantMensajesNuevos": cantMensajesNuevos, "filtro": usuario, "cantConversacionesAMostrar": len(conversacionesAMostrar), "mensaje": "No se encontraron casos que se ajusten al filtro!", "usuariosAMostrar": usuariosConConversacionesEnLosUltimos3Meses, "conversacionesAMostrar":conversacionesAMostrar, "cantConversacionesAMostrar": len(conversacionesAMostrar)})
        else:

                cantMensajesNuevos = len(mensajesSinLeer)
                mensajesSinLeer = mensajesSinLeer.values("emisor").distinct() 
                conversacionesAMostrar = obtenerConversacionesSinLeerA(request,mensajesSinLeer)    
                
                return render(request, "Mensajes/mensajes.html", {"form" : form, "cantMensajesNuevos": cantMensajesNuevos, "cantConversacionesAMostrar": len(conversacionesAMostrar), "usuariosAMostrar": usuariosConConversacionesEnLosUltimos3Meses, "conversacionesAMostrar":conversacionesAMostrar, "cantConversacionesAMostrar": len(conversacionesAMostrar)})

def crearMensaje(request):
        form = MensajesForm()
        mensajes = Mensajes.objects.all() #Profesor.objects.filter(nombre__icontains="P").all()
        return render(request, "Mensajes/conversaciones.html", {"mensajes": mensajes, "form" : form})


def buscarUsuarioMensaje(request):
        #usuario = request.GET["usuario"]
        if ((request.GET) and (request.GET["usuario"] != "")):
                usuario = request.GET["usuario"]
                usuarios = User.objects.filter(username__icontains=usuario).order_by("username") #buscar otros filtros en la documentacion de django
                if (len(usuarios)!=0):
                        for (usu) in usuarios:
                                usu.avatar = obtenerAvatar(usu.id)
                                usu.perfil = obtenerPerfil(usu.id)

                if (len(usuario)>0):
                        return render(request, "Mensajes/buscarUsuariosParaMensajes.html", {"usuarios": usuarios, "filtro": usuario})
                else:
                        return render(request, "Mensajes/buscarUsuariosParaMensajes.html", {"usuarios": usuarios, "filtro": usuario, "mensaje": "No se encontraron casos que se ajusten al filtro!"})        
        else:
                usuarios = User.objects.all().order_by("username") #Profesor.objects.filter(nombre__icontains="P").all()
                if (len(usuarios)!=0):
                        for (usu) in usuarios:
                                usu.avatar = obtenerAvatar(usu.id)
                                usu.perfil = obtenerPerfil(usu.id)                
                return render(request, "Mensajes/buscarUsuariosParaMensajes.html", {"usuarios": usuarios})


def crearMensajeAUsuario(request,id):

    usuarioDestino = User.objects.filter(id=id)[0]

    if request.method == "POST":
        form = MensajesForm(request.POST)
        if form.is_valid():
                mensaje = Mensajes()
                info = form.cleaned_data

                mensaje.texto = info['texto']
                if (info['respuesta_a']!='0'):
                    mensaje.respuesta_a = Mensajes.objects.filter(id=info['respuesta_a'])[0]
                else:
                    mensaje.respuesta_a = None
                mensaje.emisor = request.user
                mensaje.receptor = usuarioDestino
                settings.TIME_ZONE
                mensaje.cuando = make_aware(datetime.now())
                mensaje.save()
                formulario = MensajesForm()
                #mensajes = Mensajes.objects.filter(receptor__id__in=[usuarioDestino.id, request.user.id]).filter(emisor__id__in=[usuarioDestino.id, request.user.id]).exclude(emisor=request.user, receptor=request.user).exclude(emisor=usuarioDestino, receptor=usuarioDestino).order_by("cuando")
                mensajes = obtenerMensajesEntre(request.user.id, usuarioDestino.id)
                #mensajes = Mensajes.objects.filter(emisor__id=id) #buscar otros filtros en la documentacion de django
                return render(request, "Mensajes/crearMensaje.html", {"id": id, "form": formulario, "mensajes": mensajes, "mensajesNuevos": contarNuevosYMarcarComoLeidos(mensajes, usuarioDestino.id), "usuarioDestino": usuarioDestino, "mensaje":"Mensaje Enviado!"})
        else:
                print(form.errors)
                messages.error(request, form.errors)
                formulario= MensajesForm(initial={"texto":form.cleaned_data['texto'], "respuesta_a":form['respuesta_a']})
                #mensajes = Mensajes.objects.filter(emisor__username__icontains=usuario) #buscar otros filtros en la documentacion de django
                #mensajes = Mensajes.objects.filter(receptor__id__in=[usuarioDestino.id, request.user.id]).filter(emisor__id__in=[usuarioDestino.id, request.user.id]).exclude(emisor=request.user, receptor=request.user).exclude(emisor=usuarioDestino, receptor=usuarioDestino).order_by("cuando")
                mensajes = obtenerMensajesEntre(request.user.id, usuarioDestino.id)
                return render(request, "Mensajes/crearMensaje.html", {"id": id, "form": formulario, "mensajesNuevos": contarNuevosYMarcarComoLeidos(mensajes, usuarioDestino.id), "mensajes": mensajes, "usuarioDestino": usuarioDestino, "mensaje":"Algo falló. Intente Nuevamnte."})
    else:
        formulario = MensajesForm()
        #mensajes = Mensajes.objects.all() 
        #mensajes = Mensajes.objects.filter(receptor=usuarioDestino).filter(emisor=request.user)
        #mensajes = Mensajes.objects.filter(receptor__id__in=[usuarioDestino.id, request.user.id]).filter(emisor__id__in=[usuarioDestino.id, request.user.id]).exclude(emisor=request.user, receptor=request.user).exclude(emisor=usuarioDestino, receptor=usuarioDestino).order_by("cuando")
        mensajes = obtenerMensajesEntre(request.user.id, usuarioDestino.id)
        return render(request, "Mensajes/crearMensaje.html", {"id": id, "mensajes": mensajes, "mensajesNuevos": contarNuevosYMarcarComoLeidos(mensajes, usuarioDestino.id), "usuarioDestino": usuarioDestino, "form" : formulario})
    

def responderMensajeAUsuario(request,id,mensajeId):
        usuarioDestino = User.objects.filter(id=id)[0]
        mensajeRespondido = Mensajes.objects.filter(id=mensajeId)[0]
        form = MensajesForm(initial={"respuesta_a":mensajeId})
        #mensajes = Mensajes.objects.filter(receptor__id__in=[usuarioDestino.id, request.user.id]).filter(emisor__id__in=[usuarioDestino.id, request.user.id]).exclude(emisor=request.user, receptor=request.user).exclude(emisor=usuarioDestino, receptor=usuarioDestino).order_by("cuando")
        mensajes = obtenerMensajesEntre(request.user.id, usuarioDestino.id)
        return render(request, "Mensajes/crearMensaje.html", {"id": id, "mensajes": mensajes, "mensajesNuevos": contarNuevosYMarcarComoLeidos(mensajes, usuarioDestino.id), "usuarioDestino": usuarioDestino, "form" : form, "mensajeRespondido":mensajeRespondido})

def obtenerMensajesSinLeerA(usuarioReceptorID):
        #return Mensajes.objects.filter(receptor__id=usuarioReceptorID).filter(leido=False).order_by("-cuando")
        return Mensajes.objects.filter(receptor__id=usuarioReceptorID).filter(leido=False)

def obtenerMensajesOrdenadosSinLeerA(usuarioReceptorID):
        return Mensajes.objects.filter(receptor__id=usuarioReceptorID).filter(leido=False).order_by("-cuando")

def obtenerMensajesSinLeerAyDe(usuarioReceptorID, usuarioEmisorID):
        return Mensajes.objects.filter(receptor__id=usuarioReceptorID).filter(emisor__id=usuarioEmisorID).filter(leido=False).order_by("-cuando")

def obtenerMensajesEntre(UsuarioLogueadoID, UsuarioInteractuaID):
        mensajes = Mensajes.objects.filter(receptor__id__in=[UsuarioInteractuaID, UsuarioLogueadoID]).filter(emisor__id__in=[UsuarioInteractuaID, UsuarioLogueadoID]).exclude(emisor__id=UsuarioLogueadoID, receptor__id=UsuarioLogueadoID).exclude(emisor__id=UsuarioInteractuaID, receptor__id=UsuarioInteractuaID).order_by("cuando")
        mensajes.filter(leido=True).filter(mostrar_como_leido=False).update(mostrar_como_leido=True)
        return mensajes

def contarNuevosYMarcarComoLeidos(mensajes,usuarioID):
        return mensajes.filter(emisor__id = usuarioID).filter(leido=False).update(leido=True)

def obtenerUsuariosDeMensajesUlt3meses(request):
        settings.TIME_ZONE
        hace3Meses = make_aware(datetime.now() - relativedelta(months=3))
        ult3MesesComoReceptor = Mensajes.objects.filter(receptor=request.user.id).filter(cuando__gte = hace3Meses).values("emisor").distinct() 
        ult3MesesComoEmisor = Mensajes.objects.filter(emisor=request.user.id).filter(cuando__gte = hace3Meses).values("receptor").exclude(receptor__in=ult3MesesComoReceptor).distinct()
        
        usuariosUlt3Meses = []
        for usu in ult3MesesComoReceptor:
                usuariosUlt3Meses.append({'usuarioEmisorID': usu["emisor"], 'username': User.objects.filter(id=usu["emisor"])[0].username})
        
        for usu in ult3MesesComoEmisor:
                usuariosUlt3Meses.append({'usuarioEmisorID': usu["receptor"], 'username': User.objects.filter(id=usu["receptor"])[0].username})                

        usuariosUlt3Meses.sort(key=usernameDe)

        #print(type(usuariosUlt3Meses))
        return(usuariosUlt3Meses)

def usernameDe(dicc):
        return dicc["username"]

def obtenerConversacionesSinLeerA(request,conversaciones):
        conversacionesSinLeer = []
        for usu in conversaciones:
                conversacionesSinLeer.append({'usuarioEmisorID': usu["emisor"], 'username': User.objects.filter(id=usu["emisor"])[0].username, "cantidadSinLeer":len(obtenerMensajesSinLeerAyDe(request.user.id,usu["emisor"]))})

        conversacionesSinLeer.sort(key=usernameDe)
        return (conversacionesSinLeer)

