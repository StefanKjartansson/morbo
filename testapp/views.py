# Create your views here.

from django.views.generic.base import TemplateView


class TestView(TemplateView):
    template_name = 'testapp/index.html'

