from django import forms
from Mensajes.models import *
from django.forms import ModelForm
from django.contrib.auth.models import User

class MensajesForm(forms.Form):
        texto = forms.CharField(max_length=500,label="", required=True, widget=forms.Textarea(attrs={"rows":"5","cols":"80"}))
        respuesta_a = forms.CharField(initial=0, required=False,widget=forms.HiddenInput())

