import matplotlib.pyplot as plt
from io import BytesIO
from django.shortcuts import render
from ..models import Numeracao, Tipo, Divisao
from django.db.models import Count
import base64

def gerar_graficos(request):
    # Total de documentos no ano
    total_documentos_ano = Numeracao.objects.filter(create_at__year=2024).count()

    # Total de documentos separados por tipo
    documentos_por_tipo = Numeracao.objects.values('fk_tipo__tipo_doc').annotate(total=Count('fk_tipo')).order_by('-total')

    # Total de documentos separados por divisão
    documentos_por_divisao = Numeracao.objects.values('fk_divisao__divisao').annotate(total=Count('fk_divisao')).order_by('-total')

    # Gráfico de Pizza - Total de documentos no ano
    fig1, ax1 = plt.subplots()
    ax1.pie([total_documentos_ano, 100 - total_documentos_ano], labels=[f'Documentos 2024 ({total_documentos_ano})', f'Outros ({100 - total_documentos_ano})'], autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    buf1 = BytesIO()
    plt.savefig(buf1, format='png')
    plt.close(fig1)
    image_base64_1 = base64.b64encode(buf1.getvalue()).decode('utf-8')

    # Gráfico de Pizza - Documentos por Tipo
    labels_tipo = [f"{entry['fk_tipo__tipo_doc']} ({entry['total']})" for entry in documentos_por_tipo]
    sizes_tipo = [entry['total'] for entry in documentos_por_tipo]
    fig2, ax2 = plt.subplots()
    ax2.pie(sizes_tipo, labels=labels_tipo, autopct='%1.1f%%', startangle=90)
    ax2.axis('equal')

    buf2 = BytesIO()
    plt.savefig(buf2, format='png')
    plt.close(fig2)
    image_base64_2 = base64.b64encode(buf2.getvalue()).decode('utf-8')

    # Gráfico de Pizza - Documentos por Divisão
    labels_divisao = [f"{entry['fk_divisao__divisao']} ({entry['total']})" for entry in documentos_por_divisao]
    sizes_divisao = [entry['total'] for entry in documentos_por_divisao]
    fig3, ax3 = plt.subplots()
    ax3.pie(sizes_divisao, labels=labels_divisao, autopct='%1.1f%%', startangle=90)
    ax3.axis('equal')

    buf3 = BytesIO()
    plt.savefig(buf3, format='png')
    plt.close(fig3)
    image_base64_3 = base64.b64encode(buf3.getvalue()).decode('utf-8')

    # Gráfico de Pizza - Tipos de Documentos por Divisão
    divisao_tipo_aggregation = Numeracao.objects.values('fk_divisao__divisao', 'fk_tipo__tipo_doc').annotate(total=Count('id')).order_by('fk_divisao__divisao', 'fk_tipo__tipo_doc')
    
    # Agrupar dados para o gráfico
    divisao_tipo_data = {}
    for entry in divisao_tipo_aggregation:
        divisao = entry['fk_divisao__divisao']
        tipo = entry['fk_tipo__tipo_doc']
        total = entry['total']
        if divisao not in divisao_tipo_data:
            divisao_tipo_data[divisao] = {}
        divisao_tipo_data[divisao][tipo] = total

    fig4, ax4 = plt.subplots(len(divisao_tipo_data), 1, figsize=(10, 5 * len(divisao_tipo_data)))
    if len(divisao_tipo_data) == 1:
        ax4 = [ax4]
    
    for i, (divisao, tipos) in enumerate(divisao_tipo_data.items()):
        labels = [f"{tipo} ({total})" for tipo, total in tipos.items()]
        sizes = [total for total in tipos.values()]
        ax4[i].pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax4[i].set_title(f"Tipos de Documentos na Divisão: {divisao}")
        ax4[i].axis('equal')

    buf4 = BytesIO()
    plt.savefig(buf4, format='png')
    plt.close(fig4)
    image_base64_4 = base64.b64encode(buf4.getvalue()).decode('utf-8')

    context = {
        'image_base64_1': image_base64_1,
        'image_base64_2': image_base64_2,
        'image_base64_3': image_base64_3,
        'image_base64_4': image_base64_4,
    }
    return render(request, 'graficos.html', context)
