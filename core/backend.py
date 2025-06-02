# from django.contrib.auth import get_user_model
# from django_auth_ldap.backend import LDAPBackend

# class CustomLDAPBackend(LDAPBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         UserModel = get_user_model()
        
#         # Verifica se o usuário existe localmente
#         try:
#             user = UserModel.objects.get(username=username)
#         except UserModel.DoesNotExist:
#             return None
        
#         # Se o usuário existe localmente, realiza a autenticação LDAP
#         return super().authenticate(request, username=username, password=password, **kwargs)


from django_auth_ldap.backend import LDAPBackend
from django.contrib.auth import get_user_model

class CustomLDAPBackend(LDAPBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        # Verifica se o usuário existe localmente
        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            return None
        # Se o usuário existe localmente, realiza a autenticação LDAP
        return super().authenticate(request, username=username, password=password, **kwargs)

#    def populate_user(self, username, ldap_user):
#        user = super().populate_user(username, ldap_user)
#        print(user)
#        if user:
#            user.is_active = False  # Definindo is_active como False
#            user.save()
#        return user

