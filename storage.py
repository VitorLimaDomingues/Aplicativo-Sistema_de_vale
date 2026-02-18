import json
import os
from datetime import datetime

ARQUIVO_DADOS = "data.json"

def carregar_dados():
    if not os.path.exists(ARQUIVO_DADOS):
        return {"trabalhadores": []}
    
    with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)
    
def salvar_dados(dados):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)
    
def adicionar_trabalhador(nome):
    dados = carregar_dados()

    novo_trabalhador = {
        "id": len(dados["trabalhadores"]) + 1,
        "nome": nome
    }

    dados["trabalhadores"].append(novo_trabalhador)
    salvar_dados(dados)

    return novo_trabalhador


def deletar_trabalhador(id_trabalhador):
    dados = carregar_dados()

    dados["trabalhadores"] = [
        t for t in dados["trabalhadores"] if t["id"] != id_trabalhador
    ]

    salvar_dados(dados)

def listar_trabalhadores():
    dados = carregar_dados()
    return dados["trabalhadores"]

def definir_salario(trabalhador_id, salario):
    dados = carregar_dados()

    for t in dados["trabalhadores"]:
        if t["id"] == trabalhador_id:
            t["salario"] = salario
            t.setdefault("values", [])
            salvar_dados(dados)
            return True
        
    return False

def adicionar_vale(trabalhador_id, valor):
    dados =  carregar_dados()

    agora = datetime.now()

    for t in dados["trabalhadores"]:
        if t["id"] == trabalhador_id:
            t.setdefault("vales", []).append({
                "valor": valor,
                "data": agora.strftime("%d-%m-%Y"),
                "hora": agora.strftime("%H:%M")
            })
            salvar_dados(dados)
            return True
        
    return False
    
def calcular_saldo(trabalhador):
    salario = trabalhador.get("salario", 0)
    vales = trabalhador.get("vales", [])

    total_vales = sum(v["valor"] for v in vales)

    return salario - total_vales

def remover_vale(trabalhador_id, index_vale):
    dados = carregar_dados()

    for t in dados["trabalhadores"]:
        if t["id"] == trabalhador_id:
            if 0 <= index_vale < len(t.get("vales", [])):
                t["vales"].pop(index_vale)
                salvar_dados(dados)
                return True
            
    return False

def limpar_vales(trabalhador_id):
    dados = carregar_dados()

    for t in dados["trabalhadores"]:
        if t["id"] == trabalhador_id:
            t["vales"] = []
            salvar_dados(dados)
            return True
        
    return False