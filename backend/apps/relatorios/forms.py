from django import forms
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