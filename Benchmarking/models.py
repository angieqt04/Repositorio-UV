# coding: utf-8
from django.utils import timezone
import django_comments as comments
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.db import models
from Softprosp.utils import multikeysort
from django.contrib.auth.models import User

# Create your models here.
class Organizacion(models.Model):
    CLASIFICACION_ORG = (
        ('1', 'Extractiva'),
        ('2', u'Agrícola'),
        ('3', 'Fabril'),
        ('4', 'Comercial'),
        ('5', 'Sanitaria'),
        ('6', 'Instructora'),
        ('7', 'Social'),
        ('8', 'Servicios'),
    )
    nombre_organizacion = models.CharField(max_length=120)
    pais = models.CharField(max_length= 20)
    tipo_organizacion = models.CharField(max_length=1, choices=CLASIFICACION_ORG)
    directivo_organizacion = models.OneToOneField(User, primary_key=True)

    class Meta:
        verbose_name = 'Organizacion'
        verbose_name_plural = 'Organizaciones'

    def __unicode__(self):
        return u'{0}'.format(self.nombre_organizacion)

class Estudio(models.Model):
    codigo = models.PositiveIntegerField(default=1)
    titulo = models.CharField(max_length=100)
    #proyecto = models.ForeignKey('Proyectos')
    tematica = models.CharField(max_length=100)
    equipo_expertos = models.ManyToManyField('auth.User', verbose_name='Expertos', related_name='bench_expertos_set')
    moderador = models.ManyToManyField('auth.User', verbose_name='Moderador', related_name='bench_moderador_set')
    analista_externo = models.ManyToManyField('auth.User', verbose_name='Analista_externo', related_name='bench_analista_externo_set')
    organizacion = models.OneToOneField(Organizacion, verbose_name='Organizacion_bench', related_name='bench_organizacion_set')

    class Meta:
        verbose_name = 'Estudio'
        verbose_name_plural = 'Estudios'

    def __unicode__(self):
        return u'{0}'.format(self.titulo)

class Publicacion(models.Model):
    asunto = models.CharField(max_length=120)
    mensaje = models.TextField()
    archivo = models.FileField()
    fecha_actual = models.DateTimeField()
    usuario = models.OneToOneField(User)

    class Meta:
        verbose_name = 'Publicacion'
        verbose_name_plural = 'Publicaciones'

    def __str__(self):
        return '{} {}'.format(self.asunto, self.archivo)

class Actividad(models.Model):
    nombre_actividad = models.CharField(max_length=120)
    objetivos_iniciales = models.TextField()
    organizacion_objetivo = models.CharField(max_length=120)
    calendario_previsto = models.FileField()
    recursos = models.BigIntegerField()
    proceso = models.FileField()
    efecto = models.CharField(max_length=120)

    class Meta:
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'

    def __unicode__(self):
        return u'{0}'.format(self.nombre_actividad)

class Lluvia_de_ideas(models.Model):
    codigo = models.PositiveIntegerField(default=1)
    reglas = models.TextField()
    titulo = models.CharField(max_length=50)
    equipo_expertos = models.ManyToManyField(User, related_name = 'grupo_expertos')
    moderador = models.ManyToManyField(User, related_name = 'moderador')

    class Meta:
        verbose_name = 'Lluvia de ideas'
        verbose_name_plural = 'Lluvias de ideas'

    def __unicode__(self):
        return u'{0}'.format(self.titulo)

class Entrevista(models.Model):
    cargo_invitado = models.CharField(max_length=30)
    email_invitado = models.EmailField()
    objetivo_entrevista = models.TextField()
    preguntas = models.ForeignKey(Lluvia_de_ideas)
    organizacion = models.OneToOneField(Organizacion)
    equipo_expertos = models.ManyToManyField(User, related_name = 'expertos')

    class Meta:
        verbose_name = 'Entrevista'
        verbose_name_plural = 'Entrevistas'

    def __unicode__(self):
        return u'{0}'.format(self.objetivo_entrevista)

class Sesion_ideas(models.Model):
    lluvia_ideas = models.ForeignKey(
        'Lluvia_de_ideas',
        verbose_name= 'Lluvia de ideas',
        default="",
        editable="False"
    )
    codigo_sesion = models.PositiveIntegerField()
    permitir_ideas = models.BooleanField(
        default=False,
        help_text='Permitir la cracion de ideas')
    estado = models.BooleanField(
        default=True,
        help_text='Permitir la votación de ideas')
    fecha_actual =  models.DateTimeField(
        default= timezone.now)
    fecha_inicial = models.DateField(
        default= timezone.now)
    fecha_final = models.DateField(
        default= timezone.now)
    usar_sesion = models.ForeignKey(
        'Sesion_ideas',
        blank=True,
        null=True,
        verbose_name='Sesion Padre')
    seleccionar = models.IntegerField(
        default=0)

    class Meta:
        verbose_name = 'Sesion de Lluvia de ideas'
        verbose_name_plural = 'Sesiones de Lluvia de ideas'
        unique_together = ('codigo_sesion', 'lluvia_ideas')
        ordering = ('lluvia_ideas', 'codigo_sesion')

    def buscar_items(self, numero_items = None):
        ideas = self.ideas.filter(activo=True)
        items = []
        for braintem in ideas:
            commentswithvote = braintem.comments_brain_item()
            votos_positivos = commentswithvote.filter(voto = '+').count()
            votos_negativos = commentswithvote.filter(voto = '-').count()
            items.append({
                'id': braintem.id,
                'item':braintem.titulo,
                'votos_positivos': votos_positivos,
                'votos-negativos': votos_negativos,
                'votos_finales': votos_positivos-votos_negativos,
                'votos_totales': votos_positivos+votos_negativos
            })
        items = multikeysort(
            items,
            ('-votos_finales',
             '-votos_positivos',
             '-votos_negativos'))

        if numero_items is not None:
            if numero_items > items.__len__():
                numero_items = items.__len__()
            items = items[:numero_items]
        return items

    def __unicode__(self):
        return u'sesion {0} de la lluvia de ideas {0}'.format(self.codigo_sesion, self.lluvia_ideas.titulo)







    def __str__(self):
        return '{}'.format(self.codigo_sesion)

class Idea(models.Model):
    sesion = models.ForeignKey(
        'Sesion_ideas',
        related_name= 'ideas_sesion_lluvia',
        default = "",
        editable="False")
    activo = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.new_field:
            self.new_field = self.website
        super(Idea,self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Idea'
        verbose_name_plural = 'Ideas'

    def __unicode__(self):
        return u'{0}'.format(self.titulo)

    def comments_brain_item(self, id_lluvia = None):
        comment_model =comments.get_model()
        ctype = ContentType.objects.get_for_model(self)
        if id_lluvia is None:
            id_lluvia = self.id

        commentswithvote = comment_model.objects.filter(
            content_type = ctype,
            object_pk = id_lluvia,
            is_public = True,
            is_removed = False,
            site__pk = settings.SITE_ID)
        return commentswithvote

class Conclusion(models.Model):
    nombre_corto = models.CharField(max_length=7)
    titulo = models.CharField(max_length=120)
    descripcion = models.TextField()
    #sesion = models.ForeignKey('Sesion_ideas', verbose_name='sesion', related_name='sesion_set')
    ideas = models.ManyToManyField('Idea', verbose_name='ideas', related_name='ideas_set')

    class Meta:
        verbose_name = 'Grupo de ideas'
        verbose_name_plural = 'Grupos de ideas'

    def __unicode__(self):
        return u'{0}'.format(self.titulo)

class Diagrama_de_causa_efecto(models.Model):

    efecto = models.ForeignKey(Actividad)
    lluvia_de_idea = models.ForeignKey(Lluvia_de_ideas)
    factor_clave = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Diagrama de causa y efecto'
        verbose_name_plural = 'Diagramas de causa y efecto'

    def __unicode__(self):
        return u'{0} {0}'.format(self.efecto, self.factor_clave)

class Diagrama_de_pareto(models.Model):
    frecuencia_acumulada = models.PositiveIntegerField()
    frecuencia_porcentual = models.PositiveIntegerField()
    frecuencia_porcentual_acumulada = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Diagrama de pareto'
        verbose_name_plural = 'Diagramas de pareto'

    def __unicode__(self):
        return u'{0}'.format(self.frecuencia_acumulada)

class Punto_de_medida(models.Model):
    factor_clave = models.OneToOneField(Idea, primary_key=True)
    frecuencia = models.PositiveIntegerField()
    argumento = models.TextField()
    Diagrama_de_pareto = models.ForeignKey(Diagrama_de_pareto)

    class Meta:
        verbose_name = 'Punto de mdedida'
        verbose_name_plural = 'Puntos de medidas'

    def __unicode__(self):
        return u'{} {}'.format(self.efecto, self.factor_clave, self.frecuencia)