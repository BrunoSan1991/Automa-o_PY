from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time

# CONFIGURAÇÕES DO SELENIUM
options = Options()
options.add_argument("--headless=new")  # Tira isso se quiser ver o navegador abrindo
options.add_argument("--window-size=1920,1080")

# INICIALIZA O CHROME COM O CHROMEDRIVER
driver = webdriver.Chrome(options=options)

# ACESSA O SITE
driver.get("https://infoms.saude.gov.br/dev-hub")
time.sleep(3)  # Espera o JS carregar — se quiser mais garantia, aumente para 5s

# PEGA OS NOMES DOS SPANS COM CLASSE DE MASHUPS
elements = driver.find_elements(By.CSS_SELECTOR, "span.text-title.ng-isolate-scope")
nomes_extraidos = [el.text.strip() for el in elements if el.text.strip() != ""]

driver.quit()

# LÊ O EXCEL
excel_path = "mashup.xlsx"  # Altere para o nome real do seu arquivo
df = pd.read_excel(excel_path)

# VERIFICA SE A COLUNA EXISTE
if "mashup" not in df.columns:
    raise Exception("A coluna 'mashup' não foi encontrada no Excel!")

# NORMALIZA NOMES
mashups_excel = [m.strip().lower() for m in df["mashup"].astype(str)]
nomes_normalizados = [n.strip().lower() for n in nomes_extraidos]

# PEGA OS NOMES QUE ESTÃO NO SITE MAS NÃO NO EXCEL
nao_encontrados = [
    original for original, norm in zip(nomes_extraidos, nomes_normalizados)
    if norm not in mashups_excel
]

# SALVA NO .TXT
if nao_encontrados:
    with open("mashups_nao_encontrados.txt", "w", encoding="utf-8") as f:
        for nome in nao_encontrados:
            f.write(nome + "\n")
    print(f"✅ {len(nao_encontrados)} mashups não encontrados foram salvos em mashups_nao_encontrados.txt")
else:
    print("✅ Todos os mashups do site estão na planilha!")
