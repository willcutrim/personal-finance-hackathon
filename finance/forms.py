from django import forms

from finance.models import Categoria, Lancamento, TipoChoices


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'tipo']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Ex: Alimentação, Salário...'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = user
        self.fields['tipo'].widget.attrs['class'] = 'form-select'

    def clean(self):
        cleaned_data = super().clean()
        nome = cleaned_data.get('nome')
        tipo = cleaned_data.get('tipo')
        if nome and tipo and self._user:
            qs = Categoria.objects.filter(nome__iexact=nome, tipo=tipo, user=self._user)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError(
                    f'Já existe uma categoria com este nome e tipo para sua conta.'
                )
        return cleaned_data


class LancamentoForm(forms.ModelForm):
    data = forms.DateField(
        input_formats=['%Y-%m-%d', '%d/%m/%Y'],
        widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
    )

    class Meta:
        model = Lancamento
        fields = ['descricao', 'valor', 'data', 'categoria']
        widgets = {
            'descricao': forms.TextInput(attrs={'placeholder': 'Ex: Salário, Mercado...'}),
            'valor': forms.NumberInput(attrs={'placeholder': '0,00', 'step': '0.01', 'min': '0.01'}),
        }

    def __init__(self, *args, user=None, tipo=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = user
        self._tipo = tipo
        self.fields['categoria'].widget.attrs['class'] = 'form-select'
        queryset = Categoria.objects.filter(user=user) if user is not None else Categoria.objects.none()
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        self.fields['categoria'].queryset = queryset

    def clean_valor(self):
        valor = self.cleaned_data.get('valor')
        if valor is not None and valor <= 0:
            raise forms.ValidationError('O valor deve ser maior que zero.')
        return valor


class CategoriaFilterForm(forms.Form):
    nome = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Buscar por nome...',
        }),
        label='Nome',
    )


class LancamentoFilterForm(forms.Form):
    tipo = forms.ChoiceField(
        choices=[('', 'Todos os tipos')] + list(TipoChoices.choices),
        required=False,
    )
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.none(),
        required=False,
        empty_label='Todas as categorias',
    )
    data_inicio = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='De',
    )
    data_fim = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Até',
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['categoria'].queryset = Categoria.objects.filter(user=user)
