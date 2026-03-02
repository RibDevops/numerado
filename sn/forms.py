from django import forms
from sn.models import *
from django.contrib.auth.models import User
from ckeditor.widgets import CKEditorWidget

class NumeracaoForm(forms.ModelForm):
    fk_tipo = forms.ModelChoiceField(queryset=Tipo.objects.all(), widget=forms.HiddenInput)
    fk_user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput)
    fk_divisao = forms.ModelChoiceField(queryset=Divisao.objects.all(), widget=forms.HiddenInput)
    texto = forms.CharField(widget=CKEditorWidget())
    doc_sigad_origem = forms.CharField(
        widget=forms.TextInput(attrs={
            'style': 'text-transform:uppercase',
            'class': 'form-control',
            'placeholder': 'SIGADAER de origem do documento'
        })
    )
    
    # Campo para o primeiro destino
    # destino_1 = forms.ModelChoiceField(
    #     queryset=Destino.objects.none(),  # Será preenchido no __init__
    #     label="Destino",
    #     widget=forms.Select(attrs={'class': 'form-control'}),
    #     required=True
    # )

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
        setores_choices = kwargs.pop('setores_choices', [])
        super(NumeracaoForm, self).__init__(*args, **kwargs)

        # Configura campos ocultos
        for field in ['fk_tipo', 'fk_user', 'fk_divisao']:
            self.fields[field].widget.attrs['readonly'] = True
        
        # Configura campo de setor dinâmico
        self.fields['fk_setor'].widget.attrs['class'] = 'form-control'
        self.fields['fk_setor'].choices = setores_choices
        
        # Configura o queryset do campo destino com todos os destinos
        # self.fields['destino_1'].queryset = Destino.objects.all()

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
        super(SetorForm, self).__init__(*args, **kwargs)
        self.fields['setor'].widget.attrs['class'] = 'form-control'
        self.fields['fk_divisao'].widget.attrs['class'] = 'form-control'
        self.fields['fk_user'].widget.attrs['class'] = 'form-control'

class DivisaoForm(forms.ModelForm):
    divisao = forms.CharField(widget=forms.TextInput(attrs={
        'style': 'text-transform:uppercase',
        'class': 'form-control'
    }))
    
    class Meta:
        model = Divisao
        fields = ['divisao']

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
