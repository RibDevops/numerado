from django.test import SimpleTestCase

from sn.models import Anexo, Destino, Divisao, Encaminhamento, Numeracao, Setor, Tipo


class ModelBehaviorTests(SimpleTestCase):
    """Testes de regressão básica para contratos de modelos usados nas views."""

    def test_numeracao_clean_normaliza_sigad_para_maiusculo(self):
        numeracao = Numeracao(doc_sigad_origem="abc-123")

        numeracao.clean()

        self.assertEqual(numeracao.doc_sigad_origem, "ABC-123")

    def test_encaminhamento_str_usa_doc_numero_sem_attribute_error(self):
        divisao = Divisao(divisao="DTI")
        destino = Destino(destino="Arquivo")
        tipo = Tipo(tipo_doc="Memorando")
        setor = Setor(setor="Protocolo", fk_divisao=divisao)
        numeracao = Numeracao(fk_tipo=tipo, fk_destino=destino, doc_numero=42, title="Doc")
        encaminhamento = Encaminhamento(
            doc_numero=numeracao,
            origem_divisao=divisao,
            destino_setor=setor,
        )

        valor = str(encaminhamento)

        self.assertIn("Encaminhado para", valor)
        self.assertIn("42", valor)

    def test_encaminhamento_model_expoe_campo_doc_numero(self):
        campos = {field.name for field in Encaminhamento._meta.get_fields()}

        self.assertIn("doc_numero", campos)
        self.assertNotIn("documento", campos)

    def test_anexo_model_expoe_campo_doc_numero(self):
        campos = {field.name for field in Anexo._meta.get_fields()}

        self.assertIn("doc_numero", campos)
        self.assertNotIn("documento", campos)
