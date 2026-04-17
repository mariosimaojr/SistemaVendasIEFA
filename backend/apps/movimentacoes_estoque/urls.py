from django.urls import path
from . import views

app_name = 'movimentacoes_estoque'

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