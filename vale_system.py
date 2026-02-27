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
    salvar_obras,
    gerar_novo_id_obra,
    adicionar_obra,
    listar_obras,
    registrar_pagamento
)

from utils import formatar_moeda, converter_moeda_para_float


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

        self.nome = ctk.CTkEntry(
            self,
            placeholder_text="Nome da obra",
            width=400,
            height=45,
            font=("Arial", 16)
        )
        self.nome.pack(pady=10)

        self.montador = ctk.CTkEntry(
            self,
            placeholder_text="Nome do montador",
            width=400,
            height=45,
            font=("Arial", 16)
        )
        self.montador.pack(pady=10)

        self.cliente = ctk.CTkEntry(
            self,
            placeholder_text="Nome do cliente",
            width=400,
            height=45,
            font=("Arial", 16)
        )
        self.cliente.pack(pady=10)

        self.regiao = ctk.CTkEntry(
            self,
            placeholder_text="Região da obra",
            width=400,
            height=45,
            font=("Arial", 16)
        )
        self.regiao.pack(pady=10)

        self.salario_montador = ctk.CTkEntry(
            self,
            placeholder_text="Salário do montador",
            width=400,
            height=45,
            font=("Arial", 16)
        )
        self.salario_montador.pack(pady=10)

        self.valor_total = ctk.CTkEntry(
            self,
            placeholder_text="Valor da casa",
            width=400,
            height=45,
            font=("Arial", 16)
        )
        self.valor_total.pack(pady=10)

        ctk.CTkButton(
            self,
            text="Salvar",
            width=200,
            height=45,
            command=self.salvar_obra
        ).pack(pady=20)


        ctk.CTkButton(
            self,
            text="Voltar",
            width=200,
            height=45,
            command=lambda: controller.mostrar_tela(Menu)
        ).pack(pady=20)

    def salvar_obra(self):
        nome = self.nome.get().strip()
        montador = self.montador.get().strip()
        cliente = self.cliente.get().strip()
        regiao = self.regiao.get().strip()
        salario_montador = self.salario_montador.get().strip()
        valor_total = self.valor_total.get().strip()

        if not nome or not montador or not cliente or not regiao or not salario_montador or not valor_total:
            msg.showerror("Error", "Preencha todos os campos.")
            return
        
        adicionar_obra(nome, montador, cliente, regiao, salario_montador, valor_total)

        msg.showinfo("Sucesso", "Obra registrada com sucesso!")

        self.nome.delete(0, "end")
        self.montador.delete(0, "end")
        self.cliente.delete(0, "end")
        self.regiao.delete(0, "end")
        self.salario_montador.delete(0, "end")
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
# GERENCIAR OBRAS
# =============================
class GerenciarObras(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller


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

        for Tela in (Menu, Registro, RegistrarObra, Deletar, Gerenciar, GerenciarTrabalhador, GerenciarObras):
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
