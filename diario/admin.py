from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(GrupoCare)
admin.site.register(Mentor)
admin.site.register(Cuidador)
admin.site.register(DinamizadorConvidado)

admin.site.register(GrupoCog)
admin.site.register(GrupoAvalia)

admin.site.register(Facilitador)
admin.site.register(Avaliador)

admin.site.register(Participante)
admin.site.register(Nota)
admin.site.register(Partilha)
admin.site.register(Reference)
admin.site.register(Doenca)
admin.site.register(Sessao)
admin.site.register(Presenca)

admin.site.register(InformacoesGrupo)
admin.site.register(Informacoes)
admin.site.register(Respostas)
admin.site.register(PartilhaGrupo)
admin.site.register(NotaGrupo)
admin.site.register(Exercicio)




