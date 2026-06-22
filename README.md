# Fotolog

Projeto de catálogo de fotos para a disciplina de **Estrutura de Dados (UFC)**. O programa roda no terminal e utiliza uma **árvore AVL** para organizar as fotos por data.

## Como rodar

Não é necessário instalar bibliotecas externas. Basta usar o Python:

```bash
python repl.py
```

Dentro do programa, digite:

* `:help` para ver a lista de comandos;
* `:quit` para encerrar a execução.

## Como foi feito

### Ordenação

A árvore AVL utiliza a chave `(timestamp, id)` para organizar os nós. O **ID** é usado apenas como critério de desempate quando duas fotos possuem exatamente a mesma data.

### Buscas por período

O comando `:range` faz poda na árvore durante a busca. Quando identifica que um determinado ramo contém apenas datas fora do intervalo solicitado, ele ignora esse ramo e evita percorrê-lo, reduzindo o tempo de execução.

### Dicionário auxiliar

Para evitar percorrer a árvore inteira ao buscar uma foto específica com o comando `:get`, foi utilizado um dicionário Python indexado pelo ID da foto. Dessa forma, o acesso ocorre diretamente.

### Datas

O sistema aceita tanto **timestamps em segundos** quanto datas em formato textual, por exemplo:

```text
2024-05-10
```
