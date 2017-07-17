from django.conf.urls import patterns,include, url
from Benchmarking.views import index, Form_Org, Form_Actividad, Form_Estudio, Form_Sesion, Form_Idea, \
    Update_Idea, Delete_Idea, List_Conclusiones, Form_Conclusion, Update_Conclusion,Delete_Conclusion, lista_idea

"""List_Idea"""

urlpatterns = patterns('',
    url(r'^$', index, name='index'),
    url(r'^add_actividad/$', Form_Actividad.as_view(), name= 'form_actividad'),
    url(r'^organizacion/$', Form_Org.as_view(), name='form_org'),
    url(r'^estudio/$', Form_Estudio.as_view(), name='form_estudio'),
    url(r'^sesion/$', Form_Sesion.as_view(), name='form_sesion'),
    url(r'^list_ideas/$', lista_idea, name='list_idea'),
    url(r'^idea/$', Form_Idea.as_view(), name='form_idea'),
    url(r'^editar_idea/(?P<pk>\d+)/$', Update_Idea.as_view(), name='editar_idea'),
    url(r'^eliminar_idea/(?P<pk>\d+)/$', Delete_Idea.as_view(), name='eliminar_idea'),
    url(r'^resultado_idea_mod/$', List_Conclusiones.as_view(), name='resultado_mod'),
    url(r'^concluir/$', Form_Conclusion.as_view(), name='conclusion'),
    url(r'^editar_conclusion/(?P<pk>\d+)/$', Update_Conclusion.as_view(), name='editar_conclusion'),
    url(r'^eliminar_conclusion/(?P<pk>\d+)/$', Delete_Conclusion.as_view(), name='eliminar_conclusion'),

)

"""url(r'^list_ideas/$', List_Idea.as_view(), name='list_idea'),"""