# coding: utf-8
from django import forms
import autocomplete_light
from django.utils.translation import ugettext as _
from Softprosp.mixins import AjaxFormMixin
from Benchmarking.models import Actividad, Organizacion, Estudio, Sesion_ideas, Idea, Conclusion, Lluvia_de_ideas


class ActividadForm(forms.ModelForm):

    class Meta:
        model = Actividad

        fields = (
            'nombre_actividad',
            'objetivos_iniciales',
            'organizacion_objetivo',
           # 'calendario_previsto',
            'recursos',
            #'proceso',
            'efecto',
        )

        labels = {
            'nombre_actividad': 'Nombre de la actividad',
            'objetivos_iniciales': 'Objetivos iniciales',
            'organizacion_objetivo': u'Nombre de la organización objetivo',
            #'calendario_previsto': 'Calendario previsto',
            'recursos': 'Recurso',
            #'proceso': 'Proceso',
            'efecto': 'Efecto',
            'equipo_expertos': 'Equipo de expertos',
            'moderador': 'Moderador',
            'analista_externo': 'Analista externo',
        }

        widgets = {
            'nombre_actividad': forms.TextInput(attrs={'class': 'form-control'}),
            'objetivos_iniciales': forms.Textarea(attrs={'class': 'form-control', 'rows':'3', 'placeholder': 'Ingresar los objetivos iniciales del estudio'}),
            'organizacion_objetivo': forms.TextInput(attrs={'class': 'form-control'}),
            #'calendario_previsto': forms.FileInput(attrs={'class': 'form-control'}),
            'recursos': forms.TextInput(attrs={'class': 'form-control'}),
            #'proceso': forms.FileInput(attrs={'class': 'form-control'}),
            'efecto': forms.TextInput(attrs={'class': 'form-control'}),
        }

        exclude =(
            'calendario_previsto',
            'proceso'
        )

class OrganizacionForm(forms.ModelForm):

    class Meta:
        model = Organizacion

        fields = (
            'nombre_organizacion',
            'pais',
            'tipo_organizacion',
            'directivo_organizacion',
        )

        labels = {
            'nombre_organizacion': 'Nombre de la organización',
            'pais': 'País',
            'tipo_organizacion': 'Tipo de Organización',
            'directivo_organizacion': 'Directivo de la organización',
        }

        widgets = {
            'nombre_organizacion': forms.TextInput(attrs={'class':'form-control'}),
            'pais': forms.TextInput(attrs={'class':'form-control'}),
            'tipo_organizacion': forms.Select(attrs={'class':'form-control'}),
            'directivo_organizacion':forms.Select(attrs={'class':'form-control'}),

        }

class EstudioForm(forms.ModelForm):

    class Meta:
        model = Estudio

        fields = (
            'codigo',
            'titulo',
            'tematica',
            'equipo_expertos',
            'moderador',
            'analista_externo',
        )

        labels = {
            'codigo': 'Codigo',
            'titulo': 'Título',
            'tematica': 'Tematica',
            'equipo_expertos': 'Equipo de expertos',
            'moderador': 'Moderador',
            'analista_externo': 'Analista externo',
        }

        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'tematica': forms.TextInput(attrs={'class':'form-control'}),
            'equipo_expertos': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'moderador': forms.SelectMultiple(attrs={'class':'form-control'}),
            'analista_externo': forms.SelectMultiple(attrs={'class':'form-control'}),
        }

class IdeaForm(forms.ModelForm):

    class Meta:
        model = Idea

        fields = (
            'definicion_idea',
            'argumento',
        )

        labels = {
            'definicion_idea': 'Factor',
            'argumento': 'Descripción',
        }

        widgets = {
            'definicion_idea': forms.TextInput(attrs={'class': 'form-control'}),
            'argumento': forms.Textarea(attrs={'class': 'form-control', 'rows':'3', 'placeholder': 'Describir factor'}),
        }

class Factor_concluido(forms.ModelForm):

    class Meta:
        model = Conclusion

        fields = (
            'nombre_corto',
            'titulo',
            'descripcion',
            'ideas',
        )

        widgets = {
            'nombre_corto': forms.TextInput(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows':'3', 'placeholder': 'Justificar conclusión'}),
            'ideas': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

class LluviaIdeasForm(autocomplete_light.ModelForm):
    crear_sesion = forms.BooleanField(
        initial='True',
        label=(u'Crear sesion de lluvia de ideas'),
        widget=forms.HiddenInput()
    )

    class Meta:
        model = Lluvia_de_ideas
        fields = ['reglas', 'titulo', 'equipo_expertos', 'moderador']

class SesionForm(forms.ModelForm):
    lluvia_ideas = forms.ModelChoiceField(
        Lluvia_de_ideas.objects.all(),
        widget=forms.HiddenInput(),
        required=False
    )

    class Meta:
        model = Sesion_ideas
        fields = (
            'codigo_sesion',
            'fecha_inicial',
            'fecha_final',
            'permitir_ideas',
            'estado',
            'lluvia_ideas'
        )
        widgets = {
            'fecha_inicial': forms.DateInput(attrs={'class': 'datepicker'}),
            'fecha_final': forms.DateInput(attrs={'class': 'datepicker'}),
        }

class AgregarSesionForm(Sesion_ideas, AjaxFormMixin):
    usar_sesion = forms.ModelChoiceField(
        Sesion_ideas.objects.all(),
        required=False
    )

    seleccionar = forms.IntegerField(
        min_value=0,
        required=False,
        widget=forms.NumberInput(attrs={'disabled':'disabled'})
    )
    def __init__(self, *args, **kwargs):
        super(AgregarSesionForm, self).__init__(*args,**kwargs)

class EditarSesionForm(Sesion_ideas, AjaxFormMixin):
    id = forms.IntegerField(
        widget=forms.HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        self._meta.fields.append('id')
        super(EditarSesionForm, self).__init__(*args, **kwargs)


