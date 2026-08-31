from django.urls import path
from . import views

app_name = 'produtos'

urlpatterns = [

    path(
        '',
        views.lista,
        name='lista'
    ),

    path(
        'novo/',
        views.criar,
        name='novo'
    ),

    path(
        'sugerir-nome-etiqueta/',
        views.sugerir_nome_etiqueta,
        name='sugerir_nome_etiqueta'
    ),

    path(
        'editar/<int:pk>/',
        views.editar,
        name='editar'
    ),

    path(
        'excluir/<int:pk>/',
        views.excluir,
        name='excluir'
    ),

]
