from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django import forms
from sn.models import Numeracao, Destino
from sn.forms import NumeracaoForm, DestinoForm, DestinoForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from sn.views import gera_menu
from ..forms import NumeracaoForm
from ..models import Numeracao, Destino
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.shortcuts import redirect
from datetime import datetime
from django.db import transaction, connection
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from ..forms import NumeracaoForm
from django.contrib import messages
from django.shortcuts import get_object_or_404


@login_required
def lista_destino(request):
    dataset = Destino.objects.all()
    context = {"dataset": dataset}
    context.update(gera_menu())  # Mescla o contexto existente com o menu
    return render(request, "sn/destino/lista_destino.html", context)

@login_required
def novo_destino(request):
    context ={}
    if request.method == 'POST':
        form = DestinoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro feito com sucesso.')
            return redirect('lista_destino')  # Redirecione para a lista após criar
    else:
        # form = DestinoForm()
        context['form']= DestinoForm()
        context.update(gera_menu())  # Mescla o contexto existente com o menu
    
    # return render(request, 'caixa/criar.html', {'form': form})
    return render(request, 'sn/destino/novo_destino.html', context)

def delete_destino(request, id):
    # Verifica se o registro existe antes de tentar excluí-lo
    destino = get_object_or_404(Destino, id=id)

    if request.method == 'POST':
        # Confirmação de exclusão do registro
        destino.delete()
        messages.success(request, 'Registro excluído com sucesso.')
        # return redirect('lista_destino', id=destino.fk_destino_id)
        return redirect('lista_destino')
    
    # Caso o método da requisição seja GET, mostra o template de confirmação de exclusão
    context = {
        'destino': destino
    }
    return render(request, 'sn/destino/delete_destino.html', context)


def editar_destino(request, id):
    destino = get_object_or_404(Destino, id=id)

    if request.method == 'POST':
        form = DestinoForm(request.POST, instance=destino)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro atualizado com sucesso.')
            # return redirect('lista_destino', id=destino.fk_destino_id)
            return redirect('lista_destino')
    else:
        form = DestinoForm(instance=destino)

    context = {
        'form': form,
        'destino': destino
    }
    return render(request, 'sn/destino/editar_destino.html', context)