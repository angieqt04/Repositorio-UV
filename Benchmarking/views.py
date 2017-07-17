#coding=utf-8
import json
from django.contrib import messages
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models.query_utils import Q
from django.http.response import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.template.context import RequestContext
from django.template.loader import render_to_string
from django.utils import timezone
from Benchmarking.forms import ActividadForm, OrganizacionForm, EstudioForm, SesionForm, IdeaForm, Factor_concluido, LluviaIdeasForm, Sesion_ideas, AgregarSesionForm, EditarSesionForm
from Benchmarking.models import Actividad, Organizacion, Estudio, Sesion_ideas, Idea, Conclusion, Lluvia_de_ideas
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.core.urlresolvers import  reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext

def index(request):
   actividad = Actividad.objects.all()
   contexto = {'actividades':actividad}
   return render(request,'index.html', contexto)

class Form_Actividad(CreateView):
    model = Actividad
    form_class = ActividadForm
    template_name = 'Administrador/add_actividad.html'
    success_url = reverse_lazy('benchmarking:index')

class Form_Org(CreateView):
    model = Organizacion
    form_class = OrganizacionForm
    template_name = 'Administrador/registro_org.html'
    success_url = reverse_lazy('benchmarking:index')

class Form_Estudio(CreateView):
    model = Estudio
    form_class = EstudioForm
    second_form_class = OrganizacionForm
    template_name = 'Administrador/estudio.html'
    success_url = reverse_lazy('benchmarking:index')

#Agregar Form y Form2 al contexto
    def get_context_data(self, **kwargs):
        context = super(Form_Estudio, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            estudio = form.save(commit=False)
            estudio.organizacion =form2.save()
            estudio.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form= form, form2=form2))

class Form_Sesion(CreateView):
    model = Sesion_ideas
    form_class = SesionForm
    template_name = 'Moderador/sesion.html'
    success_url = reverse_lazy('benchmarking:index')

class Form_Idea(CreateView):
    model = Idea
    form_class = IdeaForm
    template_name = 'Experto/idea_form.html'
    success_url = reverse_lazy('benchmarking:list_idea')

"""class List_Idea(ListView):
    model = Idea
    template_name = 'Experto/list_ideas.html'"""

"""def lista_idea(request):
    if request.method=="POST":
        if "factor_id" in request.POST:
            try:
                id_idea = request.POST['idea_id']
                idea = Idea.objects.get(pk=id_idea)
                mensaje = {"status":"True","factor_id":idea.id}
                idea.delete() # Elinamos objeto de la base de datos
                return HttpResponse(simplejson.dumps(mensaje),mimetype='application/json')
            except:
                mensaje = {"status":"False"}
                return HttpResponse(simplejson.dumps(mensaje),mimetype='application/json')
    return render_to_response('Experto/list_ideas.html',context_instance=RequestContext(request))"""

class Update_Idea(UpdateView):
    model = Idea
    form_class = IdeaForm
    template_name = 'Experto/idea_form.html'
    success_url = reverse_lazy('benchmarking:list_idea')

class Delete_Idea(DeleteView):
    model = Idea
    template_name = 'Experto/delete_idea.html'
    success_url = reverse_lazy('benchmarking:list_idea')

class List_Conclusiones(ListView):
    model = Conclusion
    template_name = 'Moderador/resultado_fc.html'

class Form_Conclusion(CreateView):
    model = Conclusion
    form_class = Factor_concluido
    template_name = 'Moderador/add_conclusion.html'
    success_url = reverse_lazy('benchmarking:resultado_mod')

class Update_Conclusion(UpdateView):
    model = Conclusion
    form_class = Factor_concluido
    template_name = 'Moderador/add_conclusion.html'
    success_url = reverse_lazy('benchmarking:resultado_mod')

class Delete_Conclusion(DeleteView):
    model = Conclusion
    template_name = 'Moderador/delete_conclusion.html'
    success_url = reverse_lazy('benchmarking:resultado_mod')

def view_sesion_items(request, ideas, id_sesion):
    sesion = get_object_or_404(Sesion_ideas, id=id_sesion)

    if not Sesion_ideas.objects.filter(
                    Q(id=id_sesion, lluvia_ideas__equipo_expertos=request.user)
                    | Q(id=id_sesion, lluvia_ideas__moderador=request.user)).exists():
        raise Http404(u'Usted no puede ver esta sesion')

    if request.method =='GET':
        items = sesion.ideas_sesion_lluvia.all().filter(activo=True)

        if ideas == 'mis_ideas':
            items = items.filter(cerador=request.user)

        mod = sesion.lluvia_ideas.moderador.filter(id=request.user.id).exists()

        if mod and ideas == 'desabilitadas':
            items = sesion.ideas_sesion_lluvia.all().filter(activo=False)


