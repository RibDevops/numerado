from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django import forms
from sn.models import Numeracao, Setor
from sn.forms import NumeracaoForm, OmForm, OmForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from sn.views import gera_menu
from ..forms import NumeracaoForm
from ..models import Numeracao, Om, Setor
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
def lista_om(request):
    dataset = Om.objects.all()
    context = {"dataset": dataset}
    context.update(gera_menu())  # Mescla o contexto existente com o menu
    return render(request, "sn/om/lista_om.html", context)

@login_required
def nova_om(request):
    context ={}
    if request.method == 'POST':
        form = OmForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro feito com sucesso.')
            return redirect('lista_om')  # Redirecione para a lista após criar
    else:
        # form = OmForm()
        context['form']= OmForm()
        context.update(gera_menu())  # Mescla o contexto existente com o menu
    
    # return render(request, 'caixa/criar.html', {'form': form})
    return render(request, 'sn/om/novo_om.html', context)

def delete_om(request, id):
    # Verifica se o registro existe antes de tentar excluí-lo
    om = get_object_or_404(Setor, id=id)

    if request.method == 'POST':
        # Confirmação de exclusão do registro
        om.delete()
        messages.success(request, 'Registro excluído com sucesso.')
        # return redirect('lista_om', id=om.fk_om_id)
        return redirect('lista_om')
    
    # Caso o método da requisição seja GET, mostra o template de confirmação de exclusão
    context = {
        'om': om
    }
    return render(request, 'sn/om/delete_om.html', context)


def editar_om(request, id):
    om = get_object_or_404(Om, id=id)

    if request.method == 'POST':
        form = OmForm(request.POST, instance=om)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro atualizado com sucesso.')
            # return redirect('lista_om', id=om.fk_om_id)
            return redirect('lista_om')
    else:
        form = OmForm(instance=om)

    context = {
        'form': form,
        'om': om
    }
    return render(request, 'sn/om/editar_om.html', context)