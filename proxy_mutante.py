import asyncio
import aiohttp
import re
import time
import random
import os
import json
import urllib3

# Protocolo de Silêncio
urllib3.disable_warnings()

# ==============================================================================
# CONFIGURAÇÃO: NÚCLEO OPERACIONAL (ENTIDADE 12)
# ==============================================================================
LIMITADOR_CONEXOES = 1500  # Quantas conexões simultâneas a máquina aguenta
TIMEOUT_TESTE = aiohttp.ClientTimeout(total=5)

ALVOS_VELOCIDADE = [
    "http://cloudflare.com/cdn-cgi/trace",
    "http://1.1.1.1/cdn-cgi/trace"
]
ALVOS_ANONIMATO = [
    "http://httpbin.org/get",
    "http://azenv.net/",
    "http://ip-api.com/json/"
]

REGEX_IP_PORTA = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}:[0-9]{2,5}\b')
REGEX_PAIS = re.compile(r'loc=([A-Z]{2})')

# /SOMBRA: Arsenal de Agentes Disfarçados
AGENTES = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
]

# Telemetria Secreta
WEBHOOK_URL = os.getenv('WEBHOOK_URL', '')

# FROTA TOTAL (Com vírgulas corrigidas e padronizadas)
FROTA_TOTAL = [
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=5000&country=all&ssl=all&anonymity=elite",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=elite",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=5000&country=all&ssl=all&anonymity=elite",
    "https://www.proxy-list.download/api/v1/get?type=socks5",
    "https://www.proxy-list.download/api/v1/get?type=https",
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://api.openproxylist.xyz/socks5.txt",
    "https://api.openproxylist.xyz/http.txt",
    "https://spys.me/proxy.txt",
    "https://spys.me/socks.txt",
    "https://proxyspace.pro/http.txt",
    "https://proxyspace.pro/https.txt",
    "https://proxyspace.pro/socks4.txt",
    "https://proxyspace.pro/socks5.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/socks5/data.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/http/data.txt",
    "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/SOCKS5.txt",
    "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/HTTP.txt",
    "https://raw.githubusercontent.com/UserR3X/proxy-list/main/online/http.txt",
    "https://raw.githubusercontent.com/UserR3X/proxy-list/main/online/socks4.txt",
    "https://raw.githubusercontent.com/UserR3X/proxy-list/main/online/socks5.txt",
    "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/socks5.txt",
    "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/http.txt",
    "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
    "https://raw.githubusercontent.com/manuGMG/proxy-365/main/SOCKS5.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks5/socks5.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks4/socks4.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt",
    "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks5.txt",
    "https://raw.githubusercontent.com/zloi-user/hideip.me/main/http.txt",
    "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/socks5.txt",
    "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks5.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt",
    "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/generated/socks5_proxies.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/generated/http_proxies.txt",
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
    "https://raw.githubusercontent.com/komutan234/Proxy-List-Free/main/proxies/http.txt",
    "https://raw.githubusercontent.com/komutan234/Proxy-List-Free/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/komutan234/Proxy-List-Free/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt",
    "https://raw.githubusercontent.com/proxylist-to/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/proxylist-to/proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/proxylist-to/proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/http.txt",
    "https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/socks5.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/http_proxies.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/socks5_proxies.txt",
    "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks5.txt",
    "https://raw.githubusercontent.com/caliphdev/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/caliphdev/Proxy-List/master/socks5.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/uProxy/public-proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/wiki/gfpcom/free-proxy-list/lists/socks5.txt",
    "https://raw.githubusercontent.com/Ian-Lusule/Proxies/main/proxies/all_proxies.txt",
    "https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-Repo/master/proxy_list.txt",
    "https://raw.githubusercontent.com/Toffanello/Free-Proxy-List/main/proxies.txt",
    "https://alexa.lr2b.com/proxylist.txt",
    "https://multiproxy.org/txt_all/proxy.txt",
    "https://raw.githubusercontent.com/tbbt-proxy/proxies/main/socks5.txt",
    "https://raw.githubusercontent.com/yuceltoluyag/GoodProxy/main/proxies.txt",
    "https://raw.githubusercontent.com/almroot/proxylist/master/list.txt",
    "https://raw.githubusercontent.com/scuxi/free-proxy-list/main/proxy.txt",
    "https://raw.githubusercontent.com/saisuiu/Configs-All/main/proxies/free.txt",
    "https://raw.githubusercontent.com/v1k0d3n/proxies/main/socks5.txt",
    "https://raw.githubusercontent.com/v1k0d3n/proxies/main/http.txt",
    "https://raw.githubusercontent.com/elliottophellia/yakumo/master/results/socks5/global/socks5_checked.txt",
    "https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list",
    "https://raw.githubusercontent.com/orx77/proxies/main/socks5.txt",
    "https://api.proxyscrape.com/v3/free-proxy-list/get?request=getproxies&protocol=socks5&proxy_format=ipport&format=text",
    "https://api.proxyscrape.com/v3/free-proxy-list/get?request=getproxies&protocol=http&proxy_format=ipport&format=text",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/socks4_proxies.txt",
    "https://raw.githubusercontent.com/hookzof/socks4_list/master/proxy.txt",
    "https://raw.githubusercontent.com/obhai/Proxy-List/main/socks4.txt",
    "https://raw.githubusercontent.com/obhai/Proxy-List/main/socks5.txt",
    "https://raw.githubusercontent.com/obhai/Proxy-List/main/http.txt"
]

def obter_headers():
    return {'User-Agent': random.choice(AGENTES), 'Connection': 'keep-alive'}

async def raspar_site(session, url):
    url_lower = url.lower()
    proto = "socks5" if "socks5" in url_lower else "socks4" if "socks4" in url_lower else "http"
    try:
        async with session.get(url, headers=obter_headers(), ssl=False) as res:
            if res.status == 200:
                texto = await res.text()
                ips = REGEX_IP_PORTA.findall(texto)
                return [(proto, ip) for ip in set(ips)]
    except:
        pass
    return []

async def testar_proxy(sem, session, proto, ip):
    async with sem:
        proxy_url = f"{proto}://{ip}"
        alvo_vel = random.choice(ALVOS_VELOCIDADE)
        
        try:
            inicio = time.time()
            async with session.get(alvo_vel, proxy=proxy_url, timeout=TIMEOUT_TESTE, ssl=False) as res_vel:
                if res_vel.status != 200:
                    return None
                
                texto_vel = await res_vel.text()
                latencia = int((time.time() - inicio) * 1000)
                
                match_loc = REGEX_PAIS.search(texto_vel)
                pais = match_loc.group(1) if match_loc else "XX"
                
                is_elite = False
                alvo_anon = random.choice(ALVOS_ANONIMATO)
                
                try:
                    async with session.get(alvo_anon, proxy=proxy_url, timeout=TIMEOUT_TESTE, ssl=False) as res_anon:
                        if res_anon.status == 200:
                            is_elite = True 
                except:
                    pass
                
                return (proto, ip, latencia, is_elite, pais)
        except:
            pass
        return None

async def disparar_telemetria(mensagem):
    if not WEBHOOK_URL:
        return
    async with aiohttp.ClientSession() as session:
        payload = {"content": f"**[IMPÉRIO MUTANTE - ALERTA TÁTICO]**\n{mensagem}"}
        try:
            await session.post(WEBHOOK_URL, json=payload)
        except:
            pass

async def mutacao_principal():
    inicio_geral = time.time()
    print("[+] PROTOCOLO /MUTAR V4 ATIVADO: OVERCLOCK ASSÍNCRONO [+]")
    
    async with aiohttp.ClientSession() as session:
        tarefas_raspagem = [raspar_site(session, url) for url in FROTA_TOTAL]
        resultados_raspagem = await asyncio.gather(*tarefas_raspagem)
        
        todos_proxies = []
        for res in resultados_raspagem:
            todos_proxies.extend(res)
            
        todos_proxies = list(set(todos_proxies))
        print(f"[+] CARRASCO: {len(todos_proxies)} IPs extraídos. Iniciando auditoria...")

    vivos = {"socks5": [], "elite_socks5": [], "geo_paises": []}
    
    sem = asyncio.Semaphore(LIMITADOR_CONEXOES)
    connector = aiohttp.TCPConnector(limit=LIMITADOR_CONEXOES, ssl=False)
    
    async with aiohttp.ClientSession(connector=connector) as session:
        tarefas_teste = [testar_proxy(sem, session, p, ip) for p, ip in todos_proxies[:15000]]
        resultados_teste = await asyncio.gather(*tarefas_teste)
        
        for resultado in resultados_teste:
            if resultado:
                proto, ip, latencia, is_elite, pais = resultado
                vivos.setdefault(proto, []).append((latencia, ip))
                vivos.setdefault("geo_paises", []).append((latencia, f"{ip}:{pais}"))
                if is_elite:
                    vivos.setdefault(f"elite_{proto}", []).append((latencia, ip))

    resumo_logs = []
    for chave, dados in vivos.items():
        if dados:
            ips_ordenados = list(dict.fromkeys([item[1] for item in sorted(dados)]))
            with open(f"{chave}.txt", "w") as f:
                f.write("\n".join(ips_ordenados))
            resumo_logs.append(f"- **{chave.upper()}**: {len(ips_ordenados)} nós ativos.")
    
    tempo_total = time.time() - inicio_geral
    relatorio = f"Rotação concluída em {tempo_total:.2f}s.\n" + "\n".join(resumo_logs)
    print(relatorio)
    await disparar_telemetria(relatorio)

if __name__ == "__main__":
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(mutacao_principal())
