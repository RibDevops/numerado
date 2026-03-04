from django.conf import settings
from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group, Permission
# from tinymce.models import HTMLField

from django.db import models
from ckeditor.fields import RichTextField

class MyModel(models.Model):
    content = RichTextField()
    
class Om(models.Model):
    id = models.AutoField(primary_key=True)
    om = models.CharField(max_length=100, verbose_name="OM")
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): # adicionar isso
        return self.om

    class Meta:  # adicionar isso
        verbose_name = 'OM'
        verbose_name_plural = 'OMs'
        ordering = ['id']


class Divisao(models.Model):
    objects = models.Manager()
    id = models.AutoField(primary_key=True)
    fk_om = models.ForeignKey(Om, on_delete=models.PROTECT, verbose_name="OM_Divisão", null=True, blank=True)
    divisao = models.CharField(max_length=30, verbose_name="Divisão")

    create_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self): # adicionar isso
        return self.divisao
    
    class Meta:  # adicionar isso
        verbose_name = 'Divisão'
        verbose_name_plural = 'Divisões'
        ordering = ['id']

class Destino(models.Model):
    objects = models.Manager()
    id = models.AutoField(primary_key=True)
    destino = models.CharField(max_length=30, verbose_name="Destino")
    fk_om = models.ForeignKey(Om, on_delete=models.PROTECT, verbose_name="OM_Divisão", null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self): # adicionar isso
        return self.destino
    
    class Meta:  # adicionar isso
        verbose_name = 'Destino'
        verbose_name_plural = 'Destinos'
        ordering = ['id']

class Tipo(models.Model):
    objects = models.Manager()
    id = models.AutoField(primary_key=True)
    tipo_doc = models.CharField(max_length=30, verbose_name="Tipo do documento")
    create_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self): # adicionar isso
        return self.tipo_doc
    
    class Meta:  # adicionar isso
        verbose_name = 'Tipo'
        verbose_name_plural = 'Tipos'
        ordering = ['id']

class Setor(models.Model):
    objects = models.Manager()
    id = models.AutoField(primary_key=True)
    fk_divisao = models.ForeignKey(Divisao, on_delete=models.PROTECT, verbose_name="Divisão", null=True, blank=True)
    fk_user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Usuário/Setor", null=True, blank=True)
    setor = models.CharField(max_length=30, verbose_name="Setor")
    create_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):  # Personalize o método __str__
        return str(self.setor)  # Retorne o valor do campo 'setor'

    class Meta:
        verbose_name = 'Setor'
        verbose_name_plural = 'Setores'
        ordering = ['id']

class Numeracao(models.Model):
    objects = models.Manager()
    id = models.AutoField(primary_key=True)
    fk_tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE, verbose_name="Tipo do Documento")
    fk_user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Usuário", null=True, blank=True)
    fk_divisao = models.ForeignKey(Divisao, on_delete=models.PROTECT, verbose_name="Divisão", null=True, blank=True)
    fk_setor = models.ForeignKey(Setor, on_delete=models.PROTECT, verbose_name="Setor", null=True, blank=True)
    fk_destino = models.ForeignKey(
        Destino,
        on_delete=models.PROTECT,
        verbose_name="Destino",
    )  # Regra atual: um destino por registro de numeração.
    doc_despacho = RichTextField(verbose_name="Despacho", null=True, blank=True)
    # doc_destino = models.CharField(max_length=200, verbose_name="Destino", null=True, blank=True)
    # fk_ano_numeracao = models.ForeignKey(Ano_Numeracao, on_delete=models.PROTECT, verbose_name="Ano do Documento")
    doc_sigad_origem = models.CharField(max_length=200, verbose_name="SIGAD Origem", null=True, blank=True)
    doc_numero = models.IntegerField(verbose_name="Número do documento", null=True, blank=True)
    title = models.CharField(max_length=200)
    # texto = HTMLField(verbose_name="Texto", null=True, blank=True)
    texto = RichTextField(verbose_name="Texto", null=True, blank=True)
    
    create_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self): # adicionar isso
        # return self.doc_numero
        return str(self.doc_numero)
    
    class Meta:  # adicionar isso
        verbose_name = 'Número'
        verbose_name_plural = 'Números'
        ordering = ['id']
    
    def get_field_names(self):
        return [field.name for field in self._meta.get_fields()]
    def clean(self):
            # self.doc_destino = str(self.doc_desmodels.IntegerField(verbose_name="Número do documento")tino.upper())
            self.doc_sigad_origem = str(self.doc_sigad_origem.upper())

import os
from django.utils.text import slugify
import os
from django.utils.text import slugify
from datetime import datetime

# models.py (acima ou fora da classe)

def rename_anexo(instance, filename):
    ext = filename.split('.')[-1]
    tipo = slugify(instance.doc_numero.fk_tipo.tipo_doc)
    numero = f"{instance.doc_numero.doc_numero}_{tipo}"
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
    novo_nome = f"{numero}_ANEXO_{slugify(os.path.splitext(filename)[0])}_{timestamp}.{ext}"
    return f"anexos/{novo_nome}"


class Anexo(models.Model):
    id = models.AutoField(primary_key=True)
    doc_numero = models.ForeignKey(Numeracao, on_delete=models.CASCADE, related_name='anexos')
    imagem = models.ImageField(upload_to=rename_anexo)
    nome_original = models.CharField(max_length=255, blank=True)
    enviado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Anexo - Doc {self.doc_numero}"


class Encaminhamento(models.Model):
    doc_numero = models.OneToOneField(Numeracao, on_delete=models.CASCADE, related_name="encaminhamento")
    origem_divisao = models.ForeignKey(Divisao, on_delete=models.PROTECT)
    destino_setor = models.ForeignKey(Setor, on_delete=models.PROTECT)
    observacao = models.TextField(null=True, blank=True)
    encaminhado_por = models.ForeignKey(User, on_delete=models.PROTECT)
    data_envio = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Encaminhado para {self.destino_setor} - {self.doc_numero}"
