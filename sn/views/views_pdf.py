import pdfkit
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from ..models import Numeracao

def generate_pdf(request, id):
    # Obter o documento
    doc = get_object_or_404(Numeracao, pk=id)
    anexos = doc.anexos.all()

    # Mesmo código de preparação dos dados que você já tem
    fechamento1 = '<div style="text-align: center">*.*.*</div>'
    # ... (todo o resto igual)

    data = {
        'title': 'PDF Report',
        'cm': '<div style="text-align: center">COMANDO</div>',
        'ci': '<div style="text-align: center">CEN<br>',
        'tipo': f'INFORME Nº {doc.doc_numero} / {doc.create_at.year} / CI</div>',
        'texto': doc.texto,
        'fechamento1': fechamento1,
        'fechamento2': fechamento2,
        'cabecalho_rodape': cabecalho_rodape,
        'anexos_html': anexos_html,
    }

    # Renderizar template
    html_string = render_to_string('pdf/template.html', data)

    # Opções do wkhtmltopdf
    options = {
        'page-size': 'A4',
        'margin-top': '15mm',
        'margin-right': '15mm',
        'margin-bottom': '15mm',
        'margin-left': '15mm',
        'encoding': "UTF-8",
        'no-outline': None,
        'enable-local-file-access': None,  # Importante para acessar arquivos locais
    }

    # Caminho para o executável (no Replit)
    config = pdfkit.configuration(wkhtmltopdf='/run/current-system/sw/bin/wkhtmltopdf')

    # Gerar PDF
    pdf_file = pdfkit.from_string(html_string, False, options=options, configuration=config)

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="documento_{doc.doc_numero}_{doc.create_at.year}.pdf"'
    return response