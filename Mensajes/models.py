from argparse import _AppendAction
from django.db import models
from datetime import date
from django.contrib.auth.models import User



# Create your models here.
class Mensajes(models.Model):
        emisor=models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="emisor")
        receptor=models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="receptor")
        texto = models.CharField(max_length=500, null=False)
        respuesta_a = models.ForeignKey("Mensajes", on_delete=models.CASCADE, null=True)
        cuando = models.DateTimeField(null=False)
        leido = models.BooleanField(null=False, default=False)
        mostrar_como_leido = models.BooleanField(null=False, default=False)

        def __str__(self):
                return f"({self.cuando}) de {self.emisor.username} a {self.receptor.username}: {self.texto[:60]}"

        class Meta:
                verbose_name = "Mensaje"
                verbose_name_plural = "Mensajes"
