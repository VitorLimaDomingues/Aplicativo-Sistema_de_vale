import json
import os
import sys
from datetime import datetime

ARQUIVO = "data.json"

# =========================
# JSON para app
# =========================

def caminho_arquivo():
    if getattr(sys, 'frozen', False):
        return os.path.join(os.path.dirname(sys.executable), "data.json")
    return "data.json"


# =========================
# UTILIDADES INTERNAS
# =========================

def carregar_trabalhadores():
    if not os.path.exists(ARQUIVO):
        return []

    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_trabalhadores(trabalhadores):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(trabalhadores, f, indent=4, ensure_ascii=False)


def gerar_novo_id(trabalhadores):
    if not trabalhadores:
        return 1

    maior_id = max(t["id"] for t in trabalhadores)
    return maior_id + 1


# =========================
# CRUD TRABALHADOR
# =========================

def adicionar_trabalhador(nome):
    trabalhadores = carregar_trabalhadores()

    novo = {
        "id": gerar_novo_id(trabalhadores),
        "nome": nome,
        "salario": 0,
        "vales": []
    }

    trabalhadores.append(novo)
    salvar_trabalhadores(trabalhadores)


def listar_trabalhadores():
    return carregar_trabalhadores()


def deletar_trabalhador(trabalhador_id):
    trabalhadores = carregar_trabalhadores()
    trabalhadores = [t for t in trabalhadores if t["id"] != trabalhador_id]
    salvar_trabalhadores(trabalhadores)


# =========================
# SALÁRIO
# =========================

def definir_salario(trabalhador_id, valor):
    trabalhadores = carregar_trabalhadores()

    for t in trabalhadores:
        if t["id"] == trabalhador_id:
            t["salario"] = valor
            break

    salvar_trabalhadores(trabalhadores)


def calcular_saldo(trabalhador):
    salario = trabalhador.get("salario", 0)
    total_vales = sum(v["valor"] for v in trabalhador.get("vales", []))
    return salario - total_vales


# =========================
# VALES
# =========================

def adicionar_vale(trabalhador_id, valor):
    trabalhadores = carregar_trabalhadores()

    for t in trabalhadores:
        if t["id"] == trabalhador_id:
            agora = datetime.now()
            t["vales"].append({
                "valor": valor,
                "data": agora.strftime("%d/%m/%Y"),
                "hora": agora.strftime("%H:%M")
            })
            break

    salvar_trabalhadores(trabalhadores)


def remover_vale(trabalhador_id, index):
    trabalhadores = carregar_trabalhadores()

    for t in trabalhadores:
        if t["id"] == trabalhador_id:
            if 0 <= index < len(t["vales"]):
                t["vales"].pop(index)
            break

    salvar_trabalhadores(trabalhadores)


def limpar_vales(trabalhador_id):
    trabalhadores = carregar_trabalhadores()

    for t in trabalhadores:
        if t["id"] == trabalhador_id:
            t["vales"] = []
            break

    salvar_trabalhadores(trabalhadores)
