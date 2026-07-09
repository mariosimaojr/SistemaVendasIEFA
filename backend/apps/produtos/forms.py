from django import forms

from apps.usuarios.models import Usuario

from .models import Produto


class ProdutoForm(forms.ModelForm):

    estoque_inicial = forms.IntegerField(
        label='Estoque Inicial',
        required=False,
        min_value=0,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'min': '0'
            }
        )
    )

    usuario_estoque = forms.ModelChoiceField(
        label='Usuario do Estoque',
        required=False,
        queryset=Usuario.objects.none(),
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )

    def __init__(self, *args, **kwargs):

        self.is_create = kwargs.pop('is_create', False)

        super().__init__(*args, **kwargs)

        if self.is_create:
            self.fields['usuario_estoque'].queryset = Usuario.objects.filter(
                ativo=True
            ).order_by('login_acesso')
        else:
            self.fields.pop('estoque_inicial', None)
            self.fields.pop('usuario_estoque', None)

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

    def clean_estoque_inicial(self):

        estoque_inicial = self.cleaned_data.get('estoque_inicial')

        if estoque_inicial is None:
            return 0

        return estoque_inicial

    def clean(self):

        cleaned_data = super().clean()

        if not self.is_create:
            return cleaned_data

        estoque_inicial = cleaned_data.get('estoque_inicial') or 0
        usuario_estoque = cleaned_data.get('usuario_estoque')

        if estoque_inicial > 0 and not usuario_estoque:
            self.add_error(
                'usuario_estoque',
                'Informe o usuario do estoque para registrar a entrada inicial.'
            )

        return cleaned_data
