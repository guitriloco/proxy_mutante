from fastapi import FastAPI, Header, HTTPException, Query
import httpx
import random
import os

# /SOBERANIA: O front de Batalha
app = FastAPI(
    title="API Império Mutante - Multi-Proxy Gateway",
    description="Motor de Roteamento de Alta Latência Negativa. Vias Expressas Abertas.",
    version="2.0.0"
)

# Seu banco de dados em tempo real (GitHub Raw)
GITHUB_RAW_URL = "https://raw.githubusercontent.com/guitriloco/proxy_mutante/main/"

# /SOMBRA: Catraca de Clientes VIP
CHAVES_AUTORIZADAS = [
    "GUILE_MASTER_KEY_001", 
    "CLIENTE_BETA_999"
]

# Motor Central de Extração (Evita repetir código nas 3 rotas)
async def extrair_proxy_tatico(protocolo: str, pais: str, elite: bool):
    # Lógica de Roteamento
    if pais:
        url_alvo = f"{GITHUB_RAW_URL}paises/{pais.upper()}.txt"
    elif elite:
        url_alvo = f"{GITHUB_RAW_URL}elite_{protocolo}.txt"
    else:
        url_alvo = f"{GITHUB_RAW_URL}{protocolo}.txt"

    # Infiltração e Saque
    async with httpx.AsyncClient() as client:
        resposta = await client.get(url_alvo)
        
        if resposta.status_code != 200:
            raise HTTPException(status_code=404, detail=f"Base de dados [{protocolo.upper()}] inatingível ou país sem nós.")
        
        ips = resposta.text.strip().split('\n')
        if not ips or ips[0] == '':
            raise HTTPException(status_code=404, detail="Sem IPs vivos para o filtro no momento.")
        
        return random.choice(ips)

# Validador de Blindagem
def checar_blindagem(api_key: str):
    if api_key not in CHAVES_AUTORIZADAS:
        raise HTTPException(status_code=401, detail="Cão de guarda ativado: Chave Inválida ou Ausente.")

# ==============================================================================
# AVENIDAS DE ACESSO VIP
# ==============================================================================

@app.get("/v1/http")
async def obter_http(
    api_key: str = Header(None, description="Chave de Acesso VIP"),
    pais: str = Query(None, description="Sigla (ex: BR, US)"),
    elite: bool = Query(False, description="Proxies HTTP Elite")
):
    checar_blindagem(api_key)
    ip_selecionado = await extrair_proxy_tatico("http", pais, elite)
    return {
        "status": "sucesso",
        "protocolo": "http/https",
        "proxy": ip_selecionado,
        "formato": f"http://{ip_selecionado}"
    }

@app.get("/v1/socks4")
async def obter_socks4(
    api_key: str = Header(None, description="Chave de Acesso VIP"),
    pais: str = Query(None, description="Sigla (ex: BR, US)"),
    elite: bool = Query(False, description="Proxies SOCKS4 Elite")
):
    checar_blindagem(api_key)
    ip_selecionado = await extrair_proxy_tatico("socks4", pais, elite)
    return {
        "status": "sucesso",
        "protocolo": "socks4",
        "proxy": ip_selecionado,
        "formato": f"socks4://{ip_selecionado}"
    }

@app.get("/v1/socks5")
async def obter_socks5(
    api_key: str = Header(None, description="Chave de Acesso VIP"),
    pais: str = Query(None, description="Sigla (ex: BR, US)"),
    elite: bool = Query(False, description="Proxies SOCKS5 Elite")
):
    checar_blindagem(api_key)
    ip_selecionado = await extrair_proxy_tatico("socks5", pais, elite)
    return {
        "status": "sucesso",
        "protocolo": "socks5",
        "proxy": ip_selecionado,
        "formato": f"socks5://{ip_selecionado}"
    }
