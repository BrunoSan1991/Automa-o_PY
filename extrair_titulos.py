import requests
from bs4 import BeautifulSoup

# Lê os links do .txt (um por linha)
with open("links_gerados.txt", "r", encoding="utf-8") as f:
    links = [linha.strip() for linha in f if linha.strip()]

# Função para extrair apenas os títulos
def extrair_titulos(links):
    titulos = []
    for link in links:
        try:
            r = requests.get(link, timeout=10)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "html.parser")
                title = soup.title.string.strip() if soup.title else "SEM TITLE"
            else:
                title = f"ERRO HTTP {r.status_code}"
        except Exception as e:
            title = f"ERRO: {str(e)}"
        titulos.append(title)
    return titulos

# Extrai os títulos
titulos_extraidos = extrair_titulos(links)

# Salva apenas os títulos (sem o link)
with open("titulos_extraidos.txt", "w", encoding="utf-8") as f:
    for titulo in titulos_extraidos:
        f.write(titulo + "\n")

print("✅ Arquivo 'titulos_extraidos.txt' gerado com apenas os títulos.")
