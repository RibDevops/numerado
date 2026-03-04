from django import forms
from django.contrib.auth.models import User
from ckeditor.widgets import CKEditorWidget
from .models import Numeracao, Tipo, Divisao, Setor, Destino, Anexo, Encaminhamento

class NumeracaoForm(forms.ModelForm):
    # Definimos os campos que precisam de widgets específicos ou querysets iniciais
    fk_tipo = forms.ModelChoiceField(queryset=Tipo.objects.all(), widget=forms.HiddenInput())
    fk_user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())
    fk_divisao = forms.ModelChoiceField(queryset=Divisao.objects.all(), widget=forms.HiddenInput())
    
    texto = forms.CharField(
        label="Conteúdo do Documento",
        widget=CKEditorWidget(),
        required=False
    )
    
    doc_sigad_origem = forms.CharField(
        label="SIGAD de Origem",
        widget=forms.TextInput(attrs={
            'style': 'text-transform:uppercase',
            'class': 'form-control',
            'placeholder': 'Ex: 67102.000123/2024-00'
        })
    )

    class Meta:
        model = Numeracao
        fields = [
            "fk_setor",
            "doc_sigad_origem",
            "texto",
            "fk_user",
            "fk_divisao",
            "fk_tipo",
        ]

    def __init__(self, *args, **kwargs):
        # 1. Extraímos o queryset customizado enviado pela View
        # Usamos .pop para que o super() não receba um argumento inesperado
        setores_queryset = kwargs.pop('setores_queryset', None)
        
        super().__init__(*args, **kwargs)

        # 2. Refinamento do campo fk_setor (Filtro Dinâmico)
        if setores_queryset is not None:
            self.fields['fk_setor'].queryset = setores_queryset
        
        self.fields['fk_setor'].label = "Setor Responsável"
        self.fields['fk_setor'].empty_label = "--- Selecione o Setor ---"
        self.fields['fk_setor'].widget.attrs.update({'class': 'form-control select2'})

        # 3. Estilização em massa e segurança (Readonly para campos ocultos)
        readonly_fields = ['fk_tipo', 'fk_user', 'fk_divisao']
        for field_name in readonly_fields:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs['readonly'] = True

    def clean_doc_sigad_origem(self):
        """Garante que o SIGAD seja sempre salvo em maiúsculas (Validação de campo)"""
        dados = self.cleaned_data.get('doc_sigad_origem')
        return dados.upper() if dados else dados

class TipoForm(forms.ModelForm):
    class Meta:
        model = Tipo
        fields = ['tipo_doc']

    def __init__(self, *args, **kwargs):
        super(TipoForm, self).__init__(*args, **kwargs)
        self.fields['tipo_doc'].widget.attrs['class'] = 'form-control'

class SetorForm(forms.ModelForm):
    class Meta:
        model = Setor
        fields = ['setor', 'fk_divisao', 'fk_user']

    def __init__(self, *args, **kwargs):
        # setores_queryset = kwargs.pop('setores_queryset', Setor.objects.none())
        super().__init__(*args, **kwargs)

        # Campos ocultos
        for field in ['fk_user', 'fk_divisao']:
            self.fields[field].widget.attrs['readonly'] = True

        # Configura o campo fk_setor corretamente
        # self.fields['fk_setor'].queryset = setores_queryset
        self.fields['setor'].widget.attrs['class'] = 'form-control'

class DivisaoForm(forms.ModelForm):
    """
    Formulário para o modelo Divisão.
    """
    divisao = forms.CharField(widget=forms.TextInput(attrs={
        'style': 'text-transform:uppercase',
        'class': 'form-control'
    }))
    
    class Meta:
        model = Divisao
        fields = ['divisao', 'fk_om']

class DestinoForm(forms.ModelForm):
    class Meta:
        model = Destino
        fields = ['destino']
    
    class Media:
        js = ('js/admin_popup.js',)

    def __init__(self, *args, **kwargs):
        super(DestinoForm, self).__init__(*args, **kwargs)
        self.fields['destino'].widget.attrs['class'] = 'form-control'


class AnexoForm(forms.ModelForm):
    class Meta:
        model = Anexo
        fields = ['imagem']

    def __init__(self, *args, **kwargs):
        super(AnexoForm, self).__init__(*args, **kwargs)
        self.fields['imagem'].widget.attrs.update({'class': 'form-control'})

# class EncaminhamentoForm(forms.ModelForm):
#     class Meta:
#         model = Encaminhamento
#         fields = ['destino_setor', 'observacao']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['destino_setor'].queryset = Setor.objects.all()
#         self.fields['destino_setor'].widget.attrs.update({'class': 'form-control'})
#         self.fields['observacao'].widget.attrs.update({'class': 'form-control', 'rows': 3})

from django import forms
from sn.models import Setor, Encaminhamento

class EncaminhamentoForm(forms.ModelForm):
    destino_setor = forms.ModelChoiceField(
        queryset=Setor.objects.all(),
        label='Setor de destino',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    observacao = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        label='Observações',
        required=False
    )

    class Meta:
        model = Encaminhamento
        fields = ['destino_setor', 'observacao']
