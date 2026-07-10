import json

from django import forms

from apps.formaspagamento.models import FormaPagamento


class PdvVendaForm(forms.Form):

    forma_pagamento = forms.ModelChoiceField(
        label='Forma de Pagamento',
        queryset=FormaPagamento.objects.none(),
        widget=forms.RadioSelect(
            attrs={
                'class': 'pdv-payment-radio',
                'required': 'required',
            }
        )
    )

    itens_json = forms.CharField(
        widget=forms.HiddenInput(
            attrs={
                'id': 'id_itens_json',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['forma_pagamento'].queryset = FormaPagamento.objects.filter(
            ativo=True
        ).order_by('descricao')

    def clean_itens_json(self):
        itens_json = self.cleaned_data.get('itens_json')

        try:
            itens = json.loads(itens_json)
        except (TypeError, json.JSONDecodeError):
            raise forms.ValidationError('Os itens da venda estao invalidos.')

        if not isinstance(itens, list) or not itens:
            raise forms.ValidationError('Informe pelo menos um item para finalizar a venda.')

        itens_limpos = []

        for item in itens:
            if not isinstance(item, dict):
                raise forms.ValidationError('Os itens da venda estao invalidos.')

            produto_id = item.get('produto_id')
            quantidade = item.get('quantidade')

            try:
                produto_id = int(produto_id)
                quantidade = int(quantidade)
            except (TypeError, ValueError):
                raise forms.ValidationError('Os itens da venda estao invalidos.')

            if produto_id <= 0:
                raise forms.ValidationError('Informe um produto valido.')

            if quantidade <= 0:
                raise forms.ValidationError('A quantidade dos itens deve ser maior que zero.')

            itens_limpos.append(
                {
                    'produto_id': produto_id,
                    'quantidade': quantidade,
                }
            )

        return itens_limpos
