# Generated by Django 4.1.7 on 2023-05-03 14:34

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AppCoder', '0011_alter_articulos_cuerpo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulos',
            name='cuerpo',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
