from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from ..models import  User,Consulta,Medico,Agenda

from clinica import forms, models

from django.utils.decorators import method_decorator
from ..decorators import medico_required

from django.views.generic import (ListView)
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm

from datetime import datetime

from datetime import timedelta
from django import forms






@medico_required
def agenda_list(request, template_name='agenda/agenda_list.html'):

	

    medicoAtual = Medico.objects.get(pk=request.user.id)

    consulta =Consulta.objects.filter(
                            dtHoraInicial__gt = datetime.today(), #todas as consultas para o futuro do medico
                            medico=medicoAtual).order_by('dtHoraInicial')
				
    data = {}
    data['object_list'] = consulta
    return render(request, template_name, data)


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'

def agenda_insert(request, template_name='agenda/agenda_insert.html'):
    medicoAtual = Medico.objects.get(pk=request.user.id)
    form = AgendaForm(request.POST or None) #testando aqui
    model = Agenda
    if form.is_valid():
        try:
            
            
            DtFinal =  datetime.strptime(form.data['dtHoraFinal'],'%Y-%m-%d %H:%M')
            dtFlag  =   datetime.strptime(form.data['dtHoraInicial'],'%Y-%m-%d %H:%M')
            minutos=float(form.data['duracaoMinutos'])
            duracao =  timedelta(minutes=minutos)


            while True:
                if  ((dtFlag + duracao) > (DtFinal)):
                    break

                c = Consulta(id=None,
                            situacaoConsulta ='D',
                             dtHoraInicial=dtFlag,
                             dtHoraFinal=dtFlag + duracao,
                             medico=medicoAtual)
                c.save(ForceInsert=True)

                dtFlag = dtFlag + duracao
            print("terminou")
        except Exception as e:
            raise Exception(e)
            
                        

        return redirect('agenda_list')


    return render(request, template_name, {'form': form})


@medico_required
def agenda_insertComWidgets(request, template_name='agenda/agenda_insert_widget.html'):
    medicoAtual = Medico.objects.get(pk=request.user.id)

    agenda=Agenda()
    form = AgendaFormComWidgets(request.POST or None) #testando aqui

    if form.is_valid():
        try:
            
            dtFlag =  datetime.strptime(form.data['data'] + ' ' + form.data['horaInicial'],'%Y-%m-%d %H:%M')
            DtFinal  =   datetime.strptime(form.data['data'] + ' ' + form.data['horaFinal'],'%Y-%m-%d %H:%M')

            minutos=float(form.data['duracaoMinutos'])
            duracao =  timedelta(minutes=minutos)

            while True:
                if  ((dtFlag + duracao) > (DtFinal)):
                    break

                c = Consulta(id=None,
                            situacaoConsulta ='D',
                             dtHoraInicial=dtFlag,
                             dtHoraFinal=dtFlag + duracao,
                             medico=medicoAtual)

                c.save()

                dtFlag = dtFlag + duracao
        except Exception as e:
            print("HAHA")
            print(e)


        return redirect('agenda_list')


    return render(request, template_name, {'form': form})


    

class AgendaFormComWidgets(forms.Form):
    data = forms.DateField(widget=DateInput())
    horaInicial = forms.TimeField(initial='09:00',widget=TimeInput(),label="Hora Inicial")
    horaFinal = forms.TimeField(initial='13:00',widget=TimeInput(),label="Hora Final")
    duracaoMinutos = forms.IntegerField(initial=30,label='Duração')

    model=Agenda

    class Meta:
        fields = ['data','horaInicial','horaFinal']
        widgets = {
            'data':DateInput(),
            'horaInicial': TimeInput(),
            'horaFinal': TimeInput(),
        }



class AgendaForm(ModelForm):
    class Meta:
        model = Agenda
        fields = ['dtHoraInicial','dtHoraFinal','duracaoMinutos']



