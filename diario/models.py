from django.db import models
from datetime import datetime
from django import forms
from django.conf import settings


##### Eventos ######################################

class Grupo(models.Model):
    nome = models.CharField(max_length=20)
    def __str__(self):
        return f'{self.nome}'
    class Meta:
        abstract = True

class Reference(models.Model):
    reference= models.CharField(max_length=20, default="")
    def __str__(self):
        return f'{self.reference}'


class GrupoCare(Grupo):
    opEscolaridade = (
        ("0-4", "0-4"),
        ("5-9", "5-9"),
        ("10-12", "10-12"),
        ("12+", "12+")
    )
    diagnostico = models.CharField(max_length=20, default="")
    localizacao = models.CharField(max_length=20, default="")
    escolaridade = models.CharField(max_length=20, choices=opEscolaridade, default="0-9", blank=False, null=False)
    referenciacao = models.ForeignKey(Reference, on_delete=models.CASCADE )
    def __str__(self):
        return f'{self.nome}'


class Evento(models.Model):
    data = models.DateTimeField()
    class Meta:
        abstract = True

class Sessao(Evento):
    PRESENT = 'P'
    ONLINE = 'O'
    MISTO = 'M'
    REGIME = [
        (PRESENT, "Presencial"),
        (ONLINE, "Online"),
        (MISTO,"Misto")
    ]
    PORREALIZAR = 'PR'
    REALIZADO = 'R'
    ESTADO = [
        (PORREALIZAR, "Por realizar"),
        (REALIZADO, "Realizado"),
    ]
    grupos = models.ManyToManyField(GrupoCare, blank=True, related_name='sessoes')
    estado = models.CharField(max_length=20,choices=ESTADO, null=True, blank=True,default=PORREALIZAR)
    regime = models.CharField(max_length=20,choices=REGIME, null=True, blank=True,default=PRESENT)
    numeroSessao = models.CharField(max_length=10,null=True , blank=True)
    nome = models.CharField(max_length=100)
    introducao = models.TextField(max_length=1000, null=True, blank=True)
    instrucoes = models.TextField(max_length=1000, null=True, blank=True)
    tema = models.CharField(max_length=1000, null=True, blank=True)
    dinamizadores = models.CharField(max_length=1000, null=True, blank=True)
    componentes = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f'{self.nome}'


class Doenca(models.Model):
    doenca = models.CharField(max_length=20, default="")
    def __str__(self):
        return f'{self.doenca}'

class Utilizador (models.Model):
    opSexo = (
        ("Feminino", "Feminino"),
        ("Masculino", "Masculino"),
        ("Outros", "Outros")
    )
    nome = models.CharField(max_length=100)
    sexo = models.CharField(max_length=20, choices=opSexo, default="", blank=False, null=False)
    idade = models.CharField(max_length=20, default="")
    email = models.EmailField(max_length=100, blank=True)
    nascimento = models.DateField(null=True)
    data_entrada = models.DateTimeField(auto_now_add=True, null=True)
    nacionalidade = models.CharField(max_length=20, default="")


    class Meta:
        abstract = True

class Cuidador(Utilizador):
    opEscolaridade = (
        ("0-4", "0-4"),
        ("5-9", "5-9"),
        ("10-12", "10-12"),
        ("12+", "12+")
    )

    opRegime = (
        ("Online", "Online"),
        ("Presencial", "Presencial"),
        ("Misto", "Misto")
    )
    escolaridade = models.CharField(max_length=20, choices=opEscolaridade, default="0-9", blank=False, null=False)
    referenciacao = models.ForeignKey(Reference, on_delete=models.CASCADE)
    regime = models.CharField(max_length=20, choices=opRegime, default="Online", blank=False, null=False)
    localizacao = models.CharField(max_length=20, default="")
    grupoCare = models.ManyToManyField(GrupoCare, blank=True, related_name='cuidadores')
    # blank=True permite que possa haver um cuidador sem grupo
    def __str__(self):
        return f'{self.nome}'

class Mentor(Utilizador):
    grupoCare = models.ManyToManyField(GrupoCare, blank=True, related_name='mentores')
    def __str__(self):
        return f'{self.nome}'

class DinamizadorConvidado(Utilizador):
    funcao = models.CharField(max_length=20, default="")
    grupoCare = models.ManyToManyField(GrupoCare, blank=True, related_name='dinamizadores')
    def __str__(self):
        return f'{self.nome}'


###################################  COG ########################

class GrupoCog(Grupo):
    def __str__(self):
        return f'{self.nome}'


class Facilitador(Utilizador):
    grupoCog = models.ManyToManyField(GrupoCog, blank=True, related_name='facilitadores')
    def __str__(self):
        return f'{self.nome}'


class Auxiliar(Utilizador):
    grupoCog = models.ManyToManyField(GrupoCog, blank=True, related_name='auxiliares')
    def __str__(self):
        return f'{self.nome}'

###################################  Avalia ########################

class Avaliador(Utilizador):
    def __str__(self):
        return f'{self.nome}'


class Participante(Utilizador):
    opEscolaridade = (
        ("Analfabeto", "Analfabeto"),
        ("1-4", "1-4"),
        ("5-10", "5-10"),
        ("11+", "11+")
    )
    escolaridade = models.CharField(max_length=20, choices=opEscolaridade, default="1-4", blank=False, null=False)
    diagnosticos = models.ManyToManyField(Doenca, related_name='participantes')
    referenciacao = models.ForeignKey(Reference, on_delete= models.CASCADE)
    grupoCog = models.ForeignKey(GrupoCog, on_delete=models.CASCADE, null=True, blank=True, related_name='participantes')
    cuidadores = models.ManyToManyField(Cuidador, blank=True, related_name='participantes')
    avaliador = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, default=None, blank=True, null=True)

    def __str__(self):
        return f'{self.nome}'

class Nota(models.Model):

    opTipo = (
        ("Atividades", "Atividades"),
        ("Gerais", "Gerais"),
        ("Sessão", "Sessão"),
    )

    participante = models.ForeignKey(Participante, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=opTipo, default="Gerais", blank=False, null=False)
    tituloNota = models.CharField(max_length=20, default="")
    nota = models.TextField()
    data = models.DateTimeField(auto_now_add=True, null=True)
    # podemos ter alternativamente dois campos: criado, modificado sendo o segundo atualizado se modificada a nota
    # https://stackoverflow.com/questions/1737017/django-auto-now-and-auto-now-add

    def __str__(self):
        return f'{self.nota}'


class Partilha(models.Model):
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE)
    partilha = models.TextField()
    data = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.partilha}'


class GrupoAvalia(Grupo):
    avaliador = models.ForeignKey(Avaliador, on_delete=models.CASCADE)
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.nome}'




class Presenca(Evento):
    # Possibilidade de registar o motivo de noa ter ido a sessao
    PRESENT = 'P'
    ONLINE = 'O'
    PROTOCOLO = 'PR'
    COG = 'CG'
    CARE = 'CR'
    MODES = [
        (PRESENT, "Presencial"),
        (ONLINE, "Online")
    ]
    SESSAO = [
        (PROTOCOLO, "Protocolo"),
        (COG, "Cog"),
        (CARE, "Care")
    ]
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='presencas')
    tipoSessao = models.CharField(choices=SESSAO, null=True, blank=True, default=CARE, max_length=20)
    sessao = models.ForeignKey(Sessao, on_delete=models.CASCADE, null=True, blank=True, related_name='sessao')
    # info a recolher no formulário, com checkboxes
    present = models.BooleanField(default=False)
    faltou = models.BooleanField(default=False)
    mode = models.CharField(max_length=20, choices=MODES, null=True, blank=True, default=PRESENT)
    withApp = models.BooleanField(null=True, blank=True)
    descricao = models.TextField(null=True, blank=True)


class InformacoesGrupo(models.Model):
    grupo = models.ForeignKey(GrupoCare, on_delete=models.CASCADE)
    descricao = models.TextField()
    data = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.descricao}'

class Informacoes(models.Model):
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE)
    informacoes = models.TextField()
    data = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.informacoes}'


class Respostas(models.Model):
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE)
    pergunta = models.CharField(null=True, blank=True, max_length=1)
    respostas = models.TextField()
    data = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.respostas}'

class PartilhaGrupo(models.Model):
    grupo = models.ForeignKey(GrupoCare, on_delete=models.CASCADE)
    descricao = models.TextField()
    data = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.descricao}'

class NotaGrupo(models.Model):
    grupo = models.ForeignKey(GrupoCare, on_delete=models.CASCADE, null=True)
    notaGrupo = models.TextField()
    data = models.DateTimeField(auto_now_add=True, null=True)
    # podemos ter alternativamente dois campos: criado, modificado sendo o segundo atualizado se modificada a nota
    # https://stackoverflow.com/questions/1737017/django-auto-now-and-auto-now-add

    def __str__(self):
        return f'{self.notaGrupo}'

class Exercicio(models.Model):
    INICIAL = 'I'
    DESENVOLVIMENTO = 'D'
    FINAL = 'F'
    FASE = [
        (INICIAL, "Inicial"),
        (DESENVOLVIMENTO, "Desenvolvimento"),
        (FINAL, "Final")
    ]
    nome = models.CharField(max_length=100)
    sessoes = models.ManyToManyField(Sessao, related_name='exercicios')
    materiais = models.CharField(max_length=1000, null=True, blank=True)
    fase = models.CharField(max_length=10, choices=FASE, null=True, blank=True)
    duracao = models.CharField(max_length=10,null=True, blank=True)
    atividade = models.TextField(max_length=1000, null=True, blank=True)
    objetivo = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f'{self.nome}'