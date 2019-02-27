from django import forms
from django.forms import ModelForm,Textarea
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from multiselectfield import MultiSelectField
from clinica.models import TipoExame,Medicamento,ExameSolicitado
from clinica.models import (Paciente, User,Medico,ConfirmaConsulta,Consulta)
from django import forms


class ConsultaAtendimentoForm(ModelForm):
    EXAMES_CHOICES = (TipoExame.objects.values_list('id', 'descricao')) 
    MEDICAMENTOS_CHOICES = Medicamento.objects.values_list('id','nomeComercial').order_by('nomeComercial') 

    exames = forms.MultipleChoiceField(choices=EXAMES_CHOICES,widget=forms.CheckboxSelectMultiple,required=False)
    medicamentos = forms.ChoiceField(choices=MEDICAMENTOS_CHOICES,required=False)
    medicamentos.widget.attrs['onchange'] = 'addReceita(this)'
    paciente_f = forms.CharField(required=False)
    medico_f = forms.CharField(required=False)
    pacienteId = forms.IntegerField(required=False)

    class Meta:
        model = Consulta
        fields = ['queixa','receituario','exames','paciente_f','medico_f','medicamentos']
        
class PacienteSignUpForm(UserCreationForm):
    planoDeSaude = forms.CharField(required=False,max_length=50,label='Plano de Saude');
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'first_name', 'last_name','planoDeSaude')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_paciente = True
        user.username = user.email
        user.save()
        paciente = Paciente.objects.create(user=user,planodeSaude=self['planoDeSaude'].data) #meu jesus
        return user


class MedicoSignUpForm(UserCreationForm):
    especialidade = forms.CharField(required=True,label='Especialidade');

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'first_name', 'last_name','especialidade')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_medico = True
        user.username = user.email      
        
        user.save()
        medico = Medico.objects.create(user=user,especialidade=self['especialidade'].data) 
        return user


class ConfirmaConsultaForm(forms.Form):
    medico = forms.CharField()
    especialidade = forms.CharField()
    dataHora = forms.DateTimeField()
    consultaId = forms.IntegerField()
    operacao = forms.CharField()


class FinalizaConsultaForm(forms.Form):
    consultaId = forms.IntegerField()
    pdfReceituario = forms.CharField()
    pdfExames = forms.CharField()
    

class resultadoExameForm(ModelForm):
    class Meta:
        model = ExameSolicitado
        fields = ['resultadoTexto','resultadoImagem']

       

