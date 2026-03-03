from fastapi import FastAPI
from typing import Optional

app = FastAPI(
    title="Bella Tavola API",
    description="API do restaurante Bella Tavola",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {
        "restaurante": "Bella Tavola",
        "mensagem": "Bem-vindo à nossa API",
        "chef": "Marco Rossi",
        "cidade": "São Paulo",
        "especialidade": "Massas artesanais"
    }

pratos = [
    {"id": 1, "nome": "Margherita", "categoria": "pizza", "preco": 45.0, "disponivel": True},
    {"id": 2, "nome": "Carbonara", "categoria": "massa", "preco": 52.0, "disponivel": False},
    {"id": 3, "nome": "Tiramisù", "categoria": "sobremesa", "preco": 28.0, "disponivel": True},
    {"id": 4, "nome": "Lasagna alla Bolognese", "categoria": "massa", "preco": 55.0, "disponivel": True},
    {"id": 5, "nome": "Cannoli", "categoria": "sobremesa", "preco": 22.0, "disponivel": False},
    {"id": 6, "nome": "Panna Cotta", "categoria": "sobremesa", "preco": 25.0, "disponivel": True},
]

@app.get("/pratos")
async def listar_pratos():
    return pratos

@app.get("/pratos/{prato_id}")
async def buscar_prato(prato_id: int, formato: str = "completo"):
    for prato in pratos:
        if prato["id"] == prato_id:
            if formato == "resumido":
                return {"nome": prato["nome"], "preco": prato["preco"]}
            return prato
    return {"mensagem": "Prato não encontrado"}

    # Quando aparece o status 200 para um recuso que não existe, os cliente que só verificando o status code podem pensar que a requisição foi bem sucedida
    # Para evitar isso, é recomendado retornar um status code 404 para recursos não encontrados
    # return {"mensagem": "Prato não encontrado"}, 404

@app.get("/pratos/{prato_id}/detalhes")
async def detalhes_prato(
    prato_id: int,
    categoria: Optional[str] = None,
    preco_maximo: Optional[float] = None
    apenas_disponiveis: Optional[bool] = False
    ):

    resultado = pratos

    if categoria:
        resultado = [p for p in resultado if p["categoria"] == categoria]

    if preco_maximo is not None:
        resultado = [p for p in resultado if p["preco"] <= preco_maximo]

    if apenas_disponiveis:
        resultado = [p for p in resultado if p["disponivel"]]

    return resultado

@app.get("/pratos/{prato_id}/detalhes")
async def detalhes_prato(prato_id: int, apenas_disponiveis: bool = False):
    for prato in pratos:
        if prato["id"] == prato_id:
            if apenas_disponiveis and not prato["disponivel"]:
                return {"mensagem": "Prato não disponível"}
            return prato
    return {"mensagem": "Prato não encontrado"}
