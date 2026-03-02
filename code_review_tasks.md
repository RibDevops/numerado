# Revisão rápida da base e tarefas sugeridas

## 1) Tarefa de correção de erro de digitação
**Problema encontrado:** o plural configurado para o modelo `Numeracao` está como `"Numeros"`, sem acento, enquanto o restante do projeto usa acentuação em português.

**Tarefa sugerida:** ajustar `verbose_name_plural` para `"Números"` no `Meta` de `Numeracao`.

**Critério de aceite:** o Django Admin passa a exibir o plural acentuado corretamente.

## 2) Tarefa de correção de bug
**Problema encontrado:** o método `__str__` de `Encaminhamento` referencia `self.numeracao`, atributo que não existe no modelo (o campo correto é `doc_numero`). Isso tende a gerar `AttributeError` ao renderizar objetos dessa classe.

**Tarefa sugerida:** alterar o `__str__` para usar `self.doc_numero` (ou outro campo válido), e cobrir o caso com teste.

**Critério de aceite:** instâncias de `Encaminhamento` podem ser convertidas para string sem exceção.

## 3) Tarefa para ajustar comentário/discrepância de documentação
**Problema encontrado:** há um comentário dizendo que não deveria haver campo único de destino (`"não pode pq é necessário colocar vários destinos"`), porém a implementação atual usa `ForeignKey` para um único `fk_destino`.

**Tarefa sugerida:** alinhar comentário e implementação: ou remover/atualizar o comentário para refletir a regra atual, ou evoluir o modelo para suportar múltiplos destinos (ex.: `ManyToManyField`) se esse for o requisito real.

**Critério de aceite:** comentário e comportamento do modelo ficam consistentes com a regra de negócio definida.

## 4) Tarefa para melhorar teste
**Problema encontrado:** o arquivo de testes da app `sn` está vazio (apenas o stub padrão do Django).

**Tarefa sugerida:** criar testes unitários iniciais para:
- `__str__` dos modelos principais (`Numeracao`, `Encaminhamento`);
- validação do método `clean` de `Numeracao` (normalização de `doc_sigad_origem`);
- fluxo mínimo de criação de `Numeracao` em view crítica.

**Critério de aceite:** suite da app `sn` executa com casos reais cobrindo comportamento básico de modelos e uma view.
