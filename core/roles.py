from rolepermissions.roles import AbstractUserRole


class sin(AbstractUserRole):
    available_permissions = {
        'criar': True,
        'editar': True,
        'excluir': True,
        'gerar': True,
        'import': True,
        'lista': True,
        'cadastro_user': True,
        'reset_user': True,
    }


class dci_admin(AbstractUserRole):
    available_permissions = {
        'criar': True,
        'editar': True,
        'excluir': True,
        'gerar': True,
        'import': True,
        'lista': True,
        'reset_user': True,
    }

class dci(AbstractUserRole):
    available_permissions = {
        'criar': True,
        'editar': True,
        'gerar': True,
        'import': True,
        'lista': True,
    }

class div(AbstractUserRole):
    available_permissions = {
        'lista': True,
    }
