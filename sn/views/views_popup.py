# views.py

from django.shortcuts import render, redirect
from ..forms import *

def add_destino_popup(request):
    if request.method == 'POST':
        form = DestinoForm(request.POST)
        if form.is_valid():
            destino = form.save()
            return render(request, 'close_popup.html', {'object': destino})
    else:
        form = DestinoForm()
    return render(request, '/sn/destino/novo_destino.html', {'form': form})
