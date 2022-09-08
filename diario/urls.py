from diario import views
from django.urls import path

urlpatterns = [

    path('presencas_sessao', views.view_presencas_sessao, name='presencas_sessao'),

    path('new_cuidador',views.view_new_cuidador,name='new_cuidador'),
    path('new_dinamizador',views.view_new_dinamizador,name='new_dinamizador'),
    path('',views.view_grupos, name= 'grupos'),
    path('update_groups/<str:grupo_id>',views.update_groups, name= 'update_grupos'),
    path('delete_groups/<str:grupo_id>',views.delete_groups, name= 'delete_grupos'),

    path('update_dinamizador/<str:dinamizador_id>',views.update_dinamizador, name='update_dinamizador'),
    path('delete_dinamizador/<str:dinamizador_id>',views.delete_dinamizador, name='delete_dinamizador'),
    path('update_cuidador/<str:cuidador_id>',views.update_cuidador, name='update_cuidador'),
    path('delete_cuidador/<str:cuidador_id>',views.delete_cuidador, name='delete_cuidador'),
    path('grupo/<int:grupo_id>',views.view_grupo, name='grupo'),
    path('grupo/<int:grupo_id>/membros_grupo',views.view_membros_grupo, name='membros_grupo'),
    path('grupo/<int:grupo_id>/notas_grupo',views.view_notas_grupo, name='notas_grupo'),
    path('grupo/<int:grupo_id>/sessoes_grupo',views.view_sessoes_grupo, name='sessoes_grupo'),

    path('novo_grupo',views.view_novo_grupo, name='novo_grupo'),
    path('atribui_grupo/<int:grupo_id>/<int:cuidador_id>',views.view_atribui_grupo, name='atribui_grupo'),
    path('sem_grupo',views.view_sem_grupo, name='sem_grupo'),
    path('filtrar_grupo_para_candidato/<int:cuidador_id>',views.view_filtrar_grupo_para_candidato, name='filtrar_grupo_para_candidato'),

    path('participantes', views.view_participantes, name='participantes'),
    path('perfil/<int:participantes_id>', views.view_perfil, name='perfl'),

    path('menu_esquerda', views.view_menu_esquerda, name='menu_esquerda'),
    path('diario', views.view_diario, name='diario'),
    path('diario_participante/<int:id>', views.view_diario_participante, name='diario_participante'),
    path('diario_grupo/<int:idGrupo>', views.view_diario_grupo, name='diario_grupo'),

    path('detalhes_sessao/<int:id>', views.view_detalhes_sessao, name='detalhes_sessao'),

]