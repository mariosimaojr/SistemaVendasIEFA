from django import forms
from .models import FormaPagamento


class FormaPagamentoForm(forms.ModelForm):

    class Meta:
        model = FormaPagamento

        fields = [
            'descricao',
            'ativo',
        ]

        labels = {
            'descricao': 'Descrição',
            'ativo': 'Ativo',
        }

        widgets = {
            'descricao': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'ativo': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }