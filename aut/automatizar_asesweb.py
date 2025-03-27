import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Configurar Selenium
options = webdriver.ChromeOptions()
options.binary_location = "/opt/chrome-for-testing/chrome"
options.add_argument("--headless")  # Rodar sem abrir o navegador
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")


# Inicializa o WebDriver
service = Service("/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=options)

# Ler lista de sites
with open("sites.txt", "r") as f:
    sites = [line.strip() for line in f.readlines()]

resultados = []

def log(text):
    """Função auxiliar para imprimir logs formatados."""
    print(f"[LOG] {text}")

for site in sites:
    html_path = f"downloads/{site}/{site}.html"
    if not os.path.exists(html_path):
        log(f"Arquivo não encontrado: {html_path}")
        continue
    
    with open(html_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    
    log(f"Acessando site de avaliação para {site}...")
    driver.get("https://asesweb.governoeletronico.gov.br/")
    time.sleep(3)  # Espera carregar

    # Clicar na aba de Validação pelo código fonte
    try:
        log("Selecionando 'Validação pelo código fonte'...")
        tab_label = driver.find_element(By.XPATH, "//label[@id='validacaoCodigoFonte']")
        tab_label.click()
        time.sleep(3)
    except Exception as e:
        log(f"Erro ao selecionar a aba de validação para {site}: {str(e)}")
        continue

    # Inserir HTML
    try:
        log("Procurando textarea para inserir HTML...")
        textarea = driver.find_element(By.XPATH, "//textarea[@id='input']")
        log("Textarea encontrada! Inserindo HTML...")
        driver.execute_script("arguments[0].value = arguments[1];", textarea, html_content)
        time.sleep(3)
        # textarea.send_keys(Keys.SPACE)  # Simula interação
        log("HTML enviado com sucesso!")
    except Exception as e:
        log(f"Erro ao inserir HTML para {site}: {str(e)}")
        continue

    # Clicar no botão de validar
    try:
        log("Procurando botão 'Executar'...")
        validar_btn = driver.find_element(By.XPATH, "//input[@id='input_tab_3']")
        log("Botão de validar encontrado! Clicando...")
        validar_btn.click()
        log("AGUARDANDO RESULTADOS...")
        time.sleep(10)  # Espera os resultados aparecerem
    except Exception as e:
        log(f"Erro ao clicar no botão de validar para {site}: {str(e)}")
        continue

    # Obter o resultado
    try:
        log("Tentando extrair a pontuação...")
        soup = BeautifulSoup(driver.page_source, "html.parser")
        score_element = soup.find("div", id="webaxscore")
        
        if score_element:
            # score = score_element.find("span").text.strip()
            score = score_element.find("span").text.strip().replace("%", "")  # Remove o %
            log(f"Pontuação encontrada para {site}: {score}")
            resultados.append([site, score])
        else:
            log(f"Erro ao obter a pontuação para {site}")
    except Exception as e:
        log(f"Erro ao processar pontuação para {site}: {str(e)}")

# Salvar em CSV
log("Salvando resultados no CSV...")
with open("resultados_asesweb.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Site", "Pontuação"])
    writer.writerows(resultados)

log("Processo concluído. Resultados salvos em resultados.csv")

# Fechar o navegador
driver.quit()