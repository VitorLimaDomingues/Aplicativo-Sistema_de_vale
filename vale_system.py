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
    limpar_vales
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

        titulo = ctk.CTkLabel(self, text="Sistema de Vale", font=FONT_TITULO)
        titulo.pack(pady=30)

        self.msg_label = ctk.CTkLabel(self, text="", text_color="#4CAF50")
        self.msg_label.pack(pady=5)

        self.criar_botao("Registrar trabalhador", Registro)
        self.criar_botao("Gerenciar trabalhadores", Gerenciar)
        self.criar_botao("Deletar trabalhador", Deletar)

    def criar_botao(self, texto, tela):
        botao = ctk.CTkButton(
            self,
            text=texto,
            width=260,
            height=45,
            command=lambda: self.controller.mostrar_tela(tela)
        )
        botao.pack(pady=10)

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

        titulo = ctk.CTkLabel(self, text="Registrar trabalhador", font=FONT_SUBTITULO)
        titulo.pack(pady=30)

        self.nome = ctk.CTkEntry(self, placeholder_text="Nome do trabalhador", width=300)
        self.nome.pack(pady=15)

        ctk.CTkButton(self, text="Registrar", command=self.salvar).pack(pady=10)
        ctk.CTkButton(self, text="Voltar",
                      command=lambda: controller.mostrar_tela(Menu)).pack(pady=20)

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


# =============================
# DELETAR
# =============================

class Deletar(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        titulo = ctk.CTkLabel(self, text="Deletar trabalhador", font=FONT_SUBTITULO)
        titulo.pack(pady=30)

        self.lista_frame = ctk.CTkFrame(self)
        self.lista_frame.pack(pady=20, fill="x")

        ctk.CTkButton(self, text="Voltar",
                      command=lambda: controller.mostrar_tela(Menu)).pack(pady=20)

    def atualizar_lista(self):
        for widget in self.lista_frame.winfo_children():
            widget.destroy()

        trabalhadores = listar_trabalhadores()

        if not trabalhadores:
            ctk.CTkLabel(self.lista_frame,
                         text="Nenhum trabalhador cadastrado").pack(pady=10)
            return

        for trabalhador in trabalhadores:
            ctk.CTkButton(
                self.lista_frame,
                text=trabalhador["nome"],
                width=260,
                command=lambda t=trabalhador: self.confirmar(t)
            ).pack(pady=5)

    def confirmar(self, trabalhador):
        if msg.askyesno("Confirmação",
                        f"Deseja deletar {trabalhador['nome']}?"):
            deletar_trabalhador(trabalhador["id"])
            self.controller.menu.atualizar_mensagem("Trabalhador deletado!")
            self.controller.mostrar_tela(Menu)


# =============================
# GERENCIAR LISTA
# =============================

class Gerenciar(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        titulo = ctk.CTkLabel(self, text="Gerenciar trabalhadores", font=FONT_SUBTITULO)
        titulo.pack(pady=30)

        self.lista_frame = ctk.CTkFrame(self)
        self.lista_frame.pack(pady=20, fill="x")

        ctk.CTkButton(self, text="Voltar",
                      command=lambda: controller.mostrar_tela(Menu)).pack(pady=20)

    def atualizar_lista(self):
        for widget in self.lista_frame.winfo_children():
            widget.destroy()

        trabalhadores = listar_trabalhadores()

        if not trabalhadores:
            ctk.CTkLabel(self.lista_frame,
                         text="Nenhum trabalhador cadastrado").pack(pady=10)
            return

        for trabalhador in trabalhadores:
            ctk.CTkButton(
                self.lista_frame,
                text=trabalhador["nome"],
                width=260,
                command=lambda t=trabalhador: self.abrir(t)
            ).pack(pady=5)

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

        self.titulo = ctk.CTkLabel(self, text="", font=FONT_TITULO)
        self.titulo.pack(pady=20)

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=40, pady=20)

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

        self.criar_card_salario()
        self.criar_card_historico()

        ctk.CTkButton(self, text="Voltar",
                      command=lambda: controller.mostrar_tela(Gerenciar)).pack(pady=20)

    # -------------------------
    # UI
    # -------------------------

    def criar_card_salario(self):
        self.card_salario = ctk.CTkFrame(self.main_frame, corner_radius=15)
        self.card_salario.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        ctk.CTkLabel(self.card_salario, text="Salário", font=FONT_NORMAL).pack()

        self.salario_valor = ctk.CTkLabel(
            self.card_salario,
            text="R$ 0,00",
            font=("Arial", 24, "bold"),
            text_color="#4CAF50"
        )
        self.salario_valor.pack(pady=5)

        self.saldo_label = ctk.CTkLabel(self.card_salario, text="", font=FONT_NORMAL)
        self.saldo_label.pack(pady=5)

        self.salario_entry = ctk.CTkEntry(self.card_salario, placeholder_text="Novo salário")
        self.salario_entry.pack(pady=10)

        ctk.CTkButton(self.card_salario, text="Salvar salário",
                      command=self.salvar_salario).pack(pady=5)

        ctk.CTkLabel(self.card_salario, text="Resgatar vale",
                     font=FONT_SUBTITULO).pack(pady=10)

        self.resgatar_entry = ctk.CTkEntry(self.card_salario,
                                           placeholder_text="Valor do vale")
        self.resgatar_entry.pack(pady=5)

        ctk.CTkButton(self.card_salario, text="Resgatar",
                      command=self.resgatar_vale).pack(pady=5)

        ctk.CTkButton(self.card_salario,
                      text="Reiniciar histórico",
                      fg_color="red",
                      command=self.limpar_historico).pack(pady=10)

    def criar_card_historico(self):
        self.card_historico = ctk.CTkFrame(self.main_frame, corner_radius=15)
        self.card_historico.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        ctk.CTkLabel(self.card_historico,
                     text="Histórico de Vales",
                     font=FONT_SUBTITULO).pack(pady=10)

        self.lista_vales = ctk.CTkScrollableFrame(self.card_historico,
                                                  width=350,
                                                  height=350)
        self.lista_vales.pack(fill="both", expand=True, padx=10, pady=10)

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
            ctk.CTkLabel(self.lista_vales,
                         text="Nenhum vale registrado").pack(pady=10)
            return

        for index, vale in enumerate(vales):
            frame = ctk.CTkFrame(self.lista_vales, corner_radius=10)
            frame.pack(fill="x", pady=5, padx=5)

            texto = f"R$ {formatar_moeda(vale['valor'])} - {vale['data']} {vale['hora']}"
            ctk.CTkLabel(frame, text=texto).pack(side="left", padx=10)

            ctk.CTkButton(
                frame,
                text="X",
                width=30,
                fg_color="red",
                command=lambda i=index: self.remover_vale(i)
            ).pack(side="right", padx=5)

    def remover_vale(self, index):
        remover_vale(self.controller.trabalhador_atual["id"], index)
        self.carregar_trabalhador()

    def limpar_historico(self):
        if msg.askyesno("Confirmação",
                        "Deseja realmente limpar todo o histórico?"):
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

        for Tela in (Menu, Registro, Deletar, Gerenciar, GerenciarTrabalhador):
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
