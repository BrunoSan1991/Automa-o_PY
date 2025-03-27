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
time.sleep(3)  # Espera o JS carregar

# PEGA OS NOMES DOS SPANS
elements = driver.find_elements(By.CSS_SELECTOR, "span.text-title.ng-isolate-scope")
nomes_site = [el.text.strip() for el in elements if el.text.strip() != ""]

driver.quit()

# LÊ O EXCEL
excel_path = "mashup.xlsx"  # Altere para o seu arquivo
df = pd.read_excel(excel_path)

if "mashup" not in df.columns:
    raise Exception("A coluna 'mashup' não foi encontrada no Excel!")

# NORMALIZAÇÃO PARA COMPARAÇÃO
mashups_excel = df["mashup"].astype(str).str.strip()
mashups_excel_lower = mashups_excel.str.lower()
nomes_site_lower = [n.strip().lower() for n in nomes_site]

# ✔️ NOMES QUE ESTÃO NO SITE MAS NÃO ESTÃO NA PLANILHA
faltando_na_planilha = [
    original for original, norm in zip(nomes_site, nomes_site_lower)
    if norm not in mashups_excel_lower.values
]

# ❗ NOMES QUE ESTÃO NA PLANILHA MAS NÃO ESTÃO NO SITE
excesso_na_planilha = [
    original for original, norm in zip(mashups_excel, mashups_excel_lower)
    if norm not in nomes_site_lower
]

# SALVA OS RESULTADOS
with open("faltando_na_planilha.txt", "w", encoding="utf-8") as f:
    for nome in faltando_na_planilha:
        f.write(nome + "\n")

with open("excesso_na_planilha.txt", "w", encoding="utf-8") as f:
    for nome in excesso_na_planilha:
        f.write(nome + "\n")

print(f"✅ {len(faltando_na_planilha)} mashups estão no site mas não estão na planilha (faltando_na_planilha.txt)")
print(f"✅ {len(excesso_na_planilha)} mashups estão na planilha mas não estão no site (excesso_na_planilha.txt)")
