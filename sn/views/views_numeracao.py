from django.contrib.auth.decorators import login_required
from sn.forms import NumeracaoForm
from django.contrib import messages
from django.contrib.auth.models import User
from sn.views import gera_menu
from django.contrib.auth.models import User
from datetime import datetime
from django.db import transaction, connection
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from ..models import Numeracao, Divisao, Setor, Tipo
from django.http import JsonResponse

# @login_required
# def cadastrar_number(request):
#     #print(request.POST)
#     # fk_tipo_value = request.POST.get('fk_tipo')
#     fk_tipo_value = int(request.POST.get('fk_tipo'))
#     #print(fk_tipo_value)
#     # Obter o objeto Tipo com base no ID fornecido
#     tipo = get_object_or_404(Tipo, pk=fk_tipo_value)

#     # Obter o último nome do usuário logado
#     user_last_name = request.user.last_name
#     #print(f'divisao - {user_last_name}')
    
#     # Encontrar o ID da Divisao que corresponde ao último nome do usuário
#     try:
#         divisao = Divisao.objects.get(divisao=user_last_name)
#     except Divisao.DoesNotExist:
#         divisao = None  # Ou qualquer outro tratamento de exceção que desejar

#     if request.method == 'POST':
#         #print('*************************************************')
#         #print(request.POST)
#         #print('*************************************************')
#         form = NumeracaoForm(request.POST)
#         if form.is_valid():
#             #print('apos form valido')
#             #print('if form.is_valid():')
#             # Obter o usuário logado atualmente
#             user = request.user
#             # Acessar o item 'fk_tipo' do POST
            
#             doc_destino = request.POST.get('doc_destino')

#             #print(f'O tipo é: {fk_tipo_value}')
#             #print(f'Os destinos: {doc_destino}')
#             #print(request.POST.get('fk_user'))
            
#             destinos = doc_destino.split(", ")
#             #print(f'destino - {destinos}')
#             destinos_uppercase = [destino.strip().upper() for destino in destinos]
#             #print(f'destinos_uppercase - {destinos_uppercase}')

#             # Verificar se o usuário é uma instância do modelo User
#             if isinstance(user, User):
#                 with transaction.atomic():
#                     # Criar a instância de Numeracao sem salvá-la no banco de dados ainda
#                     numeracao = form.save(commit=False)
#                     numeracao.fk_user = user  # Atribuir o usuário logado ao campo fk_user

#                     # Restante do código...

#                     # Para cada destino individual, criar uma nova instância de Numeracao e salvar no banco de dados
#                     for destino in destinos_uppercase:
#                         numeracao_destino = Numeracao(
#                             fk_tipo=tipo,  # Atribuir a instância de Tipo, não o ID
#                             # fk_tipo=fk_tipo_value,
#                             fk_user=numeracao.fk_user,
#                             fk_divisao = divisao,
#                             fk_setor=numeracao.fk_setor,
#                             doc_destino=destino,
#                             doc_sigad_origem=numeracao.doc_sigad_origem,
#                             doc_numero=numeracao.doc_numero,
#                             texto=numeracao.texto
#                         )

#                         # Imprimir o SQL de inserção antes de salvar o objeto Numeracao com o destino atual no banco de dados
#                         #print('SQL de inserção para objeto Numeracao_destino:')
#                         #print(connection.queries)

#                         # Salvar o objeto Numeracao com o destino atual no banco de dados
#                         # #print(f'numeracao_destino - {numeracao_destino.fk_setor}')
#                         numeracao_destino.save()

#                 messages.add_message(request, messages.SUCCESS, 'Número(s) cadastrado(s) com sucesso')

#             else:
#                 #print('1')
#                 #print('erro:')
#                 #print(form.errors)
#                 # Caso o usuário não seja uma instância do modelo User, retorne uma mensagem de erro ou faça o tratamento adequado.
#                 messages.add_message(request, messages.ERROR, 'Erro ao cadastrar número. Usuário inválido.')
#         else:
#             #print('erro:')
#             print(form.errors)

#     else:
#         #print('2')
#         #print('erro:')
#         print(form.errors)
        
#         # form = NumeracaoForm()

#     return redirect('lista_numeracao', id=fk_tipo_value)


# @login_required
# def nova_numeracao(request):
#     context ={}
#     if request.method == 'POST':
#         fk_tipo_value = int(request.POST.get('fk_tipo'))
# #     #print(fk_tipo_value)
#         form = NumeracaoForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Registro feito com sucesso.')
#             return redirect('lista_numeracao', id=fk_tipo_value)  # Redirecione para a lista após criar
#     else:
#         # form = DestinoForm()
#         context['form']= NumeracaoForm()
#         context.update(gera_menu())  # Mescla o contexto existente com o menu
    
#     # return render(request, 'caixa/criar.html', {'form': form})
#     return render(request, 'sn/destino/novo_destino.html', context)
def nova_numeracao(request, tipo_id):
    context ={}
    fk_tipo_value = int(tipo_id)

    if request.method == 'POST':
        form = NumeracaoForm(request.POST)
        if form.is_valid():
            numeracao = form.save(commit=False)  # Don't save to the database yet
            numeracao.fk_tipo_id = fk_tipo_value  # Set fk_tipo explicitly
            numeracao.save()  # Now save the instance
            # form.save()

            messages.success(request, 'Registro feito com sucesso.')
            return redirect('lista_numeracao', id=fk_tipo_value)  # Redirecione para a lista após criar
    else:
    # Obter o último nome do usuário logado
        user_last_name = request.user.last_name
        #print(f'divisao - {user_last_name}')
        
        # Encontrar o ID da Divisao que corresponde ao último nome do usuário
        try:
            divisao = Divisao.objects.get(divisao=user_last_name)
            divisao_id = divisao.id
            print(f'divisao_id - {divisao_id}')

            setores = Setor.objects.filter(fk_divisao=divisao_id)
            # Obter os setores como uma lista de tuplas (id, valor)
            setores_choices = [(setor.id, setor.setor) for setor in setores]
            #print(f'setores_choices - {setores_choices}')

        except Divisao.DoesNotExist:
            divisao_id = None  # Ou qualquer outro tratamento de exceção que desejar
            setores_choices = []

        context = {}

        ultimo_registro = Numeracao.objects.filter(fk_tipo_id=fk_tipo_value, fk_divisao_id=divisao_id).order_by('-id').first()
        if ultimo_registro:
            ano_corrente = datetime.now().year
            ano_ultimo_registro = ultimo_registro.create_at.year

            if ano_corrente != ano_ultimo_registro:
                doc_numero = 1
            else:
                doc_numero = ultimo_registro.doc_numero + 1
        else:
            # Se não houver último registro, definimos doc_numero como 1 por padrão
            doc_numero = 1

        initial_data = {'fk_tipo': fk_tipo_value, 'fk_user': request.user.pk, 'doc_numero': doc_numero, 'fk_divisao': divisao_id}
        #print(f'request.POST - {request.POST}')
        
        form = NumeracaoForm(request.POST or None, initial=initial_data, setores_choices=setores_choices)
        
        context['form'] = form
        
        tipo_numeracao = Tipo.objects.filter(id=tipo_id)
        #print(tipo_numeracao)
        
        context.update(gera_menu())  # Mescla o contexto existente com o menu
        context['ultimo_registro'] = ultimo_registro  # Mescla o contexto existente com o menu
        context['tipo_id'] = tipo_id  # Mescla o contexto existente com o menu
        
        return render(request, "sn/numeracao/nova_numeracao.html", context)

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

def lista_numeracao(request, id):
    tipo_id = id
    #print(f'tipo_id - {tipo_id}')
    
    # Obter o último nome do usuário logado
    user_last_name = request.user.last_name
    #print(f'divisao do militar- {user_last_name}')
    
    # Encontrar o ID da Divisao que corresponde ao último nome do usuário
    try:
        divisao = Divisao.objects.get(divisao=user_last_name)
        divisao_id = divisao.id
        
    except Divisao.DoesNotExist:
        divisao_id = None  # Ou qualquer outro tratamento de exceção que desejar

    # Filtrar o queryset usando o divisao_id
    #print(f'divisao_id - {divisao_id}')
   # Garantir que divisao_id seja um valor válido
    if divisao_id:
        dataset = Numeracao.objects.filter(fk_tipo_id=id, fk_divisao_id=divisao_id).order_by('-id')
    else:
        dataset = Numeracao.objects.none()  # Define um queryset vazio

    for item in dataset:
        item.create_year = item.create_at.year
        item.create_date = item.create_at.strftime('%d/%M/%Y')

        #print(item.create_year)
        #print(item.create_date)

    #print(f'dataset - {dataset}')


    context = {
        'user': request.user,  # Passando o usuário logado para o template
        "dataset": dataset,
        "tipo_id": id,
    }
    context.update(gera_menu())  # Mescla o contexto existente com o menu

    return render(request, "sn/numeracao/lista_numeracao.html", context)





