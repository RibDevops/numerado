from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django import forms
from sn.models import Divisao
from sn.forms import DivisaoForm, DivisaoForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from sn.views import gera_menu
from ..models import  Divisao
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
from django.contrib import messages
from django.shortcuts import get_object_or_404


@login_required
def lista_divisao(request):
    dataset = Divisao.objects.all()
    context = {"dataset": dataset}
    #print(context)
    context.update(gera_menu())  # Mescla o contexto existente com o menu
    return render(request, "sn/divisao/lista_divisao.html", context)

@login_required
def nova_divisao(request):
    context ={}
    if request.method == 'POST':
        form = DivisaoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro feito com sucesso.')
            return redirect('lista_divisao')  # Redirecione para a lista após criar
    else:
        # form = DivisaoForm()
        context['form']= DivisaoForm()
        context.update(gera_menu())  # Mescla o contexto existente com o menu
    
    # return render(request, 'caixa/criar.html', {'form': form})
    return render(request, 'sn/divisao/nova_divisao.html', context)

def delete_divisao(request, id):
    # Verifica se o registro existe antes de tentar excluí-lo
    divisao = get_object_or_404(Divisao, id=id)

    if request.method == 'POST':
        # Confirmação de exclusão do registro
        divisao.delete()
        messages.success(request, 'Registro excluído com sucesso.')
        # return redirect('lista_divisao', id=divisao.fk_divisao_id)
        return redirect('lista_divisao')
    
    # Caso o método da requisição seja GET, mostra o template de confirmação de exclusão
    context = {
        'divisao': divisao
    }
    return render(request, 'sn/divisao/delete_divisao.html', context)


def editar_divisao(request, id):
    divisao = get_object_or_404(Divisao, id=id)

    if request.method == 'POST':
        form = DivisaoForm(request.POST, instance=divisao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro atualizado com sucesso.')
            # return redirect('lista_divisao', id=divisao.fk_divisao_id)
            return redirect('lista_divisao')
    else:
        form = DivisaoForm(instance=divisao)

    context = {
        'form': form,
        'divisao': divisao
    }
    return render(request, 'sn/divisao/editar_divisao.html', context)