from django.urls import path
from . import views

app_name = 'categorias'

urlpatterns = [
    path('', views.lista_categorias, name='lista'),
    path('nova/', views.nova_categoria, name='nova'),
    path('editar/<int:id>/', views.editar_categoria, name='editar'),
    path('excluir/<int:id>/', views.excluir_categoria, name='excluir'),
]