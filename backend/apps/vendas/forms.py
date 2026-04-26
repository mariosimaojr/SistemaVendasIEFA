from decimal import Decimal

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
            'produto': 'Produto',
            'quantidade': 'Quantidade',
            'preco_unitario': 'Preço Unitário',
        }

        widgets = {
            'produto': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'quantidade': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),
            'preco_unitario': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'step': '0.01'
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

            if form.cleaned_data:
                tem_item = True

        if not tem_item:
            raise forms.ValidationError('Informe pelo menos um item para a venda.')


VendaItemFormSet = inlineformset_factory(
    Venda,
    VendaItem,
    form=VendaItemForm,
    formset=BaseVendaItemFormSet,
    extra=3,
    can_delete=True
)