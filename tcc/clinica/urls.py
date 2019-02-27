from django.urls import include, path
from .views import clinica,consultas,agenda,pacientes,consultautil,medicos


urlpatterns = [
    path('', clinica.home, name='home'),
    path('verconsulta/', consultas.ConsultasListView.as_view(),name="consultas"),

    path('consulta/',  consultas.consulta_list, name='consulta_list'),
    path('consulta_atendimento/<int:pk>', consultas.consulta_atendimento, name='consulta_atendimento'),
    path('consulta_finaliza/<int:pk>', consultas.consultaFinaliza, name='consulta_finaliza'),
    path('prontuario_paciente/<int:pk>', pacientes.prontuarioPaciente, name='prontuario_paciente'),
    path('exames_paciente/<int:pk>', pacientes.examesPaciente, name='exames_paciente'),


    
    path('pdf/<str:arquivo>', consultas.retornaArquivo, name='consulta_arquivo'),
    path('exames/<str:arquivo>', consultas.retornaExame, name='consulta_exame'),

    path('medicoCancelaConsulta/<int:pk>', medicos.medicoCancelaConsulta, name='medicoCancelaConsulta'),
    path('agenda/',  agenda.agenda_list, name='agenda_list'),
    path('agenda/insert',  agenda.agenda_insertComWidgets, name='agenda_insert'),
    path('pacienteconsultas/',  pacientes.paciente_consultas_list, name='paciente_consultas'),
    path('marcarconsulta/',  pacientes.marcarconsulta, name='paciente_marcar_consulta'),
    path('pacienteConfirmaConsulta/<int:pk>',  pacientes.pacienteConfirmaConsulta, name='pacienteConfirmaConsulta'),
    path('pacienteCancelaConsulta/<int:pk>',  pacientes.pacienteCancelaConsulta, name='pacienteCancelaConsulta'),
    path('resultado_exame/<int:pk>',  pacientes.resultadoExame, name='resultado_exame'),

    
    


    

    

    




]

