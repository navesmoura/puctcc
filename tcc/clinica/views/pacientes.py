from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.http import HttpResponseRedirect
from django.contrib.auth import login

from tcc import urls

from django.views.generic import CreateView

from django.shortcuts import render, redirect, get_object_or_404
from clinica.decorators import paciente_required


from ..models import  User,Consulta,Paciente,ConfirmaConsulta,ExameSolicitado
from ..forms import PacienteSignUpForm,ConfirmaConsultaForm,resultadoExameForm
import datetime
from django.forms import ModelForm

from clinica.decorators import medico_required


@method_decorator([csrf_exempt], name='dispatch')
class PacienteSignUpView(CreateView):
    model = User
    form_class = PacienteSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'paciente'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')




@paciente_required
def marcarconsulta(request, template_name='paciente/consultas_disponiveis_list.html'):
    consultasDisponiveis =Consulta.objects.filter(
                            situacaoConsulta='D',
                            dtHoraInicial__gt = datetime.date.today()) #todas as consultas para o futuro - qualquer medico
    data = {}
    data['object_list'] = consultasDisponiveis
    return render(request, template_name, data)



@paciente_required
def paciente_consultas_list(request, template_name='paciente/consultas_agendadas_list.html'):

    pacienteAtual= Paciente.objects.get(user=request.user)

    consultasAgendadas =Consulta.objects.filter(situacaoConsulta='A',
                                                paciente=pacienteAtual,
                                                dtHoraInicial__gt = datetime.date.today()) #todas as consultas para o futuro - qualquer medico
    data = {}
    data['object_list'] = consultasAgendadas
    return render(request, template_name, data)




@paciente_required
def pacienteConfirmaConsulta(request, pk, template_name='paciente/paciente_consulta_form.html'):
    consultaAtual = get_object_or_404(Consulta, pk=pk)

    confirmaConsulta = ConfirmaConsulta()
    confirmaConsulta.consultaId =  consultaAtual.id
    confirmaConsulta.consultaDataHora = consultaAtual.dtHoraInicial
    confirmaConsulta.consultaMedicoNome = consultaAtual.medico.user.first_name + ' '  + consultaAtual.medico.user.last_name
    confirmaConsulta.consultaMedicoEspecialidade = consultaAtual.medico.especialidade
    confirmaConsulta.consultaEuQuero=False

    form = ConfirmaConsultaForm()
    
  
    form.initial['medico'] =confirmaConsulta.consultaMedicoNome
    form.initial['especialidade'] =  confirmaConsulta.consultaMedicoEspecialidade
    form.initial['dataHora'] =confirmaConsulta.consultaDataHora
    form.initial['consultaId'] =confirmaConsulta.consultaId
    form.initial['operacao'] ="o agendamento"
    

    if request.method == 'POST':
        form = ConfirmaConsultaForm(request.POST)

        #if form.is_valid():
        consultaAtual.situacaoConsulta = 'A'
        consultaAtual.paciente = Paciente.objects.get(user=request.user)
        consultaAtual.save()
        return redirect('paciente_consultas')
        #else:
        #    form.medico =confirmaConsulta.consultaMedicoNome
        #    form.especialidade = confirmaConsulta.consultaMedicoEspecialidade
        #    form.dataHora =confirmaConsulta.consultaDataHora
        #    form.consultaId = confirmaConsulta.consultaId
    

    return render(request, 'paciente/paciente_consulta_form.html' , {'form' : form})

@paciente_required
def pacienteCancelaConsulta(request, pk, template_name='paciente/paciente_consulta_form.html'):
    consultaAtual = get_object_or_404(Consulta, pk=pk)

    confirmaConsulta = ConfirmaConsulta()
    confirmaConsulta.consultaId =  consultaAtual.id
    confirmaConsulta.consultaDataHora = consultaAtual.dtHoraInicial
    confirmaConsulta.consultaMedicoNome = consultaAtual.medico.user.first_name + ' '  + consultaAtual.medico.user.last_name
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
        consultaAtual.situacaoConsulta = 'D'
        consultaAtual.paciente = None
        consultaAtual.save()
        return redirect('paciente_consultas')
        #else:
        #    form.medico =confirmaConsulta.consultaMedicoNome
        #    form.especialidade = confirmaConsulta.consultaMedicoEspecialidade
        #    form.dataHora =confirmaConsulta.consultaDataHora
        #    form.consultaId = confirmaConsulta.consultaId
    

    return render(request, 'paciente/paciente_consulta_form.html' , {'form' : form})


@medico_required
def prontuarioPaciente(request, pk, template_name='paciente/paciente_prontuario.html'):
    pacienteAtual = get_object_or_404(Paciente, pk=pk)
    
    consulta=Consulta.objects.filter(
                            paciente=pacienteAtual,
                            situacaoConsulta='C').order_by('-dtHoraInicial')
                            
    data = {}
    data['object_list'] = consulta


    examesConcluidos = ExameSolicitado.objects.filter(
                            situacaoExame='C',
                            paciente=pacienteAtual).order_by('-dtHoraSolic')
    
    data['examesConcluidos'] = examesConcluidos

    examesPendentes =ExameSolicitado.objects.filter(
                            situacaoExame='A',
                            paciente=pacienteAtual).order_by('-dtHoraSolic')

    data['examesPendentes'] = examesPendentes
                            

    return render(request, template_name,data)

@paciente_required
def examesPaciente(request, pk, template_name='paciente/paciente_exames.html'):
    pacienteAtual = get_object_or_404(Paciente, pk=pk)
    
    
    data = {}

    examesConcluidos = ExameSolicitado.objects.filter(
                            situacaoExame='C',
                            paciente=pacienteAtual).order_by('-dtHoraSolic')
    
    data['examesConcluidos'] = examesConcluidos

    examesPendentes =ExameSolicitado.objects.filter(
                            situacaoExame='A',
                            paciente=pacienteAtual).order_by('-dtHoraSolic')

    data['examesPendentes'] = examesPendentes
                            

    return render(request, template_name,data)    


def resultadoExame(request, pk, template_name='paciente/paciente_resultado_exame.html'):
    exameSolicitado = get_object_or_404(ExameSolicitado, pk=pk)

    form = resultadoExameForm(request.POST  ,request.FILES,instance=exameSolicitado)
    #form = resultadoExameForm(request.POST or None, instance=exameSolicitado)

    if request.method == 'POST':

        if form.is_valid():
            exameSolicitado.situacaoExame = 'C'
            exameSolicitado.resultadoImagem=form.cleaned_data['resultadoImagem']
            exameSolicitado.save()
            #form.save()

            return redirect( "/exames_paciente/" +  str(exameSolicitado.paciente.user.id))

        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.

        

    return render(request, template_name, {'form':form})    

