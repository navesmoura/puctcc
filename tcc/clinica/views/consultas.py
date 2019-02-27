from django.contrib.auth.decorators import login_required
from ..models import  Consulta,Medico,TipoExame,ExameSolicitado

from django.http import Http404
    
import os
from django.conf import settings
from django.http import HttpResponse
from django.conf import settings




from django.utils.decorators import method_decorator
from ..decorators import medico_required

from django.views.generic import (ListView)
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django import forms

from clinica.forms import ConsultaAtendimentoForm,FinalizaConsultaForm

import datetime

import io


from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch










class ConsultasListView(ListView):
    model = Consulta
    context_object_name = 'consultas'  # your own name for the list as a template variable
    template_name = 'clinica/medicos/consultas_list.html'

    ordering = ('dtHoraInicial',)


    def get_queryset(self):
        medico = self.request.user.medico
        queryset=Consulta.objects.filter(
                            situacaoConsulta='D',
                            dtHoraInicial__gt = datetime.date.today(),
                            medico=medico)
        return queryset

#########################################################################
# a partir da aqui utilizando function base views conforme tutorial
#########################################################################


def consulta_list(request, template_name='consultas/consulta_list.html'):

    medicoAtual = Medico.objects.get(pk=request.user.id)

    consulta =Consulta.objects.filter(
                            situacaoConsulta='A',
                            dtHoraInicial__gt = datetime.date.today(),
                            medico=medicoAtual)
    data = {}
    data['object_list'] = consulta
    return render(request, template_name, data)


def consulta_view(request, pk, template_name='consultas/consulta_detail.html'):
    consulta= get_object_or_404(Consulta, pk=pk)
    return render(request, template_name, {'object':consulta})


def consulta_update(request, pk, template_name='consultas/consulta_form.html'):
    consulta=get_object_or_404(Consulta, pk=pk)

    form = ConsultaForm(request.POST or None, instance=consulta)


    if form.is_valid():
        consulta.situacaoConsulta = 'C'
        form.save()
        return redirect('consulta_list')

    return render(request, template_name, {'form':form})


@medico_required
def consulta_atendimento(request, pk, template_name='consultas/consulta_form.html'):
    consulta=get_object_or_404(Consulta, pk=pk)

    form = ConsultaAtendimentoForm(request.POST or None, instance=consulta)
    form.initial['paciente_f'] =consulta.paciente.user.get_full_name
    form.initial['medico_f'] =consulta.medico.user.get_full_name
    form.initial['pacienteId'] =consulta.paciente.user.id

    if form.is_valid():
        consulta.situacaoConsulta = 'C'
        

        for n in form['exames'].data: #Identify all even & odd numbers

            tipoExame=TipoExame.objects.get(pk=n)
            exameSolicitado = ExameSolicitado(situacaoExame="A",
                                                tipoExame=tipoExame,
                                                medico=consulta.medico,
                                                paciente=consulta.paciente,
                                                consulta=consulta,
                                                dtHoraSolic=datetime.datetime.now())
            exameSolicitado.save()           

          

        form.save()

        pdf = consulta_relatorio(consulta)

        return redirect( "/consulta_finaliza/" +  str(consulta.id))

        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.

        

    return render(request, template_name, {'form':form})    






def consultaMarcar(request, pk, template_name='paciente/paciente_consulta_form.html'):
    consulta=get_object_or_404(Consulta, pk=pk)
    form=ConsultaMarcarForm()
    form.consultaId=consulta.id
    form.nomeMedico=consulta.medico.user.first_name  + ' ' + consulta.medico.user.lastName
    form.especialidade=consulta.medico.especialidade
    form.dtHoraInicial=consulta.dtHoraInicial

    formresult= ''

    if request.method == 'POST':
        formresult= UserForm(request.POST)
        pacienteAtual = Paciente.objects.get(user=request.user)
        consulta.situacaoConsulta='A'
        consulta.paciente= pacienteAtual
        consulta.save()
        return redirect('consulta_list')


    return render(request, template_name, {'form':form})




class ConsultaMarcarForm(forms.Form):
    nomeMedico= forms.CharField(label='Médico')
    especialidade= forms.CharField(label='Especialidade')
    dtHoraInicial= forms.DateTimeField(label='Data')
    consultaId=forms.CharField(label='Numero')




class ConsultaForm(ModelForm):
    class Meta:
        model = Consulta
        fields = ['queixa']





def consulta_relatorio(consultaPdf):

    
    def cabecalhoReceita(canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Bold',16)
        canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-90,"Sistema de Gestão de Clinica Médica")                
        canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-108,"Prescrição de Medicamentos")


    def cabecalhoExames(canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Bold',16)
        canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-90,"Sistema de Gestão de Clinica Médica")                
        canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-108,"Solicitação de Exames")


    def myLaterPages(canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman',9)
        canvas.drawString(inch, 0.75 * inch, "Page %d %s" % (doc.page, pageinfo))
        canvas.restoreState()


    def receita():
        doc = SimpleDocTemplate( consultaPdf.pdfReceituario())
        Story = [Spacer(1,2*inch)]
        style = styles["Normal"]


        p = Paragraph("Medico: " + consultaPdf.medico.user.get_full_name(), style)
        Story.append(p)
        p = Paragraph("Paciente: " + consultaPdf.paciente.user.get_full_name(), style)
        Story.append(p)
        p = Paragraph("Consulta Numero: " + str(consultaPdf.id), style)
        Story.append(p)
        p = Paragraph("Data : " + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M')), style)
        Story.append(p)

        p = Paragraph("<br />\n <br />\n", style)
        Story.append(p)


        p = Paragraph("Prescrição: ", style)
        Story.append(p)

        p = Paragraph("<br />\n", style)
        Story.append(p)

        p = Paragraph(consultaPdf.receituario.replace('\n','<br />\n'), style)
        Story.append(p)
        Story.append(Spacer(1,0.2*inch))
        

        p = Paragraph("________________________________________<br />\n" + consultaPdf.medico.user.get_full_name(), style)
        Story.append(p)
        Story.append(Spacer(1,0.2*inch))
        
        doc.build(Story, onFirstPage=cabecalhoReceita, onLaterPages=myLaterPages)



    def exames():
        doc = SimpleDocTemplate(consultaPdf.pdfExames())
        Story = [Spacer(1,2*inch)]
        style = styles["Normal"]


        p = Paragraph("Medico: " + consultaPdf.medico.user.get_full_name(), style)
        Story.append(p)
        p = Paragraph("Paciente: " + consultaPdf.paciente.user.get_full_name(), style)
        Story.append(p)
        p = Paragraph("Consulta Numero: " + str(consultaPdf.id), style)
        Story.append(p)
        p = Paragraph("Data : " + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M')), style)
        Story.append(p)



        _exameSolicitado =  ExameSolicitado.objects.all().filter(consulta=consultaPdf)
        

        p = Paragraph("<br />\n <br />\n", style)
        Story.append(p)


        p = Paragraph("Exames Solicitados : ", style)
        Story.append(p)

        p = Paragraph("<br />\n", style)
        Story.append(p)



        for exameSolicitado in _exameSolicitado:
            p = Paragraph(exameSolicitado.tipoExame.descricao, style)
            Story.append(p)
            
        
        
        p = Paragraph("<br />\n <br />\n", style)
        Story.append(p)


        p = Paragraph("________________________________________<br />\n" + consultaPdf.medico.user.get_full_name(), style)
        Story.append(p)
        Story.append(Spacer(1,0.2*inch))
        doc.build(Story, onFirstPage=cabecalhoExames, onLaterPages=myLaterPages)

    PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
    styles = getSampleStyleSheet()
    receita()
    exames()


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
        form = ConfirmaConsultaForm()

        #if form.is_valid():
        consultaAtual.situacaoConsulta = 'A'
        consultaAtual.paciente = Paciente.objects.get(user=request.user)
        consultaAtual.save()
        return redirect('paciente_consultas')
        
    

    return render(request, 'paciente/paciente_consulta_form.html' , {'form' : form})


@medico_required
def consultaFinaliza(request,pk):
    
    template_name='consultas/consulta_finaliza.html'
    consulta=get_object_or_404(Consulta, pk=pk)
    form = FinalizaConsultaForm()
    form.initial['consultaId'] =consulta.id
    form.initial['pdfReceituario'] =consulta.pdfReceituario
    form.initial['pdfExames'] =consulta.pdfExames


    
    return render(request, template_name, {'form':form})

@medico_required
def retornaArquivo(request,arquivo):

    file_path = settings.PDF_PATH + arquivo
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404(file_path + " * " + arquivo)
    

@login_required
def retornaExame(request,arquivo):

    arquivo= "exames/" + arquivo
    file_path = os.path.join(settings.MEDIA_ROOT, arquivo)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="image/jpeg")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404(file_path + " * " + arquivo)


    

