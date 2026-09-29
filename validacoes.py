
STATUS_VALIDOS = ("Disponível", "Sem estoque")


def validar_produto(nome, quantidade, preco, status):
    erros = []
    nome = nome.strip()

    if nome == "":
        erros.append("O nome é obrigatório.")
    elif len(nome) < 3:
        erros.append("O nome deve ter pelo menos 3 letras.")

    try:
        qtd = int(quantidade)
        if qtd < 0:
            erros.append("A quantidade não pode ser negativa.")
    except ValueError:
        erros.append("A quantidade deve ser um número inteiro.")
        qtd = 0

    try:
        valor = float(str(preco).replace(",", "."))
        if valor <= 0:
            erros.append("O preço deve ser maior que zero.")
    except ValueError:
        erros.append("O preço deve ser um número válido.")
        valor = 0

    if status not in STATUS_VALIDOS:
        erros.append("Escolha um status válido.")

    if qtd == 0 and status == "Disponível":
        erros.append("Se a quantidade for 0, o status deve ser 'Sem estoque'.")
    if qtd > 0 and status == "Sem estoque":
        erros.append("Se a quantidade for maior que 0, o status deve ser 'Disponível'.")

    return erros, nome, qtd, valor, status
