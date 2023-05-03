from django import forms
from django.forms import ModelForm
from AppCoder.models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from ckeditor.widgets import CKEditorWidget

class CategoriaForm(forms.Form):
    nombre = forms.CharField(max_length=40)
    imagen = forms.ImageField(max_length=100,allow_empty_file=False)

#Películas recomendadas
class ArticuloForm(forms.Form):
        titulo = forms.CharField(max_length=120)
        subtitulo = forms.CharField(max_length=255)
        cuerpo = forms.CharField(label="Cuerpo", required=False,  widget = CKEditorWidget()) #widget=forms.Textarea(attrs={"rows":"5","cols":"60"}))
        imagen = forms.ImageField(max_length=100,allow_empty_file=False)
        #autor=forms.ModelChoiceField(queryset=User.objects.all())
        #cuando = models.DateTimeField(null=False)
        categoria = forms.ModelChoiceField(queryset=Categorias.objects.all())
        link = forms.CharField(max_length=150)    
       
class RegistroUsuarioForm(UserCreationForm):
    username = forms.CharField(label = "Nombre de Usuario", required=True)
    email = forms.EmailField(label = "Correo Electrónico", required=True)
    password1 = forms.CharField(label="Contraseña", required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar la Contraseña", required=True, widget=forms.PasswordInput)
    #first_name = forms.CharField(label="Nombre", required=True)
    #last_name = forms.CharField(label="Apellido", required=True)

    class Meta:
       model = User
       fields = ["username", "email", "password1", "password2"] #, "first_name", "last_name"
       #helptext = {k:"" for k in fields}

class ModificoUsuarioForm(UserCreationForm, forms.Form):
    username = forms.CharField(widget=forms.HiddenInput())
    first_name = forms.CharField(label = "Nombre", required=False)
    last_name = forms.CharField(label = "Apellido", required=False)
    email = forms.EmailField(label = "Correo Electrónico", required=True)
    password1 = forms.CharField(label="Contraseña", required=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar la Contraseña", required=False, widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=["email", "password1", "password2", "first_name", "last_name"]
        help_texts = {k:"" for k in fields}#para cada uno de los campos del formulario, le asigna un valor vacio

class ModificoAvatarForm(forms.Form):
    imagen = forms.ImageField(label="Avatar",max_length=150,allow_empty_file=False)            

    class Meta:
        model=Avatares
        fields=["imagen"]
        help_texts = {k:"" for k in fields}#para cada uno de los campos del formulario, le asigna un valor vacio        

class ModificoPerfilForm(forms.Form):
    web = forms.CharField(max_length=250,label="Página Web", required=False)
    descripcion = forms.CharField(max_length=500,label="Descripción", required=False)

    class Meta:
        model=Perfiles
        fields=["web","descripcion"]
        help_texts = {k:"" for k in fields}#para cada uno de los campos del formulario, le asigna un valor vacio                


