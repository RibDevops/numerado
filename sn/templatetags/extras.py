import os
from django import template

register = template.Library()

@register.simple_tag
def anexos_para(anexos_map, doc_numero, tipo_id, divisao_id):
    chave = (doc_numero, tipo_id, divisao_id)
    return anexos_map.get(chave, [])

@register.filter
def basename(value):
    """Retorna apenas o nome do arquivo sem o caminho completo."""
    return os.path.basename(value)
