from .models import Divisao, Setor

def divisao_do_usuario(request):
    if request.user.is_authenticated:
        try:
            divisao = Divisao.objects.get(divisao=request.user.last_name)
            # print(divisao)
            setor = Setor.objects.filter(fk_divisao=divisao).first()
            # print(setor)
            return {
                'divisao_nome': divisao.divisao,
                'setor_nome': setor.setor if setor else '---'
            }
        except Divisao.DoesNotExist:
            return {'divisao_nome': '---', 'setor_nome': '---'}
    return {}
