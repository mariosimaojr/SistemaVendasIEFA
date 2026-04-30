from django import forms
from django.forms import inlineformset_factory

from .models import Venda, VendaItem


class VendaForm(forms.ModelForm):

    data_venda = forms.DateField(
        label='Data da Venda',
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date'
            }
        )
    )

    class Meta:
        model = Venda
        fields = [
            'data_venda',
            'usuario',
            'forma_pagamento',
            'observacao',
        ]

        labels = {
            'data_venda': 'Data da Venda',
            'usuario': 'Usuário',
            'forma_pagamento': 'Forma de Pagamento',
            'observacao': 'Observação',
        }

        widgets = {
            'usuario': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'forma_pagamento': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'observacao': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3
                }
            ),
        }


class VendaItemForm(forms.ModelForm):

    class Meta:
        model = VendaItem
        fields = [
            'produto',
            'quantidade',
            'preco_unitario',
        ]

        labels = {
            'produto': 'Código de Barras',
            'quantidade': 'Quantidade',
            'preco_unitario': 'Preço Unitário',
        }

        widgets = {
            'produto': forms.NumberInput(
                attrs={
                    'class': 'form-control codigo-produto-input',
                    'placeholder': 'Código do produto'
                }
            ),
            'quantidade': forms.NumberInput(
                attrs={
                    'class': 'form-control quantidade-input',
                    'placeholder': 'Qtd'
                }
            ),
            'preco_unitario': forms.NumberInput(
                attrs={
                    'class': 'form-control preco-unitario-input',
                    'step': '0.01',
                    'placeholder': 'Preço'
                }
            ),
        }

    def clean_quantidade(self):
        quantidade = self.cleaned_data.get('quantidade')
        if quantidade is None or quantidade <= 0:
            raise forms.ValidationError('Informe uma quantidade maior que zero.')
        return quantidade

    def clean_preco_unitario(self):
        preco = self.cleaned_data.get('preco_unitario')
        if preco is None or preco <= 0:
            raise forms.ValidationError('Informe um preço unitário maior que zero.')
        return preco


class BaseVendaItemFormSet(forms.BaseInlineFormSet):

    def clean(self):
        super().clean()

        tem_item = False

        for form in self.forms:
            if not hasattr(form, 'cleaned_data'):
                continue

            if form.cleaned_data.get('DELETE'):
                continue

            produto = form.cleaned_data.get('produto')
            quantidade = form.cleaned_data.get('quantidade')
            preco_unitario = form.cleaned_data.get('preco_unitario')

            linha_totalmente_vazia = not produto and not quantidade and not preco_unitario
            if linha_totalmente_vazia:
                continue

            linha_completa = produto and quantidade and preco_unitario
            if linha_completa:
                tem_item = True

        if not tem_item:
            raise forms.ValidationError('Informe pelo menos um item para a venda.')

def criar_venda_item_formset(extra=3):
    return inlineformset_factory(
        Venda,
        VendaItem,
        form=VendaItemForm,
        formset=BaseVendaItemFormSet,
        extra=extra,
        can_delete=True
    )