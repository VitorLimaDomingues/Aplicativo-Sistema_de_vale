import json
import os
import sys
from datetime import datetime

ARQUIVO = "data.json"
ARQUIVO2 = "obra.json"

# =========================
# JSON para app
# =========================

def caminho_arquivo():
    if getattr(sys, 'frozen', False):
        return os.path.join(os.path.dirname(sys.executable), "data.json")
    return "data.json"

def caminho_arquivo():
    if getattr(sys, 'frozen', False):
        return os.path.join(os.path.dirname(sys.executable), "obra.json")
    return "obra.json"

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

# =========================
# OBRA
# =========================

def carregar_obras():
    caminho = caminho_arquivo(ARQUIVO2)

    if not os.path.exist(caminho):
        return []
    
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)
    
def salvar_obras(obras):
    caminho = caminho_arquivo(ARQUIVO2)

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(obras, f, indent=4, ensure_ascii=False)

def gerar_novo_id_obra(obras):
    if not obras:
        return 1
    return max(o["id"] for o in obras) + 1

def adicionar_obra(nome_obra, montador, cliente, regiao, salario_montador, valor_total):
    obras = carregar_obras()

    nova = {
        "id": gerar_novo_id_obra(obras),
        "obra": nome_obra,
        "montador": montador,
        "cliente": cliente,
        "região": regiao,
        "salário do montador": salario_montador,
        "Valor a pagar do cliente": valor_total,
        "Total pago": 0
    }

    obras.append(nova)
    salvar_obras(obras)

def listar_obras():
    return carregar_obras()

def registrar_pagamento(obra_id, valor):
    obras = carregar_obras()
    
    for o in obras:
        if o["id"] == obra_id:
            o["valor_pago"] += valor
            break

    salvar_obras(obras)