# Generated by Django 4.1.7 on 2023-04-27 20:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('AppCoder', '0008_perfiles_avatares'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categorias',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=40)),
                ('imagen', models.ImageField(upload_to='imgs/cat/')),
            ],
            options={
                'verbose_name': 'Categoría',
                'verbose_name_plural': 'Categorías',
            },
        ),
        migrations.CreateModel(
            name='Notas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=120)),
                ('subtitulo', models.CharField(max_length=255)),
                ('cuerpo', models.CharField(max_length=4000)),
                ('imagen', models.ImageField(default='imgs/defaults/pubSinFoto.jpg', upload_to='imgs/pub/')),
                ('cuando', models.DateTimeField()),
                ('link', models.CharField(max_length=150)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='autor', to=settings.AUTH_USER_MODEL)),
                ('categoria', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='AppCoder.categorias')),
            ],
            options={
                'verbose_name': 'Publicación',
                'verbose_name_plural': 'Publicaciones',
            },
        ),
        migrations.RemoveField(
            model_name='peliculas',
            name='act_destacado',
        ),
        migrations.RemoveField(
            model_name='peliculas',
            name='director',
        ),
        migrations.RemoveField(
            model_name='peliculas',
            name='genero',
        ),
        migrations.RemoveField(
            model_name='peliculas',
            name='tag',
        ),
        migrations.DeleteModel(
            name='Tipos',
        ),
        migrations.AlterModelOptions(
            name='avatares',
            options={'verbose_name': 'Avatar', 'verbose_name_plural': 'Avatares'},
        ),
        migrations.AlterModelOptions(
            name='perfiles',
            options={'verbose_name': 'Perfil', 'verbose_name_plural': 'Perfiles'},
        ),
        migrations.DeleteModel(
            name='Acts',
        ),
        migrations.DeleteModel(
            name='Directores',
        ),
        migrations.DeleteModel(
            name='Generos',
        ),
        migrations.DeleteModel(
            name='Peliculas',
        ),
        migrations.DeleteModel(
            name='Tags',
        ),
    ]
