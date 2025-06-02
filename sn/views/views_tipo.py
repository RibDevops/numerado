from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from sn.models import Tipo, Setor
from sn.forms import TipoForm
from sn.views import gera_menu
from django.contrib import messages

@login_required
def novo_tipo(request):
    context ={}
    if request.method == 'POST':
        form = TipoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro feito com sucesso.')
            return redirect('lista_tipo')  # Redirecione para a lista após criar
    else:
        # form = TipoForm()
        context['form']= TipoForm()
        context.update(gera_menu())  # Mescla o contexto existente com o menu
    
    # return render(request, 'caixa/criar.html', {'form': form})
    return render(request, 'sn/tipo/novo_tipo.html', context)

@login_required
def lista_tipo(request):
    dataset = Tipo.objects.all()
    context = {"dataset": dataset}
    context.update(gera_menu())  # Mescla o contexto existente com o menu
    return render(request, "sn/tipo/lista_tipo.html", context)

def delete_tipo(request, id):
    # Verifica se o registro existe antes de tentar excluí-lo
    tipo = get_object_or_404(Tipo, id=id)

    if request.method == 'POST':
        # Confirmação de exclusão do registro
        tipo.delete()
        messages.success(request, 'Registro excluído com sucesso.')
        # return redirect('lista_tipo', id=tipo.fk_tipo_id)
        return redirect('lista_tipo')
    
    # Caso o método da requisição seja GET, mostra o template de confirmação de exclusão
    context = {
        'tipo': tipo
    }
    return render(request, 'sn/tipo/delete_tipo.html', context)


def editar_tipo(request, id):
    tipo = get_object_or_404(Tipo, id=id)

    if request.method == 'POST':
        form = TipoForm(request.POST, instance=tipo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro atualizado com sucesso.')
            # return redirect('lista_tipo', id=tipo.fk_tipo_id)
            return redirect('lista_tipo')
    else:
        form = TipoForm(instance=tipo)

    context = {
        'form': form,
        'tipo': tipo
    }
    return render(request, 'sn/tipo/editar_tipo.html', context)
# def delete_tipo(request, id):
#     # Verifica se o registro existe antes de tentar excluí-lo
#     tipo = get_object_or_404(Tipo, id=id)

#     if request.method == 'POST':
#         # Confirmação de exclusão do registro
#         tipo.delete()
#         messages.success(request, 'Registro excluído com sucesso.')
#         return redirect('lista_tipo', id=tipo.fk_tipo_id)
    
#     # Caso o método da requisição seja GET, mostra o template de confirmação de exclusão
#     context = {
#         'tipo': tipo
#     }
#     return render(request, 'sn/delete_tipo.html', context)


# def editar_tipo(request, id):
#     tipo = get_object_or_404(Tipo, id=id)

#     if request.method == 'POST':
#         form = TipoForm(request.POST, instance=tipo)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Registro atualizado com sucesso.')
#             return redirect('lista_tipo', id=tipo.fk_tipo_id)
#     else:
#         form = TipoForm(instance=tipo)

#     context = {
#         'form': form,
#         'tipo': tipo
#     }
#     return render(request, 'sn/editar_tipo.html', context)
#     fk_tipo_value = int(request.POST.get('fk_tipo'))
#     #print(fk_tipo_value)
#     # Obter o objeto Tipo com base no ID fornecido
#     tipo = get_object_or_404(Tipo, pk=fk_tipo_value)

#     if request.method == 'POST':
#         #print('1')
#         form = TipoForm(request.POST)
#         if form.is_valid():
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
#                     # Criar a instância de Tipo sem salvá-la no banco de dados ainda
#                     tipo = form.save(commit=False)
#                     tipo.fk_user = user  # Atribuir o usuário logado ao campo fk_user

#                     # Restante do código...

#                     # Para cada destino individual, criar uma nova instância de Tipo e salvar no banco de dados
#                     for destino in destinos_uppercase:
#                         tipo_destino = Tipo(
#                             fk_tipo=tipo,  # Atribuir a instância de Tipo, não o ID
#                             # fk_tipo=fk_tipo_value,
#                             fk_user=tipo.fk_user,
#                             fk_setor=tipo.fk_setor,
#                             doc_destino=destino,
#                             doc_sigad_origem=tipo.doc_sigad_origem,
#                             doc_numero=tipo.doc_numero,
#                             texto=tipo.texto
#                         )

#                         # Imprimir o SQL de inserção antes de salvar o objeto Tipo com o destino atual no banco de dados
#                         #print('SQL de inserção para objeto Tipo_destino:')
#                         #print(connection.queries)

#                         # Salvar o objeto Tipo com o destino atual no banco de dados
#                         tipo_destino.save()

#                 messages.add_message(request, messages.SUCCESS, 'Número(s) cadastrado(s) com sucesso')

#             else:
#                 #print('1')
#                 #print('erro:')
#                 #print(form.errors)
#                 # Caso o usuário não seja uma instância do modelo User, retorne uma mensagem de erro ou faça o tratamento adequado.
#                 messages.add_message(request, messages.ERROR, 'Erro ao cadastrar número. Usuário inválido.')
#         else:
#             #print('erro:')
#             #print(form.errors)

#     else:
#         #print('2')
#         #print('erro:')
#         #print(form.errors)
        
#         # form = TipoForm()

#     return redirect('lista_tipo', id=fk_tipo_value)


# @login_required
# def nova_tipo(request, tipo_id):
#     context = {}

#     ultimo_registro = Tipo.objects.filter(fk_tipo_id=tipo_id).order_by('-id').first()
#     if ultimo_registro:
#         ano_corrente = datetime.now().year
#         ano_ultimo_registro = ultimo_registro.create_at.year

#         if ano_corrente != ano_ultimo_registro:
#             doc_numero = 1
#         else:
#             doc_numero = ultimo_registro.doc_numero + 1
#     else:
#         # Se não houver último registro, definimos doc_numero como 1 por padrão
#         doc_numero = 1

#     initial_data = {'fk_tipo': tipo_id, 'fk_user': request.user.pk, 'doc_numero': doc_numero}
#     form = TipoForm(request.POST or None, initial=initial_data)
#     ultimo_registro = None  # Define a variável como None para garantir que ela seja atribuída
#     context['form'] = form
    
#     tipo_tipo = Tipo.objects.filter(id=tipo_id)
#     #print(tipo_tipo)
    
#     context.update(gera_menu())  # Mescla o contexto existente com o menu
#     context['ultimo_registro'] = ultimo_registro  # Mescla o contexto existente com o menu
#     context['tipo_id'] = tipo_id  # Mescla o contexto existente com o menu
    
#     return render(request, "sn/nova_tipo.html", context)


# def lista_tipo(request, id):
#     tipo_id = id
#     dataset = Tipo.objects.filter(fk_tipo_id=id).order_by('-id')

#     # Define o número de itens por página
#     items_per_page = 10

#     # Cria o objeto Paginator para o queryset
#     paginator = Paginator(dataset, items_per_page)

#     # Obter o número da página da query string (se estiver disponível)
#     page = request.GET.get('page')

#     try:
#         # Obter os objetos da página solicitada
#         paginated_dataset = paginator.page(page)
#     except PageNotAnInteger:
#         # Se o parâmetro da página não for um número, mostrar a primeira página
#         paginated_dataset = paginator.page(1)
#     except EmptyPage:
#         # Se a página estiver fora dos limites (por exemplo, página 9999), mostrar a última página
#         paginated_dataset = paginator.page(paginator.num_pages)

#     context = {
#         'user': request.user,  # Passando o usuário logado para o template
#         "dataset": paginated_dataset,
#         "tipo_id": tipo_id,
#         # **gera_menu()  # Inclui o menu no contexto
#     }
#     context.update(gera_menu())  # Mescla o contexto existente com o menu

#     return render(request, "sn/lista_tipo.html", context)



# @login_required
# def perfil(request):
#     dataset = Tipo.objects.filter(fk_tipo_id='2')
#     context = {"dataset": dataset}
#     return render(request, "sn/lista_tipo.html", context)



###





