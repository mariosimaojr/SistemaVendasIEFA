from django import forms
from django.db.models import Q
from django.utils import timezone

from apps.produtos.models import Produto


class RelatorioVendasFormaPagamentoForm(forms.Form):

    data_inicial = forms.DateField(
        label='Data Inicial',
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date'
            }
        )
    )

    data_final = forms.DateField(
        label='Data Final',
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date'
            }
        )
    )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        hoje = timezone.localdate()

        if not self.is_bound:
            self.fields['data_inicial'].initial = hoje
            self.fields['data_final'].initial = hoje

    def clean(self):

        cleaned_data = super().clean()

        data_inicial = cleaned_data.get('data_inicial')
        data_final = cleaned_data.get('data_final')

        if data_inicial and data_final and data_inicial > data_final:
            raise forms.ValidationError(
                'A data inicial não pode ser maior que a data final.'
            )

        return cleaned_data
    
class RelatorioCodigoBarrasForm(forms.Form):

    produto = forms.ModelChoiceField(
        label='Produto',
        queryset=Produto.objects.filter(ativo=True).order_by('nome'),
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )

    quantidade_etiquetas = forms.IntegerField(
        label='Quantidade de Etiquetas',
        min_value=1,
        initial=1,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'min': '1'
            }
        )
    )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        queryset = Produto.objects.filter(ativo=True)

        if self.is_bound:
            produto_id = self.data.get(self.add_prefix('produto'))

            if produto_id:
                try:
                    produto_id = int(produto_id)
                except (TypeError, ValueError):
                    produto_id = None

                if produto_id:
                    queryset = Produto.objects.filter(
                        Q(ativo=True) |
                        Q(pk=produto_id)
                    )

        self.fields['produto'].queryset = queryset.order_by('nome')
