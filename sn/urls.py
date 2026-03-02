from django import views
from django.urls import path, include
from .views.views_setor import *
from .views.views_tipo import *
from .views.views_home import *
from .views.views_numeracao import *
from .views.views_div import *
from .views.views_grafico import *
from .views.views_pdf import *
from .views.views_destinos import *
from .views.views_popup import *
from .views import views_grafico
from django.conf import settings
from django.conf.urls.static import static
# from .views import listar_anos, gerar_graficos

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    

    path('lista_tipo/', lista_tipo, name="lista_tipo"),
    path('delete_tipo/<int:id>/', delete_tipo, name='delete_tipo'),
    path('editar_tipo/<int:id>/', editar_tipo, name='editar_tipo'),
    path('novo_tipo/', novo_tipo, name="novo_tipo"),

    path('lista_setor/', lista_setor, name="lista_setor"),
    path('novo_setor/', novo_setor, name="novo_setor"),
    path('editar_setor/<int:id>/', editar_setor, name='editar_setor'),     
    path('delete_setor/<int:id>/', delete_setor, name='delete_setor'),     

    path('lista_numeracao/<int:id>/', lista_numeracao, name='lista_numeracao'),
    path('nova_numeracao/<tipo_id>', nova_numeracao, name="nova_numeracao"),
    # path('cadastrar_number/', cadastrar_number, name="cadastrar_number"),
    
    path('editar_numeracao/<int:id>/', editar_numeracao, name='editar_numeracao'),
    path('delete_numeracao/<int:id>/', delete_numeracao, name='delete_numeracao'),

    path('lista_divisao/', lista_divisao, name="lista_divisao"),
    path('nova_divisao/', nova_divisao, name="nova_divisao"),
    path('editar_divisao/<int:id>/', editar_divisao, name='editar_divisao'),     
    path('delete_divisao/<int:id>/', delete_divisao, name='delete_divisao'),

    path('lista_destino/', lista_destino, name="lista_destino"),
    path('novo_destino/', novo_destino, name="novo_destino"),
    path('editar_destino/<int:id>/', editar_destino, name='editar_destino'),     
    path('delete_destino/<int:id>/', delete_destino, name='delete_destino'),

    # path('graficos/', gerar_graficos, name='gerar_graficos'),

    path('anos/', listar_anos, name='listar_anos'),
    path('graficos/<int:ano>/', gerar_graficos, name='gerar_graficos'),
    # path('graficos/', views_grafico.gerar_graficos, name='graficos'),

    path('generate_pdf/<int:id>/', generate_pdf, name='generate_pdf'),

    path('ckeditor/', include('ckeditor_uploader.urls')),
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    path('add_destino_popup/', add_destino_popup, name='add_destino_popup'),

    # path('anexo/<int:id>/', adicionar_anexo, name='adicionar_anexo'),
    path('anexo/<int:tipo_id>/<int:doc_numero>/', adicionar_anexo, name='adicionar_anexo'),

    path('excluir_anexo/<int:id>/', excluir_anexo, name='excluir_anexo'),
    path('encaminhar_documento/<int:id>/', encaminhar_documento, name='encaminhar_documento'),
    path('devolver_documento/<int:id>/', devolver_documento, name='devolver_documento'),




]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

