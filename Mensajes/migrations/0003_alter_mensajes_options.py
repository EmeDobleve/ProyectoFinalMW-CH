# Generated by Django 4.1.7 on 2023-05-03 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Mensajes', '0002_mensajes_mostrar_como_leido'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mensajes',
            options={'verbose_name': 'Mensaje', 'verbose_name_plural': 'Mensajes'},
        ),
    ]
