from django import forms
from .models import Usuario


class UsuarioForm(forms.ModelForm):

    senha = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )

    confirmar_senha = forms.CharField(
        label='Confirmar Senha',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )

    class Meta:

        model = Usuario

        fields = [

            'login_acesso',
            'email',
            'perfil',
            'ativo',

        ]

        widgets = {

            'login_acesso': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'email': forms.EmailInput(
                attrs={'class': 'form-control'}
            ),

            'perfil': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'ativo': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),

        }

    def clean(self):

        cleaned_data = super().clean()

        senha = cleaned_data.get('senha')
        confirmar = cleaned_data.get('confirmar_senha')

        if senha != confirmar:

            raise forms.ValidationError(
                'As senhas não conferem.'
            )

        return cleaned_data