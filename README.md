# Vortex Supplements

Este projeto foi feito como trabalho escolar para controlar o estoque de produtos de suplementos.

## Integrantes
- Vinicius Luz
- Joaquim T
- Pedro de Lima
- Turma: 05

## Objetivo
O programa serve para cadastrar, listar, editar e excluir produtos do estoque.

## Como rodar
Abra o terminal na pasta do projeto e execute:

```bash
python main.py
```

## O que o programa faz
- cadastra produtos
- mostra os produtos na tabela
- busca por nome
- edita itens
- exclui itens com confirmação
- salva tudo em SQLite
- mostra um resumo do estoque

## Arquivos
- `main.py` - inicia o programa
- `interface.py` - cria a interface gráfica
- `dados.py` - salva e lê os dados no banco
- `validacoes.py` - valida os campos

## Validações
- nome obrigatório
- quantidade deve ser número inteiro
- preço deve ser maior que zero
- status deve ser "Disponível" ou "Sem estoque"

## Limitações
- é um programa simples
- funciona localmente
- não tem login nem cadastro de usuário

## Observação
Esse projeto foi feito com Python e Tkinter para aprender interface gráfica e banco de dados de forma simples.

