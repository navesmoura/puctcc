from ..models import Consulta,ConfirmaConsulta,Paciente
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm

from django import forms










class PacienteMarcarConsultaForm(forms.ModelForm):
    class Meta:
        model = ConfirmaConsulta
        fields = ['consultaId','consultaDataHora','consultaMedicoNome','consultaMedicoEspecialidade','consultaEuQuero']



