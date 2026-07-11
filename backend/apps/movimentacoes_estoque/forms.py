from django import forms
from .models import MovimentacaoEstoque


class MovimentacaoEstoqueForm(forms.ModelForm):

    data_movimento = forms.DateTimeField(
        label='Data do Movimento',
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }
        )
    )

    tipo_movimento = forms.ChoiceField(
        label='Tipo de Movimento',
        choices=MovimentacaoEstoque.TIPO_MOVIMENTO_CHOICES,
        widget=forms.RadioSelect(),
        required=True
    )

    class Meta:
        model = MovimentacaoEstoque

        fields = [
            'produto',
            'quantidade',
            'data_movimento',
            'observacao',
            'tipo_movimento',
        ]

        labels = {
            'produto': 'Produto',
            'quantidade': 'Quantidade',
            'data_movimento': 'Data do Movimento',
            'observacao': 'Observacao',
            'tipo_movimento': 'Tipo de Movimento',
        }

        widgets = {
            'produto': forms.Select(
                attrs={'class': 'form-control produto-select-pesquisavel'}
            ),
            'quantidade': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),
            'observacao': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4
                }
            ),
            'tipo_movimento': forms.RadioSelect(),
        }

    def clean_quantidade(self):

        quantidade = self.cleaned_data.get('quantidade')

        if quantidade is None:
            raise forms.ValidationError('Informe a quantidade.')

        if quantidade == 0:
            raise forms.ValidationError('A quantidade deve ser maior que zero.')

        return abs(quantidade)

    def clean_observacao(self):

        observacao = self.cleaned_data.get('observacao')

        if not observacao or not observacao.strip():
            raise forms.ValidationError('Informe a observacao.')

        return observacao.strip()
