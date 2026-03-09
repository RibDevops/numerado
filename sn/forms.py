from django import forms
from django.contrib.auth.models import User
from ckeditor.widgets import CKEditorWidget
from .models import Numeracao, Tipo, Divisao, Setor, Destino, Anexo, Encaminhamento, Om

class OmForm(forms.ModelForm):
    class Meta:
        model = Om
        fields = ['om']
        widgets = {
            'om': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da OM'}),
        }

class DivisaoForm(forms.ModelForm):
    class Meta:
        model = Divisao
        fields = ['divisao', 'fk_om']
        widgets = {
            'divisao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da Divisão', 'style': 'text-transform:uppercase'}),
            'fk_om': forms.Select(attrs={'class': 'form-control select2'}),
        }

class SetorForm(forms.ModelForm):
    class Meta:
        model = Setor
        fields = ['setor', 'fk_divisao', 'fk_user']
        widgets = {
            'setor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Setor'}),
            'fk_divisao': forms.Select(attrs={'class': 'form-control select2'}),
            'fk_user': forms.Select(attrs={'class': 'form-control select2'}),
        }

class TipoForm(forms.ModelForm):
    class Meta:
        model = Tipo
        fields = ['tipo_doc']
        widgets = {
            'tipo_doc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Ofício, Memorando'}),
        }

class DestinoForm(forms.ModelForm):
    class Meta:
        model = Destino
        fields = ['destino', 'fk_om']
        widgets = {
            'destino': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Destino do documento'}),
            'fk_om': forms.Select(attrs={'class': 'form-control select2'}),
        }

class NumeracaoForm(forms.ModelForm):
    fk_tipo = forms.ModelChoiceField(queryset=Tipo.objects.all(), widget=forms.HiddenInput())
    fk_user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())
    fk_divisao = forms.ModelChoiceField(queryset=Divisao.objects.all(), widget=forms.HiddenInput())
    title = forms.CharField(
        label="Assunto/Título",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Assunto do documento'}),
        required=True
    )
    
    texto = forms.CharField(
        label="Conteúdo do Documento",
        widget=CKEditorWidget(),
        required=False
    )
    
    class Meta:
        model = Numeracao
        fields = [
            "fk_setor",
            "fk_destino",
            "doc_sigad_origem",
            "title",
            "texto",
            "doc_despacho",
            "fk_user",
            "fk_divisao",
            "fk_tipo",
        ]
        widgets = {
            'fk_setor': forms.Select(attrs={'class': 'form-control select2'}),
            'fk_destino': forms.Select(attrs={'class': 'form-control select2'}),
            'doc_sigad_origem': forms.TextInput(attrs={
                'style': 'text-transform:uppercase',
                'class': 'form-control',
                'placeholder': 'Ex: 67102.000123/2024-00'
            }),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Assunto/Título'}),
            'doc_despacho': CKEditorWidget(),
        }

    def __init__(self, *args, **kwargs):
        setores_queryset = kwargs.pop('setores_queryset', None)
        super().__init__(*args, **kwargs)

        if setores_queryset is not None:
            self.fields['fk_setor'].queryset = setores_queryset
        
        self.fields['fk_setor'].empty_label = "--- Selecione o Setor ---"

        # Readonly para campos ocultos por segurança
        for field_name in ['fk_tipo', 'fk_user', 'fk_divisao']:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs['readonly'] = True

    def clean_doc_sigad_origem(self):
        dados = self.cleaned_data.get('doc_sigad_origem')
        return dados.upper() if dados else dados

class AnexoForm(forms.ModelForm):
    class Meta:
        model = Anexo
        fields = ['imagem']
        widgets = {
            'imagem': forms.FileInput(attrs={'class': 'form-control'}),
        }

class EncaminhamentoForm(forms.ModelForm):
    class Meta:
        model = Encaminhamento
        fields = ['destino_setor', 'observacao']
        widgets = {
            'destino_setor': forms.Select(attrs={'class': 'form-control select2'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
