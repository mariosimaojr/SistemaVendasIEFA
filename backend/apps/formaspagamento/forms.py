from django import forms
from .models import formaspagamento


class formaspagamentoForm(forms.ModelForm):

    class Meta:

        model = formaspagamento

        fields = [

            'sequencia',
            'descricao',
            'ativo',

        ]

        labels = {

            'sequencia': 'Código',
            'descricao': 'Descrição',
            'ativo': 'Ativo',

        }

        widgets = {

            'sequencia': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'descricao': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'ativo': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input'
                }
            ),

        }