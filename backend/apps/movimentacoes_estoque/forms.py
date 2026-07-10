from django import forms
from .models import MovimentacaoEstoque


class MovimentacaoEstoqueForm(forms.ModelForm):

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
                attrs={'class': 'form-control'}
            ),
            'quantidade': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),
            'data_movimento': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local'
                }
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
