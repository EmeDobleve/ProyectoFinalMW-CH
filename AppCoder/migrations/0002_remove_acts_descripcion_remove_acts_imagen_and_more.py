# Generated by Django 4.1.7 on 2023-04-15 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppCoder', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='acts',
            name='descripcion',
        ),
        migrations.RemoveField(
            model_name='acts',
            name='imagen',
        ),
        migrations.RemoveField(
            model_name='directores',
            name='descripcion',
        ),
        migrations.RemoveField(
            model_name='directores',
            name='imagen',
        ),
        migrations.AddField(
            model_name='acts',
            name='apellido',
            field=models.CharField(default='Sin Apellido', max_length=100),
        ),
        migrations.AddField(
            model_name='directores',
            name='apellido',
            field=models.CharField(default='Sin Apellido', max_length=100),
        ),
        migrations.AlterField(
            model_name='acts',
            name='nombre',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='directores',
            name='nombre',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='generos',
            name='descripcion',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='generos',
            name='imagen',
            field=models.ImageField(upload_to='imgs/cat/'),
        ),
        migrations.AlterField(
            model_name='tipos',
            name='imagen',
            field=models.ImageField(upload_to='imgs/tip/'),
        ),
    ]