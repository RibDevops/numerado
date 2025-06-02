from django import forms
from sn.models import *
from django import forms
from django.contrib.auth.models import User
from ckeditor.widgets import CKEditorWidget

class NumeracaoForm(forms.ModelForm):
    # fk_tipo = forms.ModelChoiceField(queryset=Tipo.objects.all(), initial=None, widget=forms.HiddenInput)
    fk_tipo = forms.ModelChoiceField(queryset=Tipo.objects.all(), widget=forms.HiddenInput)
    fk_user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput)
    fk_divisao = forms.ModelChoiceField(queryset=Divisao.objects.all(), widget=forms.HiddenInput)
    texto = forms.CharField(widget=CKEditorWidget())
   
    # doc_destino = forms.CharField(widget=forms.TextInput(attrs={'style': 'text-transform:uppercase'}))
    doc_sigad_origem = forms.CharField(widget=forms.TextInput(attrs={'style': 'text-transform:uppercase'}))

    class Meta:
        # specify model to be used
        model = Numeracao
 
        # specify fields to be used
        fields = [
            "id",
            "doc_numero",
            "fk_setor",
            "fk_destino",
            "doc_sigad_origem",
            "texto",
            "fk_user",
            "fk_divisao",
            "fk_tipo",
        ]
    
    def __init__(self, *args, **kwargs):
        setores_choices = kwargs.pop('setores_choices', [])
        super(NumeracaoForm, self).__init__(*args, **kwargs)

        self.fields['fk_tipo'].widget.attrs['readonly'] = True
        self.fields['fk_user'].widget.attrs['readonly'] = True
        self.fields['fk_divisao'].widget.attrs['readonly'] = True
        
        self.fields['doc_numero'].widget.attrs['class'] = 'form-control'
        self.fields['doc_numero'].widget.attrs['readonly'] = True
        
        self.fields['fk_setor'].widget.attrs['class'] = 'form-control'
        self.fields['fk_setor'].choices = setores_choices  # Definindo as escolhas dinamicamente

        self.fields['doc_sigad_origem'].widget.attrs['class'] = 'form-control'
        self.fields['doc_sigad_origem'].widget.attrs['placeholder'] = 'SIGADAER de origem do documento'

        self.fields['texto'].widget.attrs['class'] = 'form-control'
        
        self.fields['fk_destino'].widget.attrs['class'] = 'form-control'

        # self.fields['fk_tipo'].label = "Tipo do Documento"
        # self.fields['fk_tipo'].widget.attrs['class'] = 'form-control' 
        # self.fields['doc_destino'].widget.attrs['placeholder'] = 'Se houver mais de um destino, separe-os por vírgula e espaço ex: COMAR I, COMAR II.'

        # doc_destino = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform:uppercase'}))
        
        # self.fields['fk_user'].label = "Nome do usuário"
        # self.fields['fk_user'].widget.attrs['class'] = 'form-control'
        # self.fields['fk_user'].widget.attrs['disabled'] = True
        # self.fields['fk_user'].widget.attrs['readonly'] = True

        # self.fields['fk_divisao'].widget.attrs['readonly'] = True

        # self.fields['setor'].widget.attrs['class'] = 'form-control'
        # self.fields['setor_description'].widget.attrs['class'] = 'form-control'

        # self.fields['doc_destino'].widget.attrs['class'] = 'form-control'
        # self.fields['destino_description'].widget.attrs['class'] = 'form-control'

class TipoForm(forms.ModelForm):
    class Meta:
        model = Tipo
        fields = [
            'tipo_doc', 
            # 'tipo_sigla', 
            # 'tipo_description'
            ]

    def __init__(self, *args, **kwargs):
        super(TipoForm, self).__init__(*args, **kwargs)
        self.fields['tipo_doc'].widget.attrs['class'] = 'form-control'
        # self.fields['tipo_sigla'].widget.attrs['class'] = 'form-control'
        # self.fields['tipo_description'].widget.attrs['class'] = 'form-control'
        
class SetorForm(forms.ModelForm):

    class Meta:
        model = Setor
        # fields = ['setor', 'setor_description', 'fk_divisao']
        fields = ['setor', 'fk_divisao']

    def __init__(self, *args, **kwargs):
        super(SetorForm, self).__init__(*args, **kwargs)
        self.fields['setor'].widget.attrs['class'] = 'form-control'
        # self.fields['setor_description'].widget.attrs['class'] = 'form-control'
        self.fields['fk_divisao'].widget.attrs['class'] = 'form-control'

class DivisaoForm(forms.ModelForm):
    divisao = forms.CharField(widget=forms.TextInput(attrs={'style': 'text-transform:uppercase'}))
    class Meta:
        model = Divisao
        fields = ['divisao']

    def __init__(self, *args, **kwargs):
        super(DivisaoForm, self).__init__(*args, **kwargs)
        self.fields['divisao'].widget.attrs['class'] = 'form-control'

class DestinoForm(forms.ModelForm):
    # destino = forms.CharField(widget=forms.TextInput(attrs={'style': 'text-transform:uppercase'}))
    class Meta:
        model = Destino
        fields = ['destino']
    
    class Media:
        js = ('js/admin_popup.js',)  # Adiciona o arquivo JavaScript customizado

    def __init__(self, *args, **kwargs):
        super(DestinoForm, self).__init__(*args, **kwargs)
        self.fields['destino'].widget.attrs['class'] = 'form-control'        


