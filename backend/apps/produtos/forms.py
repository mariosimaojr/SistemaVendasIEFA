from django import forms
from .models import Produto


class ProdutoForm(forms.ModelForm):

    class Meta:
        model = Produto
        fields = [
            'nome',
            'descricao',
            'categoria',
            'preco_venda',
            'ativo',
        ]

        labels = {
            'nome': 'Nome',
            'descricao': 'Descrição',
            'categoria': 'Categoria',
            'preco_venda': 'Preço de Venda',
            'ativo': 'Ativo',
        }

        widgets = {
            'nome': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'descricao': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4
                }
            ),
            'categoria': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'preco_venda': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'step': '0.01'
                }
            ),
            'ativo': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }