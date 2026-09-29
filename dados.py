# dados.py - guarda e le os produtos no banco SQLite (arquivo dados/vortex.db)
import os
import sqlite3

PASTA = os.path.dirname(os.path.abspath(__file__))
CAMINHO_BANCO = os.path.join(PASTA, "dados", "vortex.db")


def conectar():
    os.makedirs(os.path.dirname(CAMINHO_BANCO), exist_ok=True)
    return sqlite3.connect(CAMINHO_BANCO)


def criar_tabela():
    con = conectar()
    con.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco REAL NOT NULL,
            status TEXT NOT NULL
        )
    """)
    con.commit()
    con.close()


def inserir(nome, quantidade, preco, status):
    con = conectar()
    con.execute("INSERT INTO produtos (nome, quantidade, preco, status) VALUES (?, ?, ?, ?)",
                (nome, quantidade, preco, status))
    con.commit()
    con.close()


def atualizar(id_produto, nome, quantidade, preco, status):
    con = conectar()
    con.execute("UPDATE produtos SET nome=?, quantidade=?, preco=?, status=? WHERE id=?",
                (nome, quantidade, preco, status, id_produto))
    con.commit()
    con.close()


def excluir(id_produto):
    con = conectar()
    con.execute("DELETE FROM produtos WHERE id=?", (id_produto,))
    con.commit()
    con.close()


def listar(texto="", status="Todos"):
    """Devolve os produtos filtrando pelo nome e (opcional) pelo status."""
    sql = "SELECT id, nome, quantidade, preco, status FROM produtos WHERE nome LIKE ?"
    parametros = ["%" + texto + "%"]
    if status != "Todos":
        sql += " AND status = ?"
        parametros.append(status)
    sql += " ORDER BY nome"
    con = conectar()
    linhas = con.execute(sql, parametros).fetchall()
    con.close()
    return linhas


def resumo():
    """Devolve (total de produtos, total de unidades, valor total em estoque)."""
    con = conectar()
    total, unidades, valor = con.execute(
        "SELECT COUNT(*), COALESCE(SUM(quantidade), 0), COALESCE(SUM(quantidade * preco), 0) FROM produtos"
    ).fetchone()
    con.close()
    return total, unidades, valor
