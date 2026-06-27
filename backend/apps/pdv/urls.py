from django.urls import path

from . import views


app_name = 'pdv'

urlpatterns = [

    path(
        '',
        views.caixa,
        name='caixa'
    ),

    path(
        'buscar-produto/',
        views.buscar_produto,
        name='buscar_produto'
    ),
]
