from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group, Permission
from tinymce.models import HTMLField

from django.db import models
from ckeditor.fields import RichTextField

class MyModel(models.Model):
    content = RichTextField()

class Divisao(models.Model):
    id = models.AutoField(primary_key=True)
    divisao = models.CharField(max_length=30, verbose_name="Divisão")
    create_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self): # adicionar isso
        return self.divisao
    
    class Meta:  # adicionar isso
        verbose_name = 'Divisão'
        verbose_name_plural = 'Divisões'
        ordering = ['id']

class Destino(models.Model):
    id = models.AutoField(primary_key=True)
    destino = models.CharField(max_length=30, verbose_name="Destino")
    create_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self): # adicionar isso
        return self.destino
    
    class Meta:  # adicionar isso
        verbose_name = 'Destino'
        verbose_name_plural = 'Destinos'
        ordering = ['id']

class Tipo(models.Model):
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
    id = models.AutoField(primary_key=True)
    fk_divisao = models.ForeignKey(Divisao, on_delete=models.PROTECT, verbose_name="Divisão", null=True, blank=True)
    setor = models.CharField(max_length=30, verbose_name="Setor")
    create_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):  # Personalize o método __str__
        return str(self.setor)  # Retorne o valor do campo 'setor'

    class Meta:
        verbose_name = 'Setor'
        verbose_name_plural = 'Setores'
        ordering = ['id']

class Numeracao(models.Model):
    id = models.AutoField(primary_key=True)
    fk_tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE, verbose_name="Tipo do Documento")
    fk_user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Usuário", null=True, blank=True)
    fk_divisao = models.ForeignKey(Divisao, on_delete=models.PROTECT, verbose_name="Divisão", null=True, blank=True)
    fk_setor = models.ForeignKey(Setor, on_delete=models.PROTECT, verbose_name="Setor", null=True, blank=True)
    fk_destino = models.ForeignKey(Destino, on_delete=models.PROTECT, verbose_name="Destino")# - não pode pq e necessário colocar vários destinos
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
        verbose_name_plural = 'Numeros'
        ordering = ['id']
    
    def get_field_names(self):
        return [field.name for field in self._meta.get_fields()]
    def clean(self):
            # self.doc_destino = str(self.doc_destino.upper())
            self.doc_sigad_origem = str(self.doc_sigad_origem.upper())
