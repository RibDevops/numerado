# 🔧 Refatoração mínima da app `sn` (mapa + mudanças + regressão)

## 1) Mapa de funções e fluxo

### Núcleo do fluxo de documentos (`views_numeracao.py`)
1. `nova_numeracao` cria registros de numeração por destino.
2. `lista_numeracao` lista documentos visíveis para a divisão/setor.
3. `adicionar_anexo` anexa arquivo a um documento.
4. `encaminhar_documento` registra encaminhamento para um setor.
5. `devolver_documento` remove encaminhamento quando o setor devolve.

## 2) O que foi refatorado (mínimo, sem alterar regra de negócio)

### a) Limpeza de código não usado
- Removido bloco grande de código legado comentado no topo de `views_numeracao.py`.
- Removidos imports duplicados e não utilizados.

### b) Correções de inconsistência de nomes de campos
- Padronizado uso de `doc_numero` em vez de `documento` nas rotas de anexos/encaminhamento.
- Corrigido filtro de devolução para `doc_numero_id`.

### c) Comentários de documentação no código
- Adicionados docstrings nas funções:
  - `adicionar_anexo`
  - `encaminhar_documento`
  - `devolver_documento`
- Comentário descritivo no módulo para deixar explícito o escopo do arquivo.

## 3) Testes de regressão básicos adicionados

Arquivo: `sn/tests.py`

- `test_numeracao_clean_normaliza_sigad_para_maiusculo`
- `test_encaminhamento_str_usa_doc_numero_sem_attribute_error`
- `test_encaminhamento_model_expoe_campo_doc_numero`
- `test_anexo_model_expoe_campo_doc_numero`

## 4) Benefício prático das mudanças
- Menos risco de `AttributeError` por nome de campo inconsistente.
- Menor ruído no arquivo de view principal.
- Base mais legível para evoluções futuras (ex.: extrair serviços para encaminhamento/anexos).

## 5) Próximos passos sugeridos
- Extrair regras de autorização de `lista_numeracao` para funções auxiliares.
- Criar testes de integração de views com `RequestFactory`.
- Adicionar validação de permissões de encaminhamento/devolução por divisão.
