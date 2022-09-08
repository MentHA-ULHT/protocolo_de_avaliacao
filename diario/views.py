from django.shortcuts import render, redirect
from django.forms import ModelForm, TextInput, Textarea
from .models import DinamizadorConvidado, GrupoCare, \
    GrupoCog, GrupoAvalia, Participante, Nota, Partilha, \
    Cuidador, Mentor, Informacoes, PartilhaGrupo, Respostas, Presenca, NotaGrupo,Sessao, Exercicio
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import NotaForm, PartilhaForm, CuidadorForm, GrupoForm, DinamizadorForm, PresencaForm,PartilhaGrupoForm,InformacoesForm,RespostasForm,NotaGrupoForm


# Create your views here.


###########################################################
##########          Antigo Progeto               ##########
###########################################################
def view_menu_esquerda(request):
    context = {

    }
    return render(request, "diario/menu_esquerda.html", context)

def view_participantes(request):
    contexto = {'grupos': GrupoCog.objects.all(), 'participantes': Participante.objects.all()}
    return render(request, "diario/participantes.html", contexto)

def view_new_dinamizador(request):
    form = DinamizadorForm(request.POST or None)
    if form.is_valid():
        form.save()

    contexto = {
        'dinamizador': DinamizadorConvidado.objects.all(),
        'form': form,
    }
    return render(request, "diario/new_dinamizador.html", contexto)

def update_dinamizador(request, dinamizador_id):
    dinamizador = DinamizadorConvidado.objects.get(pk=dinamizador_id)
    formDinamizador = DinamizadorForm(request.POST or None, instance=dinamizador)

    if formDinamizador.is_valid():
        formDinamizador.save()
        return HttpResponseRedirect(reverse('grupos'))

    contexto = {

        'formDinamizador': formDinamizador
    }

    return render(request, "diario/new_dinamizador.html", contexto)

def delete_dinamizador(request, dinamizador_id):
    dinamizador = DinamizadorConvidado.objects.get(pk=dinamizador_id)
    dinamizador.delete()

    return HttpResponseRedirect(reverse('grupos'))

def view_new_cuidador(request):
    form = CuidadorForm(request.POST or None)
    if form.is_valid():
        form.save()

    contexto = {
        'cuidadores': Cuidador.objects.all(),
        'form': form,
    }
    return render(request, "diario/new_cuidador.html", contexto)

def view_grupos(request):
    formGrupo = GrupoForm(request.POST or None)
    if formGrupo.is_valid():
        formGrupo.save()
        return HttpResponseRedirect(reverse('grupos'))
    contexto = {
        'grupos': GrupoCare.objects.all(),
        'cuidadores': Cuidador.objects.filter(grupoCare=None),
        'formGrupo': formGrupo
    }

    return render(request, "diario/grupos.html", contexto)

def update_groups(request, grupo_id):
    grupo = GrupoCare.objects.get(pk=grupo_id)
    formGrupo = GrupoForm(request.POST or None, instance=grupo)

    if formGrupo.is_valid():
        formGrupo.save()
        return HttpResponseRedirect(reverse('grupos'))

    contexto = {

        'formGrupo': formGrupo
    }

    return render(request, "diario/novo_grupo.html", contexto)

def delete_groups(request, grupo_id):
    grupo = GrupoCare.objects.get(pk=grupo_id)
    grupo.delete()

    return HttpResponseRedirect(reverse('grupos'))


def view_grupo(request, grupo_id):
    cuidadores = Cuidador.objects.filter(grupoCare=grupo_id)
    mentores = Mentor.objects.filter(grupoCare=grupo_id)
    dinamizadores = DinamizadorConvidado.objects.filter(grupoCare=grupo_id)

    contexto = {
        'grupo': GrupoCare.objects.get(id=grupo_id),
        'cuidadores': cuidadores,
        'mentores': mentores,
        'dinamizadores': dinamizadores,

    }
    return render(request, "diario/grupo.html", contexto)

def view_membros_grupo(request, grupo_id):
    cuidadores = Cuidador.objects.filter(grupoCare=grupo_id)
    mentores = Mentor.objects.filter(grupoCare=grupo_id)
    dinamizadores = DinamizadorConvidado.objects.filter(grupoCare=grupo_id)
    grupo = GrupoCare.objects.get(id=grupo_id)

    formDinamizador = DinamizadorForm(request.POST or None)
    if formDinamizador.is_valid():
        formDinamizador.save()
        grupo.dinamizadores.add(dinamizadores)

        return HttpResponseRedirect(reverse('grupo_id'))

    contexto = {
        'grupo': GrupoCare.objects.get(id=grupo_id),
        'cuidadores': cuidadores,
        'mentores': mentores,
        'dinamizadores': dinamizadores,
        'formDinamizador': formDinamizador
    }
    return render(request, "diario/membros_grupo.html", contexto)

def update_cuidador(request, cuidador_id):
    cuidador = Cuidador.objects.get(pk=cuidador_id)
    formCuidador = CuidadorForm(request.POST or None, instance=cuidador)

    if formCuidador.is_valid():
        formCuidador.save()
        return HttpResponseRedirect(reverse('grupos'))

    contexto = {

        'formCuidador': formCuidador
    }

    return render(request, "diario/new_cuidador.html", contexto)

def delete_cuidador(request, cuidador_id):
    cuidador = Cuidador.objects.get(pk=cuidador_id)
    cuidador.delete()

    return HttpResponseRedirect(reverse('grupos'))

def view_sessoes_grupo(request, grupo_id):
    contexto = {
        'grupo': GrupoCare.objects.get(id=grupo_id),
        #    'sessoes': SessoesCare.objects.all(grupo=grupo_id)
    }
    return render(request, "diario/sessoes_grupo.html", contexto)

def view_notas_grupo(request, grupo_id):
    contexto = {'grupo': GrupoCare.objects.get(id=grupo_id)}
    return render(request, "diario/notas_grupo.html", contexto)

def view_novo_grupo(request):
    formGrupo = GrupoForm(request.POST or None)
    if formGrupo.is_valid():
        formGrupo.save()
        return HttpResponseRedirect(reverse('grupos'))

    contexto = {'formGrupo': formGrupo}
    return render(request, "diario/novo_grupo.html", contexto)

def view_sem_grupo(request):
    contexto = {
        'cuidadores': Cuidador.objects.filter(grupoCare=None),
    }
    return render(request, "diario/sem_grupo.html", contexto)

def view_filtrar_grupo_para_candidato(request, cuidador_id):
    cuidador = Cuidador.objects.get(id=cuidador_id)

    filtrados = []

    grupos = GrupoCare.objects.all()
    lista_pesquisa = {
        'diagnostico': {grupo.diagnostico for grupo in grupos},
        'localizacao': {grupo.localizacao for grupo in grupos},
        'escolaridade': {grupo.escolaridade for grupo in grupos},
        'referenciacao': {grupo.referenciacao for grupo in grupos}
    }

    if request.POST:
        filtrados = GrupoCare.objects.all()
        for campo, valor in request.POST.items():
            if valor != '':
                if campo == 'diagnostico':
                    filtrados = filtrados.filter(diagnostico=valor)
                if campo == 'localizacao':
                    filtrados = filtrados.filter(localizacao=valor)
                if campo == 'escolaridade':
                    filtrados = filtrados.filter(escolaridade=valor)
                if campo == 'referenciacao':
                    filtrados = filtrados.filter(referenciacao=valor)

    contexto = {
        'cuidador': cuidador,
        'lista_pesquisa': lista_pesquisa,
        'grupos': filtrados,
    }
    return render(request, "diario/filtrar_grupo_para_candidato.html", contexto)

def view_atribui_grupo(request, grupo_id, cuidador_id):
    cuidador = Cuidador.objects.get(id=cuidador_id)
    grupo = GrupoCare.objects.get(id=grupo_id)
    grupo.cuidadores.add(cuidador)

    return HttpResponseRedirect(reverse('grupos'))

def view_perfil(request, participantes_id):
    contexto = {
        'participante': Participante.objects.get(id=participantes_id),

    }

    return render(request, "diario/perfil.html", contexto)

def view_diario(request):
    group_id = 1

    sessao_id = 2
    sessao = Sessao.objects.get(id=sessao_id)
    contexto = {
        'participantes': Participante.objects.filter(grupoCog=group_id),
        'grupo': GrupoCog.objects.get(id=group_id),
        'exercicios': sessao.exercicios.all(),
        'sessao': Sessao.objects.filter(id=sessao_id)
    }

    return render(request, "diario/diario.html", contexto)

def view_diario_participante(request, id):

    form = NotaForm(request.POST or None)
    if form.is_valid():
        form.save()

    form = PartilhaForm(request.POST or None)
    if form.is_valid():
        form.save()

    context = {
        'participante_id': id,
        'notas': Nota.objects.filter(participante=id).order_by('-data'),
        'partilhas': Partilha.objects.filter(participante=id).order_by('-data'),
        'informacoes': Informacoes.objects.filter(participante=id).order_by('-data'),
        'respostas': Respostas.objects.filter(participante=id).order_by('-data'),
        'notaForm': NotaForm(),
        'partilhaForm': PartilhaForm()
    }

    return render(request, "diario/diario_participante.html", context)

def view_diario_grupo(request, idGrupo):
    form = NotaGrupoForm(request.POST or None)
    if form.is_valid():
        form.save()

    form = RespostasForm(request.POST or None)
    if form.is_valid():
        form.save()


    context = {
        'participantes': Participante.objects.filter(grupoCog=idGrupo).order_by('nome'),
        'grupo_id': idGrupo,
        'notasGrupo': NotaGrupo.objects.filter(grupo=idGrupo),
        'partilhas': PartilhaGrupo.objects.filter(grupo=idGrupo),
        'informacoes': Informacoes.objects.all(),
        'respostas': Respostas.objects.all(),
        'notaForm': NotaGrupoForm(),
        'partilhaGrupoForm': PartilhaGrupoForm()

    }

    return render(request, "diario/diario_grupo.html", context)




def view_presencas_sessao(request):

    group_id = 1
    grupo = GrupoCog.objects.get(id=group_id)

    sessao_id = 2
    sessao = Sessao.objects.get(id=sessao_id)

    # unico usado é o participantes

    contexto = {
        'participantes': Participante.objects.filter(grupoCog=group_id),
        'grupo': GrupoCog.objects.get(id=group_id),
        'exercicios': sessao.exercicios.all(),
        'sessao': Sessao.objects.filter(id=sessao_id),
    }

    return render(request, "diario/presencas_sessao.html", contexto)



def view_detalhes_sessao(request,id):
    group_id = 1
    grupo = GrupoCog.objects.get(id=group_id)

    sessao_id = id
    sessao = Sessao.objects.get(id=sessao_id)



    contexto = {'grupos': GrupoCare.objects.all(),
                'exercicios': sessao.exercicios.all(),
                'sessao': Sessao.objects.filter(id=id)

                }
    return render(request, "diario/detalhes_sessao.html", contexto)
