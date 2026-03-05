import io
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
from ..models import Numeracao


def generate_pdf(request, id):
    doc = get_object_or_404(Numeracao, pk=id)
    anexos = doc.anexos.all()

    fechamento1 = '<div style="text-align: center">*.*.*</div>'
    fechamento2 = ''
    cabecalho_rodape = ''
    anexos_html = ''

    for anexo in anexos:
        if anexo.imagem:
            # WeasyPrint can handle absolute paths to files on the filesystem
            image_path = anexo.imagem.path
            anexos_html += f'<div style="text-align: center; margin-top: 20px;"><img src="file://{image_path}" style="max-width: 100%; height: auto;"></div>'

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

    html_string = render_to_string('pdf/template.html', data)

    font_config = FontConfiguration()
    html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
    pdf_file = html.write_pdf(font_config=font_config)

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="documento_{doc.doc_numero}_{doc.create_at.year}.pdf"'
    return response
