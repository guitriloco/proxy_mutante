import requests
import re
import concurrent.futures
import urllib3
import time
import random

# Protocolo de Silêncio SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==============================================================================
# CONFIGURAÇÃO: NÚCLEO OPERACIONAL E AUDITORIA (ENTIDADE 12)
# ==============================================================================
TIMEOUT_EXTRACAO = 4
TIMEOUT_TESTE_BASE = 2   # FASE 3: Alvo de Velocidade Bruta (Cloudflare)
TIMEOUT_TESTE_ELITE = 3  # FASE 2: Alvo de Auditoria de Anonimato (HttpBin)

ALVO_VELOCIDADE = "http://cloudflare.com/cdn-cgi/trace"
ALVO_ANONIMATO = "http://httpbin.org/get"

# /MUTAR: Regex pré-compilado na memória para Latência Negativa em larga escala
REGEX_IP_PORTA = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}:[0-9]{2,5}\b')

AGENTES = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
]

# FASE 1: INGESTÃO DE NOVAS FROTAS (ALTA ROTAÇÃO)
FROTA_TOTAL = list(set([
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=3000&country=all&ssl=all&anonymity=elite",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=3000&country=all&ssl=all&anonymity=elite",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=3000&country=all&ssl=all&anonymity=elite",
    "https://www.proxy-list.download/api/v1/get?type=socks5",
    "https://www.proxy-list.download/api/v1/get?type=https",
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://api.openproxylist.xyz/socks5.txt",
    "https://api.openproxylist.xyz/http.txt",
    "https://api.proxyscrape.com/v3/free-proxy-list/get?request=getproxies&protocol=socks5&proxy_format=ipport&format=text",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/socks5/data.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/http/data.txt",
    "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/SOCKS5.txt",
    "https://raw.githubusercontent.com/B4RC0DE-7/proxy-list/main/SOCKS5.txt",
    "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/socks5.txt",
    "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/socks5.txt",
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
    "https://raw.githubusercontent.com/officialputuid/Proxy-List/master/socks5.txt",
    "https://raw.githubusercontent.com/officialputuid/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks5.txt",
    "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/socks5.txt",
    "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/socks4.txt",
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
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/socks4_proxies.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/socks5_proxies.txt",
    "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks4.txt",
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
    "https://api.proxyscrape.com/v3/free-proxy-list/get?request=getproxies&proxy_format=ipport&format=text",
    "https://raw.githubusercontent.com/tbbt-proxy/proxies/main/socks5.txt",
    "https://raw.githubusercontent.com/yuceltoluyag/GoodProxy/main/proxies.txt",
    "https://raw.githubusercontent.com/almroot/proxylist/master/list.txt",
    "https://raw.githubusercontent.com/scuxi/free-proxy-list/main/proxy.txt",
    "https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/saisuiu/Configs-All/main/proxies/free.txt",
    "https://raw.githubusercontent.com/v1k0d3n/proxies/main/socks5.txt",
    "https://raw.githubusercontent.com/v1k0d3n/proxies/main/http.txt",
    "https://raw.githubusercontent.com/elliottophellia/yakumo/master/results/socks5/global/socks5_checked.txt",
    "https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list",
    "https://raw.githubusercontent.com/orx77/proxies/main/socks5.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/socks4/data.txt",
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt"
]))

def raspar_site(url):
    url_lower = url.lower()
    if "socks5" in url_lower: proto = "socks5"
    elif "socks4" in url_lower: proto = "socks4"
    else: proto = "http"

    # /SOMBRA: Headers expandidos para evitar bloqueios WAF (Web Application Firewall)
    headers = {
        'User-Agent': random.choice(AGENTES),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }
    
    try:
        res = requests.get(url, headers=headers, timeout=TIMEOUT_EXTRACAO, verify=False)
        if res.status_code == 200:
            ips = REGEX_IP_PORTA.findall(res.text)
            return [(proto, ip) for ip in set(ips)]
    except:
        pass
    return []

def auditoria_mutante(item):
    proto, ip = item
    proxies = {"http": f"{proto}://{ip}", "https": f"{proto}://{ip}"}
    
    # FASE 3: Múltiplos Alvos (Teste de Velocidade e Rejeição)
    try:
        inicio_ping = time.time()
        res_vel = requests.get(ALVO_VELOCIDADE, proxies=proxies, timeout=TIMEOUT_TESTE_BASE)
        if res_vel.status_code != 200:
            return None
        
        latencia = int((time.time() - inicio_ping) * 1000)
        is_elite = False

        # FASE 2: Filtro de Elite (Auditoria de Headers e Anonimato)
        try:
            res_anon = requests.get(ALVO_ANONIMATO, proxies=proxies, timeout=TIMEOUT_TESTE_ELITE)
            if res_anon.status_code == 200:
                dados = res_anon.json()
                headers = str(dados.get("headers", {})).lower()
                # Se X-Forwarded-For ou Via estiverem ausentes, o proxy é blindado (Elite)
                if "x-forwarded-for" not in headers and "via" not in headers:
                    is_elite = True
        except:
            pass # Se falhar no httpbin mas passou no Cloudflare, salva normal, mas não é elite.

        # Retorna os dados mapeados para ordenação
        return (proto, ip, latencia, is_elite)
    except:
        pass
    return None

if __name__ == "__main__":
    inicio_geral = time.time()
    print(f"\n[+] PROTOCOLO /MUTAR ATIVADO [+]")
    print(f"[+] INGESTÃO: {len(FROTA_TOTAL)} Fontes de Alta Rotação.")

    todos_proxies = []
    
    # Extração Massiva Multi-thread
    with concurrent.futures.ThreadPoolExecutor(max_workers=80) as executor:
        futuros = {executor.submit(raspar_site, url): url for url in FROTA_TOTAL}
        for futuro in concurrent.futures.as_completed(futuros):
            res = futuro.result()
            if res:
                todos_proxies.extend(res)

    todos_proxies = list(set(todos_proxies))
    
    # Trava de Segurança Custo Zero: Corta excessos para não estourar o limite de tempo do GitHub Actions
    if len(todos_proxies) > 5000:
        todos_proxies = random.sample(todos_proxies, 5000)

    print(f"[+] CARRASCO: {len(todos_proxies)} IPs brutos. Testando contra múltiplos alvos...")

    vivos = {"socks5": [], "socks4": [], "http": [], "elite": []}

    # Teste de Guerra e Classificação
    with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
        futuros_teste = {executor.submit(auditoria_mutante, p): p for p in todos_proxies}
        for futuro in concurrent.futures.as_completed(futuros_teste):
            resultado = futuro.result()
            if resultado:
                proto, ip, latencia, is_elite = resultado
                
                # Guarda no protocolo padrão junto com a latência (para ordenação) APENAS o IP
                vivos[proto].append((latencia, ip))
                
                # /SOBERANIA: Injeta no pool de Elite APENAS o IP cru (Sem o prefixo)
                if is_elite:
                    vivos["elite"].append((latencia, ip))

    # Exportação Tática (Ordenados dos mais rápidos para os mais lentos)
    for chave in vivos:
        if vivos[chave]:
            nome_arquivo = f"{chave}.txt"
            # Ordena pelo menor tempo de latência [0] e pega apenas o IP [1]
            ips_ordenados = [item[1] for item in sorted(vivos[chave])]
            
            # Remove duplicatas que podem ter passado de protocolos mistos no Elite
            ips_ordenados = list(dict.fromkeys(ips_ordenados))
            
            with open(nome_arquivo, "w") as f:
                for ip in ips_ordenados:
                    f.write(f"{ip}\n")
            print(f"[✔] {chave.upper()}: {len(ips_ordenados)} nós armados ({nome_arquivo}).")

    print(f"\n[✔] ROTAÇÃO CONCLUÍDA EM: {time.time() - inicio_geral:.2f}s")
