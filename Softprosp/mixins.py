from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class LoginRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

import json
from django.http.response import HttpResponse


class JSONResponseMixin(object):

    def render_to_response(self, context, **response_kwargs):
        return HttpResponse(json.dumps(response_kwargs.pop('data')), content_type='application/json', **response_kwargs)


class AjaxFormMixin(object):
    def get_errors(self):
        return self.errors.items()