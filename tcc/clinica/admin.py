from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Medicamento,Paciente
from clinica.forms import PacienteSignUpForm

class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ('nomeComercial', 'nomeGenerico')

class MyUserAdmin(admin.ModelAdmin):
	list_display = ('email','first_name', 'last_name','is_active')

	fields = ('email','first_name', 'last_name', 'is_active')
	actions = ['change']
	

	
	
admin.site.register(Medicamento,MedicamentoAdmin)
admin.site.register(User,MyUserAdmin)