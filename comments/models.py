from django.contrib.contenttypes.models import ContentType
import django_comments as comments
from django.conf import settings
from django.db import models
from django_comments.models import Comment
from .choices import CHOICES_VOTO

class CommentWithVote(Comment):
    voto = models.CharField(max_length=1,
                            choices=CHOICES_VOTO)
    def votos_item(self,item):
        comment_model = comments.get_model()
        ctype = ContentType.objects.get_for_model(item)
        commentswithvote = comment_model.objects.filter(content_type = ctype,
                                                        object_pk = item.id,
                                                        is_public = True,
                                                        is_removed = False,
                                                        site__pk = settings.SITE_ID)
        return commentswithvote

    def usuarios_votos(self,items):
        comment_model = comments.get_model()

        if items.exists():
            ctype = ContentType.objects.get_for_model(items[0])
        else:
            ctype = None

        items = items.values_list('id', flat=True)
        items = map(int, items)

        usuarios = comment_model.objects.filter(content_type = ctype,
                                                object_pk_in = items,
                                                is_public = True,
                                                is_removed = False,
                                                site__pk = settings.SITE_ID).order_by('user').distinct('user')
        return usuarios

    def is_comment(self,item,user):
        query = self.votos_item(item)
        return query.filter(user=user).first()

    def voto_comment (self):
        voto = ''
        if self.voto =='1':
            voto = 'white'
        elif self.voto == '2':
            voto = 'red'
        elif self.voto == '3':
            voto = 'lred'
        elif self.voto == '4':
            voto = 'yellow'
        elif self.voto == '5':
            voto = 'lgreen'
        elif self.voto == '6':
            voto = 'green'
        elif self.voto == '0':
            voto = 'black'

        return voto