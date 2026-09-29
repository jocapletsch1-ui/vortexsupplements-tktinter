import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

import dados
from validacoes import validar_produto, STATUS_VALIDOS


def iniciar():
    dados.criar_tabela()

    janela = tk.Tk()
    janela.title("Vortex Supplements")
    janela.geometry("760x620")
    janela.resizable(False, False)

    estado = {"id_edicao": None}

    nome_var = tk.StringVar()
    qtd_var = tk.StringVar()
    preco_var = tk.StringVar()
    status_var = tk.StringVar(value="Disponível")
    busca_var = tk.StringVar()
    filtro_var = tk.StringVar(value="Todos")

    def atualizar_lista():
        for item in tabela.get_children():
            tabela.delete(item)

        produtos = dados.listar(busca_var.get(), filtro_var.get())

        for produto in produtos:
            tabela.insert(
                "",
                "end",
                values=(produto[0], produto[1], produto[2], f"{produto[3]:.2f}", produto[4]),
            )

        if len(produtos) == 0:
            lbl_aviso.config(text="Nenhum produto encontrado.")
        else:
            lbl_aviso.config(text="")

    def atualizar_resumo():
        total, unidades, valor = dados.resumo()
        lbl_resumo.config(
            text=f"Produtos: {total}   |   Quantidade: {unidades}   |   Valor total: R$ {valor:.2f}"
        )

    def limpar():
        nome_var.set("")
        qtd_var.set("")
        preco_var.set("")
        status_var.set("Disponível")
        estado["id_edicao"] = None
        btn_salvar.config(text="Salvar")
        campo_nome.focus()

    def salvar():
        erros, nome, qtd, preco, status = validar_produto(
            nome_var.get(), qtd_var.get(), preco_var.get(), status_var.get()
        )

        if erros:
            messagebox.showwarning("Erro", "\n".join(erros))
            return

        try:
            if estado["id_edicao"] is None:
                dados.inserir(nome, qtd, preco, status)
                messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
            else:
                dados.atualizar(estado["id_edicao"], nome, qtd, preco, status)
                messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Não foi possível salvar: {erro}")
            return

        limpar()
        atualizar_lista()
        atualizar_resumo()

    def editar():
        selecionado = tabela.selection()
        if not selecionado:
            messagebox.showinfo("Aviso", "Selecione um produto na lista.")
            return

        id_produto, nome, quantidade, preco, status = tabela.item(selecionado[0], "values")
        nome_var.set(nome)
        qtd_var.set(quantidade)
        preco_var.set(preco)
        status_var.set(status)
        estado["id_edicao"] = int(id_produto)
        btn_salvar.config(text="Salvar alterações")
        campo_nome.focus()

    def excluir():
        selecionado = tabela.selection()
        if not selecionado:
            messagebox.showinfo("Aviso", "Selecione um produto para excluir.")
            return

        id_produto, nome = tabela.item(selecionado[0], "values")[:2]
        resposta = messagebox.askyesno("Confirmar", f"Deseja excluir '{nome}'?")
        if not resposta:
            return

        try:
            dados.excluir(int(id_produto))
        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Não foi possível excluir: {erro}")
            return

        limpar()
        atualizar_lista()
        atualizar_resumo()
        messagebox.showinfo("Sucesso", "Produto excluído.")

    def sair():
        if nome_var.get() or qtd_var.get() or preco_var.get():
            resposta = messagebox.askyesno("Sair", "Tem dados não salvos. Deseja sair mesmo assim?")
            if not resposta:
                return
        janela.destroy()

    frame_principal = ttk.Frame(janela, padding=10)
    frame_principal.pack(fill="both", expand=True)

    ttk.Label(frame_principal, text="Vortex Supplements", font=("Arial", 16, "bold")).pack(anchor="w")
    ttk.Label(frame_principal, text="Sistema de controle de estoque").pack(anchor="w", pady=(0, 10))

    frame_cadastro = ttk.LabelFrame(frame_principal, text="Cadastro de produto", padding=10)
    frame_cadastro.pack(fill="x")

    ttk.Label(frame_cadastro, text="Nome:").grid(row=0, column=0, sticky="w", pady=5)
    campo_nome = ttk.Entry(frame_cadastro, textvariable=nome_var, width=40)
    campo_nome.grid(row=0, column=1, sticky="w", pady=5)

    ttk.Label(frame_cadastro, text="Quantidade:").grid(row=1, column=0, sticky="w", pady=5)
    campo_qtd = ttk.Entry(frame_cadastro, textvariable=qtd_var, width=15)
    campo_qtd.grid(row=1, column=1, sticky="w", pady=5)

    ttk.Label(frame_cadastro, text="Preço (R$):").grid(row=2, column=0, sticky="w", pady=5)
    campo_preco = ttk.Entry(frame_cadastro, textvariable=preco_var, width=15)
    campo_preco.grid(row=2, column=1, sticky="w", pady=5)

    ttk.Label(frame_cadastro, text="Status:").grid(row=3, column=0, sticky="w", pady=5)
    combo_status = ttk.Combobox(
        frame_cadastro,
        textvariable=status_var,
        values=STATUS_VALIDOS,
        state="readonly",
        width=15,
    )
    combo_status.grid(row=3, column=1, sticky="w", pady=5)

    botoes = ttk.Frame(frame_cadastro)
    botoes.grid(row=4, column=0, columnspan=2, sticky="w", pady=(10, 0))
    btn_salvar = ttk.Button(botoes, text="Salvar", command=salvar)
    btn_salvar.pack(side="left")
    ttk.Button(botoes, text="Limpar", command=limpar).pack(side="left", padx=5)

    campo_nome.bind("<Return>", lambda e: salvar())
    campo_qtd.bind("<Return>", lambda e: salvar())
    campo_preco.bind("<Return>", lambda e: salvar())

    frame_lista = ttk.LabelFrame(frame_principal, text="Produtos cadastrados", padding=10)
    frame_lista.pack(fill="both", expand=True, pady=10)

    busca_frame = ttk.Frame(frame_lista)
    busca_frame.pack(fill="x")
    ttk.Label(busca_frame, text="Buscar:").pack(side="left")
    campo_busca = ttk.Entry(busca_frame, textvariable=busca_var, width=25)
    campo_busca.pack(side="left", padx=5)
    ttk.Label(busca_frame, text="Status:").pack(side="left", padx=(10, 0))
    combo_filtro = ttk.Combobox(
        busca_frame,
        textvariable=filtro_var,
        values=("Todos",) + STATUS_VALIDOS,
        state="readonly",
        width=12,
    )
    combo_filtro.pack(side="left", padx=5)
    ttk.Button(busca_frame, text="Buscar", command=atualizar_lista).pack(side="left", padx=5)

    tabela = ttk.Treeview(frame_lista, columns=("id", "nome", "quantidade", "preco", "status"), show="headings", height=10)
    tabela.heading("id", text="ID")
    tabela.heading("nome", text="Nome")
    tabela.heading("quantidade", text="Qtd")
    tabela.heading("preco", text="Preço")
    tabela.heading("status", text="Status")
    tabela.column("id", width=50)
    tabela.column("nome", width=240)
    tabela.column("quantidade", width=70)
    tabela.column("preco", width=90)
    tabela.column("status", width=110)
    tabela.pack(fill="both", expand=True, pady=(8, 5))

    lbl_aviso = ttk.Label(frame_lista, text="", foreground="red")
    lbl_aviso.pack(anchor="w")

    botoes_lista = ttk.Frame(frame_lista)
    botoes_lista.pack(fill="x")
    ttk.Button(botoes_lista, text="Editar", command=editar).pack(side="left")
    ttk.Button(botoes_lista, text="Excluir", command=excluir).pack(side="left", padx=5)

    frame_resumo = ttk.LabelFrame(frame_principal, text="Resumo", padding=10)
    frame_resumo.pack(fill="x")
    lbl_resumo = ttk.Label(frame_resumo, text="")
    lbl_resumo.pack(anchor="w")

    janela.protocol("WM_DELETE_WINDOW", sair)
    atualizar_lista()
    atualizar_resumo()
    campo_nome.focus()
    janela.mainloop()
