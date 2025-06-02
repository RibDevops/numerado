from django.contrib.auth import authenticate, login as login_django
from django.contrib.auth import login as login_django
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rolepermissions.roles import assign_role, get_user_roles
from rolepermissions.decorators import has_permission_decorator
from core.settings import LOGIN_REDIRECT_URL
from django.contrib import messages
from sn.views.views_home import gera_menu
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

@login_required
# @has_permission_decorator('cadastro_user')
def cadastro(request):
    context ={}
    if request.method == "GET":
        context.update(gera_menu())
        return render(request, 'cadastro.html', context)
    else:
        username = request.POST.get('username')
        #password = request.POST.get('password')
        #tipo = request.POST.get('tipo')

        user = User.objects.filter(username=username).first()
        if user:
            # return HttpResponse('Usuário já existe')
            messages.add_message(request, messages.ERROR, 'Usuário já existe.')
            return redirect('cadastro')
        user = User.objects.create_user(username=username)

        user.save()
 
        # assign_role(user, tipo)
        messages.add_message(request, messages.SUCCESS, 'Usuário cadastrado com sucesso.')
        context.update(gera_menu())
        
        # return redirect('cadastro', context)
        return render(request, 'cadastro.html', context)
        # return render(request, 'sn/novo_setor.html', context)
        # return HttpResponse('Usuário cadastrado com sucesso')


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Tentar autenticar o usuário
            user = authenticate(username=username, password=password)

            if user is not None:
                # Autenticar o usuário
                login_django(request, user)
                request.session['username'] = user.username
                print(user.username)
                # request.session['username'] = user.username
                print("Usuário autenticado com sucesso!")
                return redirect('/')  # Redirecionar para a página inicial após o login
            else:
                print("Falha na autenticação do usuário. Verifique as credenciais.")
                return render(request, 'login.html', {'error_message': 'Credenciais inválidas'})

        except Exception as e:
            print(f"Erro durante a autenticação: {e}")
            return render(request, 'login.html', {'error_message': 'Erro durante a autenticação'})



# @login_required
# def reset(request):
#     if request.method == "GET":
#         users = User.objects.all()
#         return render(request, 'reset.html', {'users': users})
#     else:
#         username = request.POST.get('username')
#         password2 = request.POST.get('password2')
#         password = request.POST.get('password')
        
#         if password == password2:
#             user = User.objects.get(username=username)
#             user.set_password(password)
#             user.save()
#             messages.add_message(request, messages.SUCCESS, 'Senha alterada com sucesso.')
#             return redirect('reset')
#         else:
#             messages.add_message(request, messages.ERROR, 'As senhas fornecidas não correspondem. Por favor, verifique e tente novamente.')
#             return redirect('reset')

@login_required
def custom_logout(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'Logged out successfully!')
    return redirect("/")

@login_required
def perfil_usuario(request):
    context ={}
    
    user = request.user
    
    context = {
        'user' : user
    }
    context.update(gera_menu())

    return render(request, 'perfil_usuario.html', context)
