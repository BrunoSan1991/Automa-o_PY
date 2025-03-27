import os
import requests
import re

# Ler a lista de sites de um arquivo
def carregar_lista_sites(arquivo):
    with open(arquivo, "r") as f:
        return [linha.strip() for linha in f.readlines() if linha.strip()]

sites = carregar_lista_sites("sites.txt")
base_url = "https://infoms.saude.gov.br/extensions/{}/{}"

def baixar_arquivo(url, pasta, nome_arquivo):
    try:
        resposta = requests.get(url, timeout=10)
        if resposta.status_code == 200:
            caminho_arquivo = os.path.join(pasta, nome_arquivo)
            with open(caminho_arquivo, "wb") as arquivo:
                arquivo.write(resposta.content)
            print(f"Baixado: {caminho_arquivo}")
            return caminho_arquivo
        else:
            print(f"Erro {resposta.status_code} ao baixar {url}")
    except Exception as e:
        print(f"Erro ao acessar {url}: {e}")
    return None

def analisar_js(caminho_arquivo, log_file):
    if not caminho_arquivo or not os.path.exists(caminho_arquivo):
        with open(log_file, "a", encoding="utf-8") as log:
            log.write(f"[ERRO] Arquivo JS não encontrado: {caminho_arquivo}\n\n")
        return
    
    with open(caminho_arquivo, "r", encoding="utf-8") as file:
        conteudo = file.readlines()
    
    padrao = re.compile(r"qlik\.openApp\(['\"](.*?)['\"],", re.IGNORECASE)
    linhas_encontradas = []
    
    for i, linha in enumerate(conteudo, start=1):
        match = padrao.search(linha)
        if match:
            linhas_encontradas.append((i, linha.strip()))
    
    with open(log_file, "a", encoding="utf-8") as log:
        if linhas_encontradas:
            log.write(f"Olhando arquivo JS {caminho_arquivo} encontrei:\n")
            for linha_num, linha_texto in linhas_encontradas:
                log.write(f"Linha {linha_num}: {linha_texto}\n")
        else:
            log.write(f"Nenhuma referência a qlik.openApp encontrada em {caminho_arquivo}\n")
        log.write("\n")

# Criar pastas e baixar arquivos
log_file = "analise_js.log"
if os.path.exists(log_file):
    os.remove(log_file)

for site in sites:
    pasta_site = os.path.join("downloads", site)
    os.makedirs(pasta_site, exist_ok=True)
    
    baixar_arquivo(base_url.format(site, site + ".html"), pasta_site, site + ".html")
    js_path = baixar_arquivo(base_url.format(site, site + ".js"), pasta_site, site + ".js")
    baixar_arquivo(base_url.format(site, site + ".css"), pasta_site, site + ".css")
    
    if js_path and os.path.exists(js_path):
        analisar_js(js_path, log_file)