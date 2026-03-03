from urllib import response
from django.shortcuts import render, get_object_or_404
from django.http import FileResponse, HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from ..models import Numeracao

def generate_pdf(request, id):
    # Obter o documento primeiro
    doc = get_object_or_404(Numeracao, pk=id)
    
    # Agora podemos acessar os anexos
    anexos = doc.anexos.all()  # Usando o related_name definido no modelo
    
    # Configurações do documento
    fechamento1 = '<div style="text-align: center">*.*.*</div>'
    fechamento2 = '''
    <table style="border-collapse:collapse;border-spacing:0" class="tg">
        <thead>
            <tr>
                <td style="border-color:#fe0000;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:12px;overflow:hidden;padding:10px 5px;text-align:justify;vertical-align:middle;word-break:normal">
                    <span style="color:#FE0000">
                        Este documento refere-se à Atividade de Inteligência e, como tal, é de utilização interna e considerado preparatório, de acordo com o Decreto nº 7.724, art 3º, inciso XII. A divulgação, a revelação, o fornecimento, a utilização ou a reprodução desautorizada das informações e conhecimentos utilizados, contidos ou veiculados neste documento, a qualquer tempo, meio ou modo, inclusive mediante acesso ou facilitação de acesso indevidos, caracterizam crime de violação do sigilo funcional e improbidade administrativa tipificados, respectivamente, nos art. 154 e art. 325 do Decreto-Lei nº 2.848, e nos art. 116, inciso VIII e art. 132, incisos IV e IX, da Lei nº 8.112/1990.
                    </span>
                </td>
            </tr>
        </thead>
    </table>
    '''
    
    cabecalho_rodape = '''
    <table style="border-collapse:collapse;border-spacing:0" class="tg">
        <thead>
            <tr>
                <td style="border-color:#fe0000;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:center;vertical-align:middle;word-break:normal">
                    <span style="color:#FE0000">DOCUMENTO PREPARATÓRIO - ACESSO RESTRITO</span><br>
                    <span style="color:#FE0000">Art. 3º, Inciso XII e Art. 20 do Decreto nº 7.724, de 16 de maio de 2012</span>
                </td>
            </tr>
        </thead>
    </table>
    '''
    
    # Preparar HTML para os anexos
    anexos_html = ""
    for anexo in anexos:
        anexos_html += f'''
        <div style="page-break-before: always;">
            <h3>Anexo: {anexo.nome_original}</h3>
            <img src="{anexo.imagem.url}" style="max-width: 100%; height: auto;">
        </div>
        '''
    
    data = {
        'title': 'PDF Report',
        'cm': '<div style="text-align: center">COMANDO</div>',
        'ci': '<div style="text-align: center">CEN<br>',
        'tipo': f'INFORME Nº {doc.doc_numero} / {doc.create_at.year} / CI</div>', 
        'texto': doc.texto,
        'fechamento1': fechamento1,
        'fechamento2': fechamento2,
        'cabecalho_rodape': cabecalho_rodape,
        'anexos_html': anexos_html,  # HTML processado dos anexos
    }

    # Renderizar o template HTML
    html_string = render_to_string('pdf/template.html', data)
    
    # Gerar o PDF
    pdf_file = HTML(
        string=html_string, 
        base_url=request.build_absolute_uri('/')
    ).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="documento_{doc.doc_numero}_{doc.create_at.year}.pdf"'
    return response

    


    return response