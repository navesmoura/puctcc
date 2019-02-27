
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from ..models import  User,Consulta,ConfirmaConsulta
from clinica import forms
from django.utils.decorators import method_decorator
from ..decorators import medico_required

from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django.shortcuts import  redirect, render, get_object_or_404

from ..forms import MedicoSignUpForm,ConfirmaConsultaForm

from django.urls import path








@method_decorator([csrf_exempt], name='dispatch')
class MedicoSignUpView(CreateView):
    model = User
    form_class = MedicoSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'medico'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')



@medico_required
def medicoCancelaConsulta(request, pk, template_name='paciente/paciente_consulta_form.html'):
    consultaAtual = get_object_or_404(Consulta, pk=pk)

    confirmaConsulta = ConfirmaConsulta()
    confirmaConsulta.consultaId =  consultaAtual.id
    confirmaConsulta.consultaDataHora = consultaAtual.dtHoraInicial
    confirmaConsulta.consultaMedicoNome = consultaAtual.medico.user.get_full_name
    confirmaConsulta.consultaMedicoEspecialidade = consultaAtual.medico.especialidade
    confirmaConsulta.consultaEuQuero=False

    form = ConfirmaConsultaForm()
    
  
    form.initial['medico'] =confirmaConsulta.consultaMedicoNome
    form.initial['especialidade'] =  confirmaConsulta.consultaMedicoEspecialidade
    form.initial['dataHora'] =confirmaConsulta.consultaDataHora
    form.initial['consultaId'] =confirmaConsulta.consultaId
    form.initial['operacao'] ="o cancelamento"
    

    if request.method == 'POST':
        form = ConfirmaConsultaForm(request.POST)

        #if form.is_valid():
        consultaAtual.delete()
        return redirect('agenda_list')
        #else:
        #    form.medico =confirmaConsulta.consultaMedicoNome
        #    form.especialidade = confirmaConsulta.consultaMedicoEspecialidade
        #    form.dataHora =confirmaConsulta.consultaDataHora
        #    form.consultaId = confirmaConsulta.consultaId
    

    return render(request, 'paciente/paciente_consulta_form.html' , {'form' : form})


