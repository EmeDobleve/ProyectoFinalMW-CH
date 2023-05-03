from django.db import models
from datetime import date
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField 

# Create your models here.

#Estadios, Partidos, Anécdotas, Mística, Artistas, Mundiales
class Categorias(models.Model):
    nombre = models.CharField(max_length=40)
    imagen = models.ImageField(
            upload_to='imgs/cat/'
            , height_field=None
            , width_field=None
            , max_length=100
    )

    def __str__(self):
        return f"{self.nombre}"     
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"    

#Películas recomendadas
class Articulos(models.Model):
        titulo = models.CharField(max_length=120)
        subtitulo = models.CharField(max_length=255)
        #cuerpo = models.CharField(max_length=4000)
        #cuerpo = RichTextField()
        cuerpo = RichTextField(blank=True, null=True)
        imagen = models.ImageField(
            upload_to='imgs/pub/'
            , height_field=None
            , width_field=None
            , max_length=100
            , default="imgs/defaults/pubSinFoto.jpg"
        )
        autor=models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="autor")
        cuando = models.DateTimeField(null=False)
        categoria = models.ForeignKey(
            'Categorias'
            , on_delete=models.RESTRICT
            , null=True
        )
        link = models.CharField(max_length=150)

        def __str__(self):
                return f"({self.cuando}) de {self.autor.username}: {self.titulo}"

        class Meta:
                verbose_name = "Publicación"
                verbose_name_plural = "Publicaciones"


class Avatares(models.Model):
        usuario=models.ForeignKey(User, on_delete=models.CASCADE, null=False)
        imagen= models.ImageField(upload_to="imgs/avt/", default="imgs/defaults/perSinFoto.jpg")

        def __str__(self):
                return f"{self.usuario.username} - Avatar"
        
        class Meta:
                verbose_name = "Avatar"
                verbose_name_plural = "Avatares"        

class Perfiles(models.Model):
        usuario=models.ForeignKey(User, on_delete=models.CASCADE, null=False)
        web = models.CharField(max_length=250)
        descripcion = models.CharField(max_length=500)

        def __str__(self):
                return f"{self.usuario.username} - Perfil"
        
        class Meta:
                verbose_name = "Perfil"
                verbose_name_plural = "Perfiles"