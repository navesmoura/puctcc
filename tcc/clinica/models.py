# Create your models here.
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe
from django.db.models  import DateTimeField,DurationField
from django.conf import settings


class User(AbstractUser):
    
    email = models.EmailField(unique=True)
    is_medico = models.BooleanField(default=False)
    is_paciente = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    
class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    planodeSaude = models.CharField(max_length=50)

    def nomeCompleto():
        return self.user.get_full_name
        

class Medico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    especialidade = models.CharField(max_length=50)
    ativo = models.BooleanField(default=True)

class Gestor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


class Consulta(models.Model):
    SITUACAO_CONSULTA = (
        ('D', 'Disponivel'),
        ('A', 'Agendada'),
        ('C', 'Concluida')
    )
    medico = models.ForeignKey(Medico, on_delete=models.SET_NULL, blank=True, null=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.SET_NULL, blank=True, null=True)
    situacaoConsulta = models.CharField(max_length=1, choices=SITUACAO_CONSULTA)
    dtHoraInicial = models.DateTimeField()
    dtHoraFinal = models.DateTimeField()
    queixa=models.TextField(blank=True, null=True)
    receituario=models.TextField(blank=True, null=True)
    

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('pacienteconsulta_edit', kwargs={'pk': self.pk})

    def podeCancelar(self):
        if (self.situacaoConsulta=='D'):
            return True
        else:
            return False

    def pdfReceituario(self):
        return  settings.PDF_PATH + "consulta_receita_" + str(self.id) + ".pdf"

    def pdfExames(self):
        return settings.PDF_PATH + "consulta_exames_" + str(self.id) + ".pdf"


class Agenda(models.Model):
    dtHoraInicial = models.DateTimeField(verbose_name=u"Inicio dos Atendimento", help_text=u"Informe o Horario que voce começa a Atender")
    dtHoraFinal = models.DateTimeField(verbose_name=u"Fim dos Atendimento", help_text=u"Informe o horario do Inicio da Ultima Consulta")
    intervalo = models.TimeField() #Campo descontinuado
    duracaoMinutos = models.IntegerField(blank=True, null=True,verbose_name=u"Duraçao da Consulta em Minutos", help_text=u"Informe o tempo estimado de cada consulta",default=20)
    managed = False
    
    class Meta:
        abstract = True
        managed = False
        
        

class ConfirmaConsulta(models.Model):
    consultaId = models.IntegerField(blank=True, null=True)
    consultaDataHora = models.DateTimeField(blank=True, null=True)
    consultaMedicoNome = models.CharField(max_length=100,blank=True, null=True)
    consultaMedicoEspecialidade = models.CharField(max_length=100,blank=True, null=True)
    consultaEuQuero = models.BooleanField(default=False,blank=True, null=True)
    
    
    class Meta:
        abstract = True
        managed = False
        

class TipoExame(models.Model):
    descricao = models.CharField(max_length=100)
    instrucoes = models.CharField(max_length=200)
 
    
class ExameSolicitado(models.Model):
    SITUACAO_EXAME = (
        ('A', 'Aguardando Resultado'),
        ('C', 'Concluido')
    )
    situacaoExame = models.CharField(max_length=1, choices=SITUACAO_EXAME)
    tipoExame=models.ForeignKey(TipoExame, on_delete=models.PROTECT, blank=False, null=False)
    medico = models.ForeignKey(Medico,  on_delete=models.PROTECT, blank=False, null=False)
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT, blank=False, null=False)
    dtHoraSolic = models.DateTimeField()    
    consulta= models.ForeignKey(Consulta,  on_delete=models.SET_NULL, blank=True, null=True)
    resultadoTexto = models.TextField(blank=True, null=True)
    resultadoImagem = models.ImageField(upload_to = 'exames/',blank=True, null=True)
    
    
    
class Medicamento(models.Model):
    nomeGenerico    = models.CharField(max_length=100,verbose_name="Nome Generico")
    nomeComercial   = models.CharField(max_length=100,verbose_name="Nome Comercial")
    fabricante      = models.CharField(max_length=100,verbose_name="Fabricante")


