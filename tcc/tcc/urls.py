"""tcc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,include
from django.contrib import admin

from clinica.views import clinica,pacientes,medicos



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('clinica.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', clinica.SignUpView.as_view(), name='signup'),
    path('accounts/signup/paciente/', pacientes.PacienteSignUpView.as_view(), name='paciente_signup'),
    path('accounts/signup/medico/', medicos.MedicoSignUpView.as_view(), name='medico_signup'),

]
