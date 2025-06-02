from sn.models import Tipo
from django.shortcuts import render

def handler404(request, exception):
    return render(request, 'home.html')

def gera_menu():
    data_tipo = Tipo.objects.all()
    context = ({"data_tipo": data_tipo})  # Mescla o contexto existente com o novo contexto
    return context

def home(request):
    context = gera_menu()  # Mescla o contexto existente com o novo contexto
    return render(request, 'home.html', context )