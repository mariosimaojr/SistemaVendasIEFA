# apps/relatorios/urls.py
from django.urls import path
from . import views

app_name = 'relatorios'

urlpatterns = [

    path(
        '',
        views.lista,
        name='lista'
    ),

    path(
        'codigo-barras/',
        views.codigo_barras,
        name='codigo_barras'
    ),

    path(
        'vendas-forma-pagamento/',
        views.vendas_forma_pagamento,
        name='vendas_forma_pagamento'
    ),

]