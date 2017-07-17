# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre_actividad', models.CharField(max_length=120)),
                ('objetivos_iniciales', models.TextField()),
                ('organizacion_objetivo', models.CharField(max_length=120)),
                ('calendario_previsto', models.FileField(upload_to=b'')),
                ('recursos', models.BigIntegerField()),
                ('proceso', models.FileField(upload_to=b'')),
                ('efecto', models.CharField(max_length=120)),
            ],
            options={
                'verbose_name': 'Actividad',
                'verbose_name_plural': 'Actividades',
            },
        ),
        migrations.CreateModel(
            name='Conclusion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre_corto', models.CharField(max_length=7)),
                ('titulo', models.CharField(max_length=120)),
                ('descripcion', models.TextField()),
            ],
            options={
                'verbose_name': 'Grupo de ideas',
                'verbose_name_plural': 'Grupos de ideas',
            },
        ),
        migrations.CreateModel(
            name='Diagrama_de_causa_efecto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('factor_clave', models.CharField(max_length=20)),
                ('efecto', models.ForeignKey(to='Benchmarking.Actividad')),
            ],
            options={
                'verbose_name': 'Diagrama de causa y efecto',
                'verbose_name_plural': 'Diagramas de causa y efecto',
            },
        ),
        migrations.CreateModel(
            name='Diagrama_de_pareto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('frecuencia_acumulada', models.PositiveIntegerField()),
                ('frecuencia_porcentual', models.PositiveIntegerField()),
                ('frecuencia_porcentual_acumulada', models.PositiveIntegerField()),
            ],
            options={
                'verbose_name': 'Diagrama de pareto',
                'verbose_name_plural': 'Diagramas de pareto',
            },
        ),
        migrations.CreateModel(
            name='Entrevista',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cargo_invitado', models.CharField(max_length=30)),
                ('email_invitado', models.EmailField(max_length=254)),
                ('objetivo_entrevista', models.TextField()),
            ],
            options={
                'verbose_name': 'Entrevista',
                'verbose_name_plural': 'Entrevistas',
            },
        ),
        migrations.CreateModel(
            name='Estudio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.PositiveIntegerField(default=1)),
                ('titulo', models.CharField(max_length=100)),
                ('tematica', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Estudio',
                'verbose_name_plural': 'Estudios',
            },
        ),
        migrations.CreateModel(
            name='Idea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Idea',
                'verbose_name_plural': 'Ideas',
            },
        ),
        migrations.CreateModel(
            name='Lluvia_de_ideas',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.PositiveIntegerField(default=1)),
                ('reglas', models.TextField()),
                ('titulo', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Lluvia de ideas',
                'verbose_name_plural': 'Lluvias de ideas',
            },
        ),
        migrations.CreateModel(
            name='Organizacion',
            fields=[
                ('nombre_organizacion', models.CharField(max_length=120)),
                ('pais', models.CharField(max_length=20)),
                ('tipo_organizacion', models.CharField(max_length=1, choices=[(b'1', b'Extractiva'), (b'2', 'Agr\xedcola'), (b'3', b'Fabril'), (b'4', b'Comercial'), (b'5', b'Sanitaria'), (b'6', b'Instructora'), (b'7', b'Social'), (b'8', b'Servicios')])),
                ('directivo_organizacion', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Organizacion',
                'verbose_name_plural': 'Organizaciones',
            },
        ),
        migrations.CreateModel(
            name='Publicacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('asunto', models.CharField(max_length=120)),
                ('mensaje', models.TextField()),
                ('archivo', models.FileField(upload_to=b'')),
                ('fecha_actual', models.DateTimeField()),
                ('usuario', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Publicacion',
                'verbose_name_plural': 'Publicaciones',
            },
        ),
        migrations.CreateModel(
            name='Sesion_ideas',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo_sesion', models.PositiveIntegerField()),
                ('permitir_ideas', models.BooleanField(default=False, help_text=b'Permitir la cracion de ideas')),
                ('estado', models.BooleanField(default=True, help_text=b'Permitir la votaci\xc3\xb3n de ideas')),
                ('fecha_actual', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_inicial', models.DateField(default=django.utils.timezone.now)),
                ('fecha_final', models.DateField(default=django.utils.timezone.now)),
                ('seleccionar', models.IntegerField(default=0)),
                ('lluvia_ideas', models.ForeignKey(default=b'', editable=b'False', to='Benchmarking.Lluvia_de_ideas', verbose_name=b'Lluvia de ideas')),
                ('usar_sesion', models.ForeignKey(verbose_name=b'Sesion Padre', blank=True, to='Benchmarking.Sesion_ideas', null=True)),
            ],
            options={
                'ordering': ('lluvia_ideas', 'codigo_sesion'),
                'verbose_name': 'Sesion de Lluvia de ideas',
                'verbose_name_plural': 'Sesiones de Lluvia de ideas',
            },
        ),
        migrations.CreateModel(
            name='Punto_de_medida',
            fields=[
                ('factor_clave', models.OneToOneField(primary_key=True, serialize=False, to='Benchmarking.Idea')),
                ('frecuencia', models.PositiveIntegerField()),
                ('argumento', models.TextField()),
                ('Diagrama_de_pareto', models.ForeignKey(to='Benchmarking.Diagrama_de_pareto')),
            ],
            options={
                'verbose_name': 'Punto de mdedida',
                'verbose_name_plural': 'Puntos de medidas',
            },
        ),
        migrations.AddField(
            model_name='lluvia_de_ideas',
            name='equipo_expertos',
            field=models.ManyToManyField(related_name='grupo_expertos', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lluvia_de_ideas',
            name='moderador',
            field=models.ManyToManyField(related_name='moderador', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='idea',
            name='sesion',
            field=models.ForeignKey(related_name='ideas_sesion_lluvia', default=b'', editable=b'False', to='Benchmarking.Sesion_ideas'),
        ),
        migrations.AddField(
            model_name='estudio',
            name='analista_externo',
            field=models.ManyToManyField(related_name='bench_analista_externo_set', verbose_name=b'Analista_externo', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='estudio',
            name='equipo_expertos',
            field=models.ManyToManyField(related_name='bench_expertos_set', verbose_name=b'Expertos', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='estudio',
            name='moderador',
            field=models.ManyToManyField(related_name='bench_moderador_set', verbose_name=b'Moderador', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='estudio',
            name='organizacion',
            field=models.OneToOneField(related_name='bench_organizacion_set', verbose_name=b'Organizacion_bench', to='Benchmarking.Organizacion'),
        ),
        migrations.AddField(
            model_name='entrevista',
            name='equipo_expertos',
            field=models.ManyToManyField(related_name='expertos', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='entrevista',
            name='organizacion',
            field=models.OneToOneField(to='Benchmarking.Organizacion'),
        ),
        migrations.AddField(
            model_name='entrevista',
            name='preguntas',
            field=models.ForeignKey(to='Benchmarking.Lluvia_de_ideas'),
        ),
        migrations.AddField(
            model_name='diagrama_de_causa_efecto',
            name='lluvia_de_idea',
            field=models.ForeignKey(to='Benchmarking.Lluvia_de_ideas'),
        ),
        migrations.AddField(
            model_name='conclusion',
            name='ideas',
            field=models.ManyToManyField(related_name='ideas_set', verbose_name=b'ideas', to='Benchmarking.Idea'),
        ),
        migrations.AlterUniqueTogether(
            name='sesion_ideas',
            unique_together=set([('codigo_sesion', 'lluvia_ideas')]),
        ),
    ]
