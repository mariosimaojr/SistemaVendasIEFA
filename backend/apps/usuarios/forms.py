from django import forms
from .models import Usuario


class LoginForm(forms.Form):

    login_acesso = forms.CharField(
        label='Login',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'autofocus': 'autofocus'
            }
        )
    )

    senha = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )


class UsuarioForm(forms.ModelForm):

    PERFIL_CHOICES = [
        ('Administrador', 'Administrador'),
        ('Gerente', 'Gerente'),
        ('Usuário', 'Usuário'),
    ]

    perfil = forms.ChoiceField(
        label='Perfil',
        choices=PERFIL_CHOICES,
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )

    senha = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        ),
        required=False
    )

    confirmar_senha = forms.CharField(
        label='Confirmar Senha',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        ),
        required=False
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

            'ativo': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),

        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        if not self.instance or not self.instance.pk:
            self.fields['senha'].required = True
            self.fields['confirmar_senha'].required = True

    def clean(self):

        cleaned_data = super().clean()

        senha = cleaned_data.get('senha')
        confirmar = cleaned_data.get('confirmar_senha')

        if self.instance and self.instance.pk:
            if senha or confirmar:
                if senha != confirmar:
                    raise forms.ValidationError(
                        'As senhas não conferem.'
                    )
        else:
            if senha != confirmar:
                raise forms.ValidationError(
                    'As senhas não conferem.'
                )

        return cleaned_data
