# =============================
# IMPORTS
# =============================

# Biblioteca padrão
import tkinter.messagebox as msg

# Biblioteca externa
import customtkinter as ctk

# Módulos internos
from storage import (
    adicionar_trabalhador,
    listar_trabalhadores,
    deletar_trabalhador,
    calcular_saldo,
    definir_salario,
    adicionar_vale,
    remover_vale,
    limpar_vales,
    carregar_obras,
    adicionar_obra,
    listar_obras,
    registrar_pagamento,
    remover_pagamento_obra,
    remover_obra
)

from utils import formatar_moeda, converter_moeda_para_float

# =============================
# FORMATAÇÃO AUTOMÁTICA DE MOEDA
# =============================

def formatar_entry_moeda(event):
    entry = event.widget
    valor = entry.get()

    # Remove tudo que não for número
    numeros = "".join(filter(str.isdigit, valor))

    if not numeros:
        entry.delete(0, "end")
        return

    # Converte para centavos
    valor_float = float(numeros) / 100

    # Formata padrão brasileiro
    texto_formatado = formatar_moeda(valor_float)

    entry.delete(0, "end")
    entry.insert(0, texto_formatado)


# =============================
# CONFIGURAÇÕES GLOBAIS
# =============================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

FONT_TITULO = ("Arial", 26, "bold")
FONT_SUBTITULO = ("Arial", 20, "bold")
FONT_NORMAL = ("Arial", 16)

PAD_Y = 8
PAD_X = 10


# =============================
# MENU
# =============================

class Menu(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        container = ctk.CTkFrame(self, corner_radius=20)
        container.grid(row=0, column=0, padx=200, pady=80, sticky="nsew")

        container.grid_columnconfigure(0, weight=1)

        titulo = ctk.CTkLabel(
            container,
            text="Sistema de Vale",
            font=("Arial", 34, "bold")
        )
        titulo.pack(pady=40)

        self.msg_label = ctk.CTkLabel(
            container,
            text="",
            font=("Arial", 16),
            text_color="#4CAF50"
        )
        self.msg_label.pack(pady=5)

        self.criar_botao(container, "Registrar trabalhador", Registro)
        self.criar_botao(container, "Registrar Obra", RegistrarObra)
        self.criar_botao(container, "Gerenciar obras", GerenciarObras)
        self.criar_botao(container, "Gerenciar trabalhadores", Gerenciar)
        self.criar_botao(container, "Deletar trabalhador", Deletar)
        self.criar_botao(container, "Deletar Obra", DeletarObra)

    def criar_botao(self, parent, texto, tela):
        botao = ctk.CTkButton(
            parent,
            text=texto,
            width=320,
            height=55,
            font=("Arial", 16),
            command=lambda: self.controller.mostrar_tela(tela)
        )
        botao.pack(pady=15)

    def atualizar_mensagem(self, texto):
        self.msg_label.configure(text=texto)
        self.after(5000, lambda: self.msg_label.configure(text=""))



# =============================
# REGISTRO
# =============================

class Registro(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        titulo = ctk.CTkLabel(
            self,
            text="Registrar trabalhador",
            font=("Arial", 28, "bold")
        )
        titulo.pack(pady=40)

        self.nome = ctk.CTkEntry(
            self,
            placeholder_text="Nome do trabalhador",
            width=400,
            height=45,
            font=("Arial", 16)
        )
        self.nome.pack(pady=20)

        ctk.CTkButton(
            self,
            text="Registrar",
            width=200,
            height=45,
            command=self.salvar
        ).pack(pady=10)

        ctk.CTkButton(
            self,
            text="Voltar",
            width=200,
            height=45,
            command=lambda: controller.mostrar_tela(Menu)
        ).pack(pady=20)

    def salvar(self):
        nome = self.nome.get().strip()

        if not nome:
            msg.showerror("Erro", "Digite um nome válido.")
            return

        adicionar_trabalhador(nome)

        mensagem = f"{nome} registrado com sucesso!"
        self.controller.menu.atualizar_mensagem(mensagem)

        self.nome.delete(0, "end")
        self.controller.mostrar_tela(Menu)

    def abrir(self, trabalhador):
        self.controller.trabalhador_atual = trabalhador
        self.controller.mostrar_tela(GerenciarTrabalhador)

# ============================
# REGISTRAR OBRA
# ============================

class RegistrarObra(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        titulo = ctk.CTkLabel(
            self,
            text="Registrar Obra",
            font=("Arial", 28, "bold")
        )
        titulo.pack(pady=20)

        self.nome = ctk.CTkEntry(self, placeholder_text="Nome da obra", width=400, height=45, font=("Arial", 16))
        self.nome.pack(pady=10)

        self.montador = ctk.CTkEntry(self, placeholder_text="Nome do montador", width=400, height=45, font=("Arial", 16))
        self.montador.pack(pady=10)

        self.cliente = ctk.CTkEntry(self, placeholder_text="Nome do cliente", width=400, height=45, font=("Arial", 16))
        self.cliente.pack(pady=10)

        self.regiao = ctk.CTkEntry(self, placeholder_text="Região da obra", width=400, height=45, font=("Arial", 16))
        self.regiao.pack(pady=10)

        self.valor_total = ctk.CTkEntry(self, placeholder_text="Valor da casa", width=400, height=45, font=("Arial", 16))
        self.valor_total.pack(pady=10)
        self.valor_total.bind("<KeyRelease>", formatar_entry_moeda)

        ctk.CTkButton(self, text="Salvar", width=200, height=45, command=self.salvar_obra).pack(pady=20)
        ctk.CTkButton(self, text="Voltar", width=200, height=45, command=lambda: controller.mostrar_tela(Menu)).pack(pady=20)

    def salvar_obra(self):
        nome = self.nome.get().strip()
        montador = self.montador.get().strip()
        cliente = self.cliente.get().strip()
        regiao = self.regiao.get().strip()

        if not nome or not montador or not cliente or not regiao:
            msg.showerror("Erro", "Preencha todos os campos.")
            return

        try:
            valor_total = converter_moeda_para_float(self.valor_total.get())
        except ValueError:
            msg.showerror("Erro", "Digite valores válidos.")
            return

        adicionar_obra(nome, montador, cliente, regiao, valor_total)

        msg.showinfo("Sucesso", "Obra registrada com sucesso!")

        self.nome.delete(0, "end")
        self.montador.delete(0, "end")
        self.cliente.delete(0, "end")
        self.regiao.delete(0, "end")
        self.valor_total.delete(0, "end")

        self.controller.mostrar_tela(Menu)


# =============================
# DELETAR
# =============================

class Deletar(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        titulo = ctk.CTkLabel(
            self,
            text="Deletar trabalhador",
            font=("Arial", 28, "bold")
        )
        titulo.pack(pady=30)

        self.lista_frame = ctk.CTkScrollableFrame(self)
        self.lista_frame.pack(fill="both", expand=True, padx=200, pady=20)

        ctk.CTkButton(
            self,
            text="Voltar",
            width=200,
            height=45,
            command=lambda: controller.mostrar_tela(Menu)
        ).pack(pady=20)

    def atualizar_lista(self):
        for widget in self.lista_frame.winfo_children():
            widget.destroy()

        trabalhadores = listar_trabalhadores()

        if not trabalhadores:
            ctk.CTkLabel(
                self.lista_frame,
                text="Nenhum trabalhador cadastrado",
                font=("Arial", 16)
            ).pack(pady=20)
            return

        for trabalhador in trabalhadores:
            ctk.CTkButton(
                self.lista_frame,
                text=trabalhador["nome"],
                height=50,
                font=("Arial", 16),
                fg_color="red",
                command=lambda t=trabalhador: self.confirmar(t)
            ).pack(fill="x", pady=8, padx=20)

    def confirmar(self, trabalhador):
        resposta = msg.askyesno(
            "Confirmar exclusão",
            f"Deseja realmente excluir {trabalhador['nome']}?"
        )

        if resposta:
            deletar_trabalhador(trabalhador["id"])
            self.atualizar_lista()

class DeletarObra(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        titulo = ctk.CTkLabel(
            self,
            text="Deletar obra",
            font=("Arial", 28, "bold")
        )
        titulo.pack(pady=30)

        self.lista_frame = ctk.CTkScrollableFrame(self)
        self.lista_frame.pack(fill="both", expand=True, padx=200, pady=20)

        ctk.CTkButton(
            self,
            text="Voltar",
            width=200,
            height=45,
            command=lambda: controller.mostrar_tela(Menu)
        ).pack(pady=20)

    def atualizar_lista(self):
        for widget in self.lista_frame.winfo_children():
            widget.destroy()

        obras = listar_obras()

        if not obras:
            ctk.CTkLabel(
                self.lista_frame,
                text="Nenhuma obra cadastrada",
                font=("Arial", 16)
            ).pack(pady=20)
            return

        for obra in obras:
            ctk.CTkButton(
                self.lista_frame,
                text=obra["nome"],
                height=50,
                font=("Arial", 16),
                fg_color="red",
                command=lambda o=obra: self.confirmar(o)
            ).pack(fill="x", pady=8, padx=20)

    def confirmar(self, obra):
        resposta = msg.askyesno(
            "Confirmar exclusão",
            f"Deseja realmente excluir {obra['nome']}?"
        )

        if resposta:
            remover_obra(obra["id"])
            self.atualizar_lista()


# =============================
# GERENCIAR LISTA
# =============================

class Gerenciar(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        titulo = ctk.CTkLabel(
            self,
            text="Gerenciar trabalhadores",
            font=("Arial", 28, "bold")
        )
        titulo.pack(pady=30)

        self.lista_frame = ctk.CTkScrollableFrame(self)
        self.lista_frame.pack(fill="both", expand=True, padx=200, pady=20)

        ctk.CTkButton(
            self,
            text="Voltar",
            width=200,
            height=45,
            command=lambda: controller.mostrar_tela(Menu)
        ).pack(pady=20)

    def atualizar_lista(self):
        for widget in self.lista_frame.winfo_children():
            widget.destroy()

        trabalhadores = listar_trabalhadores()

        if not trabalhadores:
            ctk.CTkLabel(
                self.lista_frame,
                text="Nenhum trabalhador cadastrado",
                font=("Arial", 16)
            ).pack(pady=20)
            return

        for trabalhador in trabalhadores:
            ctk.CTkButton(
                self.lista_frame,
                text=trabalhador["nome"],
                height=50,
                font=("Arial", 16),
                command=lambda t=trabalhador: self.abrir(t)
            ).pack(fill="x", pady=8, padx=20)

    def abrir(self, trabalhador):
        self.controller.trabalhador_atual = trabalhador
        self.controller.mostrar_tela(GerenciarTrabalhador)


# =============================
# GERENCIAR TRABALHADOR
# =============================

class GerenciarTrabalhador(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Título maior
        self.titulo = ctk.CTkLabel(self, text="", font=("Arial", 32, "bold"))
        self.titulo.pack(pady=30)

        # Frame principal ocupando tudo
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=60, pady=20)

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        self.criar_card_salario()
        self.criar_card_historico()

        ctk.CTkButton(
            self,
            text="Voltar",
            height=45,
            command=lambda: controller.mostrar_tela(Gerenciar)
        ).pack(pady=20)

    # -------------------------
    # UI
    # -------------------------

    def criar_card_salario(self):
        self.card_salario = ctk.CTkFrame(self.main_frame, corner_radius=20)
        self.card_salario.grid(row=0, column=0, padx=30, pady=20, sticky="nsew")

        self.card_salario.grid_rowconfigure(8, weight=1)

        ctk.CTkLabel(
            self.card_salario,
            text="Salário",
            font=("Arial", 20, "bold")
        ).pack(pady=10)

        self.salario_valor = ctk.CTkLabel(
            self.card_salario,
            text="R$ 0,00",
            font=("Arial", 28, "bold"),
            text_color="#4CAF50"
        )
        self.salario_valor.pack(pady=5)

        self.saldo_label = ctk.CTkLabel(
            self.card_salario,
            text="",
            font=("Arial", 18)
        )
        self.saldo_label.pack(pady=5)

        self.salario_entry = ctk.CTkEntry(
            self.card_salario,
            placeholder_text="Novo salário",
            height=40,
            font=("Arial", 16)
        )
        self.salario_entry.pack(pady=10)

        self.salario_entry.bind("<KeyRelease>", formatar_entry_moeda)

        ctk.CTkButton(
            self.card_salario,
            text="Salvar salário",
            height=40,
            command=self.salvar_salario
        ).pack(pady=5)

        ctk.CTkLabel(
            self.card_salario,
            text="Resgatar vale",
            font=("Arial", 20, "bold")
        ).pack(pady=20)

        self.resgatar_entry = ctk.CTkEntry(
            self.card_salario,
            placeholder_text="Valor do vale",
            height=40,
            font=("Arial", 16)
        )
        self.resgatar_entry.pack(pady=5)

        self.resgatar_entry.bind("<KeyRelease>", formatar_entry_moeda)

        ctk.CTkButton(
            self.card_salario,
            text="Resgatar",
            height=40,
            command=self.resgatar_vale
        ).pack(pady=5)

        ctk.CTkButton(
            self.card_salario,
            text="Reiniciar histórico",
            fg_color="red",
            height=40,
            command=self.limpar_historico
        ).pack(pady=20)

    def criar_card_historico(self):
        self.card_historico = ctk.CTkFrame(self.main_frame, corner_radius=20)
        self.card_historico.grid(row=0, column=1, padx=30, pady=20, sticky="nsew")

        ctk.CTkLabel(
            self.card_historico,
            text="Histórico de Vales",
            font=("Arial", 22, "bold")
        ).pack(pady=15)

        self.lista_vales = ctk.CTkScrollableFrame(
            self.card_historico
        )
        self.lista_vales.pack(fill="both", expand=True, padx=15, pady=10)

    # -------------------------
    # LÓGICA 
    # -------------------------

    def carregar_trabalhador(self):
        trabalhadores = listar_trabalhadores()

        for t in trabalhadores:
            if t["id"] == self.controller.trabalhador_atual["id"]:
                self.controller.trabalhador_atual = t
                break

        trabalhador = self.controller.trabalhador_atual

        self.titulo.configure(text=f"{trabalhador['nome']}")

        salario = trabalhador.get("salario", 0)
        saldo = calcular_saldo(trabalhador)

        self.salario_valor.configure(text=f"R$ {formatar_moeda(salario)}")
        self.saldo_label.configure(
            text=f"Saldo a receber: R$ {formatar_moeda(saldo)}"
        )

        self.atualizar_historico()

    def salvar_salario(self):
        try:
            valor = converter_moeda_para_float(self.salario_entry.get())
            definir_salario(self.controller.trabalhador_atual["id"], valor)
            self.salario_entry.delete(0, "end")
            self.carregar_trabalhador()
        except ValueError:
            msg.showerror("Erro", "Digite um valor válido.")

    def resgatar_vale(self):
        try:
            valor = converter_moeda_para_float(self.resgatar_entry.get())
            adicionar_vale(self.controller.trabalhador_atual["id"], valor)
            self.resgatar_entry.delete(0, "end")
            self.carregar_trabalhador()
        except ValueError:
            msg.showerror("Erro", "Digite um valor válido.")

    def atualizar_historico(self):
        for widget in self.lista_vales.winfo_children():
            widget.destroy()

        trabalhador = self.controller.trabalhador_atual
        vales = trabalhador.get("vales", [])

        if not vales:
            ctk.CTkLabel(
                self.lista_vales,
                text="Nenhum vale registrado",
                font=("Arial", 16)
            ).pack(pady=20)
            return

        for index, vale in enumerate(vales):
            frame = ctk.CTkFrame(self.lista_vales, corner_radius=12)
            frame.pack(fill="x", pady=8, padx=5)

            texto = f"R$ {formatar_moeda(vale['valor'])} - {vale['data']} {vale['hora']}"

            ctk.CTkLabel(
                frame,
                text=texto,
                font=("Arial", 16)
            ).pack(side="left", padx=15, pady=8)

            ctk.CTkButton(
                frame,
                text="X",
                width=35,
                height=30,
                fg_color="red",
                command=lambda i=index: self.remover_vale(i)
            ).pack(side="right", padx=10)

    def remover_vale(self, index):
        remover_vale(self.controller.trabalhador_atual["id"], index)
        self.carregar_trabalhador()

    def limpar_historico(self):
        if msg.askyesno(
            "Confirmação",
            "Deseja realmente limpar todo o histórico?"
        ):
            limpar_vales(self.controller.trabalhador_atual["id"])
            self.carregar_trabalhador()

# =============================
# Gerenciar Obras
# =============================

class GerenciarObras(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.controller.obra_atual = None

        self.titulo = ctk.CTkLabel(
            self,
            text="Gerenciar Obras",
            font=("Arial", 32, "bold")
        )
        self.titulo.pack(pady=30)

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=60, pady=20)

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

        self.lista_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.lista_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.card_info = ctk.CTkFrame(self.main_frame, corner_radius=20)
        self.card_info.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.criar_card_info()

        ctk.CTkButton(
            self,
            text="Voltar",
            height=45,
            command=lambda: controller.mostrar_tela(Menu)
        ).pack(pady=20)

    # =========================
    # UI
    # =========================

    def criar_card_info(self):
        for widget in self.card_info.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self.card_info,
            text="Informações da Obra",
            font=("Arial", 20, "bold")
        ).pack(pady=10)

        self.info_label = ctk.CTkLabel(
            self.card_info,
            text="Selecione uma obra",
            font=("Arial", 16)
        )
        self.info_label.pack(pady=5)

        self.pagamento_entry = ctk.CTkEntry(
            self.card_info,
            placeholder_text="Valor do pagamento",
            height=40
        )
        self.pagamento_entry.pack(pady=10)

        # ADICIONADO
        self.pagamento_entry.bind("<KeyRelease>", formatar_entry_moeda)

        ctk.CTkButton(
            self.card_info,
            text="Registrar pagamento",
            command=self.registrar_pagamento
        ).pack(pady=5)

        ctk.CTkLabel(
            self.card_info,
            text="Histórico de Pagamentos",
            font=("Arial", 18, "bold")
        ).pack(pady=15)

        self.lista_pagamentos = ctk.CTkScrollableFrame(self.card_info)
        self.lista_pagamentos.pack(fill="both", expand=True, padx=10, pady=10)

    # =========================
    # LÓGICA
    # =========================

    def atualizar_lista(self):
        for widget in self.lista_frame.winfo_children():
            widget.destroy()

        obras = listar_obras()

        if not obras:
            ctk.CTkLabel(
                self.lista_frame,
                text="Nenhuma obra cadastrada",
                font=("Arial", 16)
            ).pack(pady=20)
            return

        for obra in obras:
            ctk.CTkButton(
                self.lista_frame,
                text=obra["nome"],
                height=50,
                font=("Arial", 16),
                command=lambda o=obra: self.selecionar_obra(o)
            ).pack(fill="x", pady=8, padx=10)

    def selecionar_obra(self, obra):
        self.controller.obra_atual = obra
        self.carregar_obra()

    def carregar_obra(self):
        obras = carregar_obras()
        self.pagamento_entry.bind("<KeyRelease>", formatar_entry_moeda)

        for o in obras:
            if o["id"] == self.controller.obra_atual["id"]:
                self.controller.obra_atual = o
                break

        obra = self.controller.obra_atual

        saldo = float(obra["valor_total"]) - float(obra["valor_pago"])

        # limpa antes
        for widget in self.card_info.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self.card_info,
            text=obra["nome"],
            font=("Arial", 26, "bold")
        ).pack(pady=10)

        ctk.CTkLabel(
            self.card_info,
            text=f"Cliente: {obra['cliente']}",
            font=("Arial", 16)
        ).pack()

        ctk.CTkLabel(
            self.card_info,
            text=f"Montador: {obra['montador']}",
            font=("Arial", 16)
        ).pack(pady=5)

        ctk.CTkLabel(
            self.card_info,
            text=f"Região: {obra['regiao']}",
            font=("Arial", 16)
        ).pack(pady=2)

        # VALOR TOTAL
        ctk.CTkLabel(
            self.card_info,
            text=f"Valor Total\nR$ {formatar_moeda(obra['valor_total'])}",
            font=("Arial", 22, "bold"),
            text_color="#4CAF50"
        ).pack(pady=5)

        # JÁ PAGO
        ctk.CTkLabel(
            self.card_info,
            text=f"Já Pago\nR$ {formatar_moeda(obra['valor_pago'])}",
            font=("Arial", 18),
            text_color="#4CAF50"
        ).pack(pady=5)

        # FALTA
        ctk.CTkLabel(
            self.card_info,
            text=f"Falta Pagar\nR$ {formatar_moeda(saldo)}",
            font=("Arial", 18),
            text_color="#FF5252"
        ).pack(pady=10)

        # Entrada
        self.pagamento_entry = ctk.CTkEntry(
            self.card_info,
            placeholder_text="Valor do pagamento",
            height=40
        )
        self.pagamento_entry.pack(pady=10)

        # ADICIONADO
        self.pagamento_entry.bind("<KeyRelease>", formatar_entry_moeda)

        ctk.CTkButton(
            self.card_info,
            text="Registrar pagamento",
            height=40,
            command=self.registrar_pagamento
        ).pack(pady=5)

        # HISTÓRICO
        ctk.CTkLabel(
            self.card_info,
            text="Histórico de Pagamentos",
            font=("Arial", 18, "bold")
        ).pack(pady=15)

        self.lista_pagamentos = ctk.CTkScrollableFrame(self.card_info)
        self.lista_pagamentos.pack(fill="both", expand=True, padx=10, pady=10)

        self.atualizar_historico()

    def registrar_pagamento(self):
        try:
            valor = converter_moeda_para_float(self.pagamento_entry.get())
            registrar_pagamento(self.controller.obra_atual["id"], valor)
            self.pagamento_entry.delete(0, "end")
            self.carregar_obra()
        except ValueError:
            msg.showerror("Erro", "Digite um valor válido.")

    def atualizar_historico(self):
        for widget in self.lista_pagamentos.winfo_children():
            widget.destroy()

        obra = self.controller.obra_atual
        pagamentos = obra.get("pagamentos", [])

        if not pagamentos:
            ctk.CTkLabel(
                self.lista_pagamentos,
                text="Nenhum pagamento registrado",
                font=("Arial", 14)
            ).pack(pady=10)
            return

        for index, pagamento in enumerate(pagamentos):
            frame = ctk.CTkFrame(self.lista_pagamentos, corner_radius=12)
            frame.pack(fill="x", pady=8, padx=5)

            texto = (
                f"R$ {formatar_moeda(pagamento['valor'])} "
                f"- {pagamento['data']} {pagamento['hora']}"
            )

            ctk.CTkLabel(
                frame,
                text=texto,
                font=("Arial", 15),
            ).pack(side="left", padx=15, pady=8)

            ctk.CTkButton(
                frame,
                text="X",
                width=35,
                height=30,
                fg_color="red",
                command=lambda i=index: self.remover_pagamento(i)
            ).pack(side="right", padx=10)

    def remover_pagamento(self, index):
        if msg.askyesno(
            "Confirmar exclusão",
            "Deseja realmente excluir este pagamento?"
        ):
            remover_pagamento_obra(
                self.controller.obra_atual["id"],
                index
            )
            self.carregar_obra()

# =============================
# APP
# =============================

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Vale")

        # Tamanho mínimo
        self.minsize(900, 600)

        # Abrir maximizado
        self.state("zoomed")

        # Centralizar caso não esteja maximizado
        self.eval('tk::PlaceWindow . center')

        # Container principal
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        # IMPORTANTE: tornar grid expansível
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.telas = {}

        for Tela in (Menu, Registro, RegistrarObra, Deletar, DeletarObra, Gerenciar, GerenciarTrabalhador, GerenciarObras):
            frame = Tela(self.container, self)
            self.telas[Tela] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.menu = self.telas[Menu]
        self.mostrar_tela(Menu)

    def mostrar_tela(self, tela):
        frame = self.telas[tela]

        if hasattr(frame, "atualizar_lista"):
            frame.atualizar_lista()

        if hasattr(frame, "carregar_trabalhador"):
            frame.carregar_trabalhador()

        frame.tkraise()

# =============================
# EXECUÇÃO
# =============================

app = App()
app.mainloop()
