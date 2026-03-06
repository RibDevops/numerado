import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from sn.forms import NumeracaoForm
from sn.models import Anexo
from sn.views import gera_menu

from ..forms import AnexoForm, EncaminhamentoForm
from ..models import Destino, Divisao, Encaminhamento, Numeracao, Setor

# Fluxo principal de numeração e encaminhamento de documentos.

@login_required
def nova_numeracao(request, tipo_id):
    context = {}
    fk_tipo_value = int(tipo_id)
    ultimo_registro = None

    # 🔎 Obtemos a divisão do usuário (baseado no sobrenome)
    try:
        divisao = Divisao.objects.get(divisao=request.user.last_name)
        divisao_id = divisao.id
        setores_queryset = Setor.objects.filter(fk_divisao=divisao_id)
    except Divisao.DoesNotExist:
        divisao_id = None
        setores_queryset = Setor.objects.none()

    if request.method == 'POST':
        form = NumeracaoForm(request.POST, setores_queryset=setores_queryset)

        if form.is_valid():
            destinos_ids = [int(id) for id in request.POST.getlist('destinos') if id]

            if not destinos_ids:
                messages.error(request, 'Selecione pelo menos um destino!')
                return render(request, "sn/numeracao/nova_numeracao.html", context)

            # 📌 Obtém último número para esse tipo e divisão
            ultimo_registro = Numeracao.objects.filter(
                fk_tipo_id=fk_tipo_value,
                fk_divisao_id=divisao_id
            ).order_by('-doc_numero').first()

            doc_numero = 1 if not ultimo_registro else ultimo_registro.doc_numero + 1

            # 🎯 Salva um registro para cada destino com número sequencial
            #saved_count = 0
            try:
                with transaction.atomic():
                    for destino_id in destinos_ids:
                        numeracao = Numeracao(
                            fk_tipo_id=fk_tipo_value,
                            fk_user=request.user,
                            fk_divisao_id=divisao_id,
                            fk_setor=form.cleaned_data['fk_setor'],
                            fk_destino_id=destino_id,
                            doc_sigad_origem=form.cleaned_data['doc_sigad_origem'].upper(),
                            texto=form.cleaned_data['texto'],
                            doc_numero=doc_numero
                        )
                        print("SETOR:", form.cleaned_data.get('fk_setor'))
                        numeracao.save()
                        #doc_numero += 1
                        #saved_count += 1

                messages.success(
                    request,
                    f'Documento(s) cadastrado(s) com sucesso! Número: {doc_numero}'
                    # f'Documento(s) cadastrado(s) com sucesso! Número: {doc_numero - saved_count} a {doc_numero - 1}'
                )
                return redirect('lista_numeracao', id=fk_tipo_value)

            except Exception as e:
                messages.error(request, f'Erro ao salvar documentos: {str(e)}')
        else:
            error_messages = []
            for field, errors in form.errors.items():
                field_name = form.fields[field].label if field in form.fields else field
                error_messages.append(f"{field_name}: {', '.join(errors)}")
            
            error_text = "Erro no formulário: " + " | ".join(error_messages)
            messages.error(request, error_text)
            print(f"DEBUG FORM ERRORS: {form.errors}")

    else:
        # 📄 Inicializa o formulário na primeira carga (GET)
        ultimo_registro = Numeracao.objects.filter(
            fk_tipo_id=fk_tipo_value,
            fk_divisao_id=divisao_id
        ).order_by('-doc_numero').first()

        initial_data = {
            'fk_tipo': fk_tipo_value,
            'fk_user': request.user.pk,
            'fk_divisao': divisao_id
        }

        form = NumeracaoForm(initial=initial_data, setores_queryset=setores_queryset)

    # 🔄 Atualiza contexto com form e lista de destinos
    context.update({
        'form': form,
        'tipo_id': tipo_id,
        'ultimo_registro': ultimo_registro,
        'destinos': Destino.objects.all()
    })
    context.update(gera_menu())

    return render(request, "sn/numeracao/nova_numeracao.html", context)

@login_required
def editar_numeracao(request, id):
    numeracao = get_object_or_404(Numeracao, id=id)

    if request.method == 'POST':
        form = NumeracaoForm(request.POST, instance=numeracao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro atualizado com sucesso.')
            return redirect('lista_numeracao', id=numeracao.fk_tipo_id)
    else:
        # form = SetorForm(instance=numeracao)
        tipo = Numeracao.objects.get(id=id)
        #print(f'tipo - {tipo}')
        initial_data = {'fk_tipo': tipo.fk_tipo, 'fk_user': request.user.pk, 'doc_numero': tipo.doc_numero}
        # form = NumeracaoForm(request.POST or None, initial=initial_data)
        form = NumeracaoForm(instance=numeracao, initial=initial_data)

    context = {
        'form': form,
        'numeracao': numeracao
    }
    return render(request, 'sn/numeracao/editar_numeracao.html', context)

def delete_numeracao(request, id):
    # Verifica se o registro existe antes de tentar excluí-lo
    numero = get_object_or_404(Numeracao, id=id)

    if request.method == 'POST':
        # Confirmação de exclusão do registro
        numero.delete()
        messages.success(request, 'Registro excluído com sucesso.')
        # return redirect('lista_tipo', id=tipo.fk_tipo_id)
        # return redirect('lista_numeracao')
        return redirect('lista_numeracao', id=numero.fk_tipo_id)
    
    # Caso o método da requisição seja GET, mostra o template de confirmação de exclusão
    #print(f'id_numero: {numero.id}')
    #print(f'id_numero: {numero.fk_tipo_id}')
    context = {
        'id': numero.fk_tipo_id,
        'numero': numero.id
    }
    return render(request, 'sn/numeracao/delete_numeracao.html', context)

# def lista_numeracao(request, id):
#     tipo_id = id
#     #print(f'tipo_id - {tipo_id}')
    
#     # Obter o último nome do usuário logado
#     user_last_name = request.user.last_name
#     #print(f'divisao do militar- {user_last_name}')
    
#     # Encontrar o ID da Divisao que corresponde ao último nome do usuário
#     try:
#         divisao = Divisao.objects.get(divisao=user_last_name)
#         divisao_id = divisao.id
        
#     except Divisao.DoesNotExist:
#         divisao_id = None  # Ou qualquer outro tratamento de exceção que desejar

#     # Filtrar o queryset usando o divisao_id
#     #print(f'divisao_id - {divisao_id}')
#    # Garantir que divisao_id seja um valor válido
#     if divisao_id:
#         dataset = Numeracao.objects.filter(fk_tipo_id=id, fk_divisao_id=divisao_id).order_by('-id')
#     else:
#         dataset = Numeracao.objects.none()  # Define um queryset vazio

#     for item in dataset:
#         item.create_year = item.create_at.year
#         item.create_date = item.create_at.strftime('%d/%M/%Y')

#         #print(item.create_year)
#         #print(item.create_date)

#     #print(f'dataset - {dataset}')
#     # Organiza anexos por (doc_numero, tipo_id)
#     anexos_map = defaultdict(list)
#     for anexo in Anexo.objects.filter(tipo_id=id):
#         key = (anexo.doc_numero, anexo.tipo_id)
#         anexos_map[key].append(anexo)

#     context = {
#         'user': request.user,  # Passando o usuário logado para o template
#         "dataset": dataset,
#         "tipo_id": id,
#         "anexos_map": anexos_map,
        
#     }
#     context.update(gera_menu())  # Mescla o contexto existente com o menu
#     return render(request, "sn/numeracao/lista_numeracao.html", context)

from django.db.models import Q
from sn.models import Encaminhamento

# def lista_numeracao(request, id):
#     tipo_id = id
#     user = request.user

#     # Descobre a divisão do usuário com base no sobrenome
#     divisao_id = None
#     try:
#         divisao = Divisao.objects.get(divisao=user.last_name)
#         divisao_id = divisao.id
#     except Divisao.DoesNotExist:
#         pass

#     # Descobre setor do usuário
#     setor_user = getattr(user, 'setor', None)
#     # print(divisao)

#     # Consulta documentos da divisão OU encaminhados para o setor
#     dataset = Numeracao.objects.filter(
#         Q(fk_tipo_id=tipo_id) &
#         (
#             Q(fk_divisao_id=divisao_id) |
#             Q(encaminhamento__destino_setor=setor_user)
#         )
#     ).distinct().order_by('-id')

#     # Formatando campos auxiliares
#     for item in dataset:
#         item.create_year = item.create_at.year
#         item.create_date = item.create_at.strftime('%d/%m/%Y')

#     # Mapeando anexos
#     anexos_map = defaultdict(list)
#     for anexo in Anexo.objects.filter(tipo_id=tipo_id):
#         key = (anexo.doc_numero, anexo.tipo_id)
#         anexos_map[key].append(anexo)

#     context = {
#         'user': user,
#         'dataset': dataset,
#         'tipo_id': tipo_id,
#         'anexos_map': anexos_map,
#         'divisao_nome': divisao.divisao,
#         # 'encaminhado_por': encaminhado_por,
#     }
#     context.update(gera_menu())
#     return render(request, "sn/numeracao/lista_numeracao.html", context)

@login_required
def lista_numeracao(request, id):
    tipo_id = id
    user = request.user

    # Obter a divisão e setor do usuário atual
    divisao_user = Divisao.objects.filter(divisao=user.last_name).first()
    setor_user = Setor.objects.filter(fk_user=user).first()

    # Busca todos os documentos do tipo
    documentos = Numeracao.objects.filter(fk_tipo_id=tipo_id).order_by('-id')

    # Filtragem por regras:
    docs_visiveis = []

    for doc in documentos:
        encaminhado = getattr(doc, 'encaminhamento', None)

        if not encaminhado:
            # Documento ainda não encaminhado → só visível para a divisão de origem
            if doc.fk_divisao == divisao_user:
                docs_visiveis.append(doc)

        else:
            # Documento encaminhado
            if doc.fk_divisao == divisao_user:
                docs_visiveis.append(doc)  # a divisão de origem sempre vê (sem ações)
            elif encaminhado.destino_setor == setor_user:
                docs_visiveis.append(doc)  # setor de destino vê (com ações)

    # Mapear os anexos como você já fazia
    # anexos_map = defaultdict(list)
    anexos_map = {}
    for anexo in Anexo.objects.select_related('doc_numero__fk_tipo', 'doc_numero__fk_divisao'):
        chave = (
            anexo.doc_numero.doc_numero,
            anexo.doc_numero.fk_tipo_id,
            anexo.doc_numero.fk_divisao_id
        )
        anexos_map.setdefault(chave, []).append(anexo)


    context = {
        "user": user,
        "tipo_id": tipo_id,
        "dataset": docs_visiveis,
        "anexos_map": anexos_map,
    }
    context.update(gera_menu())
    return render(request, "sn/numeracao/lista_numeracao.html", context)



@login_required
def adicionar_anexo(request, id):
    """Adiciona anexo ao documento selecionado pelo ID único."""
    documento = get_object_or_404(Numeracao, id=id)
    tipo_id = documento.fk_tipo_id

    if request.method == 'POST':
        form = AnexoForm(request.POST, request.FILES)
        if form.is_valid():
            anexo = form.save(commit=False)
            anexo.doc_numero = documento
            anexo.nome_original = form.cleaned_data['imagem'].name
            anexo.save()
            messages.success(request, "Anexo enviado com sucesso.")
            return redirect('lista_numeracao', tipo_id)
    else:
        form = AnexoForm()

    return render(request, 'sn/anexos/adicionar_anexo.html', {
        'form': form,
        'numeracao': documento,
        'tipo_id': tipo_id,
    })





@login_required
def excluir_anexo(request, id):
    anexo = get_object_or_404(Anexo, id=id)

    # Remove também o arquivo físico do anexo para não deixar órfãos em disco.
    if anexo.imagem:
        caminho = os.path.join(settings.MEDIA_ROOT, anexo.imagem.name)
        if os.path.exists(caminho):
            os.remove(caminho)

    anexo.delete()
    messages.success(request, "Anexo excluído com sucesso.")
    return redirect('lista_numeracao', anexo.doc_numero.fk_tipo.id)

@login_required
def encaminhar_documento(request, id):
    """Encaminha documento para um setor, registrando origem e usuário remetente."""
    documento = get_object_or_404(Numeracao, id=id)

    if request.method == 'POST':
        form = EncaminhamentoForm(request.POST)
        if form.is_valid():
            encaminhamento = form.save(commit=False)
            encaminhamento.doc_numero = documento
            encaminhamento.origem_divisao = documento.fk_divisao
            encaminhamento.destino_setor = form.cleaned_data['destino_setor']
            encaminhamento.observacao = form.cleaned_data['observacao']
            encaminhamento.encaminhado_por = request.user
            encaminhamento.save()

            messages.success(request, 'Documento encaminhado com sucesso.')
            return redirect('lista_numeracao', documento.fk_tipo.id)
    else:
        form = EncaminhamentoForm()

    return render(request, 'sn/numeracao/encaminhar_documento.html', {
        'form': form,
        'documento': documento
    })



@login_required
def devolver_documento(request, id):
    """Remove encaminhamento quando o setor de destino devolve o documento."""
    encaminhamento = get_object_or_404(Encaminhamento, doc_numero_id=id)
    if encaminhamento.destino_setor.fk_user == request.user:
        tipo_id = encaminhamento.doc_numero.fk_tipo.id
        encaminhamento.delete()
        messages.success(request, "Documento devolvido com sucesso.")
    else:
        tipo_id = encaminhamento.doc_numero.fk_tipo.id
        messages.error(request, "Você não tem permissão para devolver este documento.")
    return redirect('lista_numeracao', tipo_id)
