from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django import forms
from sn.models import Numeracao, Setor
from sn.forms import NumeracaoForm, SetorForm, SetorForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from sn.views import gera_menu
from ..forms import NumeracaoForm
from ..models import Numeracao, Setor
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
def lista_setor(request):
    dataset = Setor.objects.all()
    context = {"dataset": dataset}
    context.update(gera_menu())  # Mescla o contexto existente com o menu
    return render(request, "sn/setor/lista_setor.html", context)

@login_required
def novo_setor(request):
    context ={}
    if request.method == 'POST':
        form = SetorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro feito com sucesso.')
            return redirect('lista_setor')  # Redirecione para a lista após criar
    else:
        # form = SetorForm()
        context['form']= SetorForm()
        context.update(gera_menu())  # Mescla o contexto existente com o menu
    
    # return render(request, 'caixa/criar.html', {'form': form})
    return render(request, 'sn/setor/novo_setor.html', context)

def delete_setor(request, id):
    # Verifica se o registro existe antes de tentar excluí-lo
    setor = get_object_or_404(Setor, id=id)

    if request.method == 'POST':
        # Confirmação de exclusão do registro
        setor.delete()
        messages.success(request, 'Registro excluído com sucesso.')
        # return redirect('lista_setor', id=setor.fk_setor_id)
        return redirect('lista_setor')
    
    # Caso o método da requisição seja GET, mostra o template de confirmação de exclusão
    context = {
        'setor': setor
    }
    return render(request, 'sn/setor/delete_setor.html', context)


def editar_setor(request, id):
    setor = get_object_or_404(Setor, id=id)

    if request.method == 'POST':
        form = SetorForm(request.POST, instance=setor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro atualizado com sucesso.')
            # return redirect('lista_setor', id=setor.fk_setor_id)
            return redirect('lista_setor')
    else:
        form = SetorForm(instance=setor)

    context = {
        'form': form,
        'setor': setor
    }
    return render(request, 'sn/setor/editar_setor.html', context)