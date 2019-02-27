from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from django.contrib.auth import login



class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    return render(request, 'clinica/home.html')