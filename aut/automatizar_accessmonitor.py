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
# options.add_argument("--headless")  # Rodar sem abrir o navegador
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
    
    # Acessar o site de avaliação
    log(f"Acessando site de avaliação para {site}...")
    driver.get("https://accessmonitor.acessibilidade.gov.pt/")
    time.sleep(3)  # Espera carregar
    
    # with open(f"debug_{site}.html", "w", encoding="utf-8") as f:
    #     f.write(driver.page_source)
    #     log("HTML salvo em debug.html")

    # Clicar no botão para inserir HTML
    try:
        log("Procurando botão 'Inserir código HTML'...")
        button = driver.find_element(By.XPATH, "//button[contains(text(), 'Inserir código HTML')]")
        log("Botão encontrado! Clicando...")
        button.click()
        time.sleep(3)
    except Exception as e:
        log(f"Erro ao clicar no botão para site {site}: {str(e)}")
        continue
    
    # Inserir HTML
    # try:
    #     log("Procurando textarea para inserir HTML...")
    #     textarea = driver.find_element(By.XPATH, "//textarea[@id='html']")
    #     log("Textarea encontrada! Inserindo HTML...")
    #     textarea.send_keys(html_content)
    #     time.sleep(30)
    #     log("HTML enviado com sucesso!")
    # except Exception as e:
    #     log(f"Erro ao inserir HTML para {site}: {str(e)}")
    #     continue


    # Definir diretamente o valor do textarea via JavaScript FUNCIONOU
    # try:
    #     log("Procurando textarea para inserir HTML...")
    #     textarea = driver.find_element(By.XPATH, "//textarea[@id='html']")
    #     log("Textarea encontrada! Limpando e inserindo HTML via JavaScript...")
    #     # Usando JavaScript para definir o conteúdo
    #     driver.execute_script("arguments[0].value = arguments[1];", textarea, html_content)
    #     time.sleep(3)  # Espera para garantir que o conteúdo foi inserido
    #     log("HTML enviado com sucesso!")
    # except Exception as e:
    #     log(f"Erro ao inserir HTML para {site}: {str(e)}")
    #     continue
    
    try:
        log("Procurando textarea para inserir HTML...")
        textarea = driver.find_element(By.XPATH, "//textarea[@id='html']")
        log("Textarea encontrada! Limpando e inserindo HTML via JavaScript...")

        # Usando JavaScript para definir o conteúdo
        driver.execute_script("arguments[0].value = arguments[1];", textarea, html_content)
        time.sleep(3)  # Espera para garantir que o conteúdo foi inserido
        log("HTML enviado com sucesso!")

        # Adicionar um "espaço" para ativar o botão
        log("Adicionando um espaço no textarea para ativar o botão...")
        textarea.send_keys(" ")  # Simula pressionamento de "espaço"
        time.sleep(2)  # Espera para garantir que o botão foi ativado

        log("Espaço enviado com sucesso!")
    except Exception as e:
        log(f"Erro ao simular espaço para {site}: {str(e)}")
        continue

    # Clicar no botão de validar
    # try:
    #     log("Procurando botão 'Validar'...")
    #     # validar_btn = driver.find_element(By.XPATH, "//button[contains(., 'Validar')]")
    #     validar_btn = driver.find_element(By.XPATH, "//form//button[@id='btn-html']//span[contains(text(), 'Validar')]")
    #     log("Botão de validar encontrado! Clicando...")
    #     validar_btn.click()
    #     log("AGUARDANDO RESULTADOS...")
    #     time.sleep(20)  # Espera os resultados aparecerem
    # except Exception as e:
    #     log(f"Erro ao clicar no botão de validar para {site}: {str(e)}")
    #     continue


    # Esperar até que o botão de validar esteja habilitado e clicável
    try:
        log("Esperando o botão de validar ficar habilitado...")
        validar_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//form//button[@id='btn-html'][not(@disabled)]"))
        )
        log("Botão habilitado e clicável! Clicando...")
        validar_btn.click()
        time.sleep(10)  # Espera a ação ser processada
        log("AGUARDANDO RESULTADOS...")
    except Exception as e:
        log(f"Erro ao esperar e clicar no botão de validar para {site}: {str(e)}")
        continue


    # Habilitar o botão de "Validar" via JavaScript
    # try:
    #     log("Habilitando o botão de validar...")
    #     driver.execute_script("document.getElementById('btn-html').disabled = false;")
    #     time.sleep(1)  # Espera para garantir que o botão foi habilitado

    #     # Agora, clicar no botão
    #     log("Botão habilitado! Clicando...")
    #     validar_btn = driver.find_element(By.XPATH, "//form//button[@id='btn-html']")
    #     driver.execute_script("arguments[0].click();", validar_btn)  # Clica usando JS
    #     time.sleep(5)  # Espera a ação ser processada
    # except Exception as e:
    #     log(f"Erro ao habilitar e clicar no botão de validar para {site}: {str(e)}")
    #     continue


    
    # Obter o resultado
    log("Tentando extrair a pontuação...")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    score_element = soup.find("text", string="Pontuação")
    
    if score_element:
        score = score_element.find_previous_sibling("text").text.strip()
        log(f"Pontuação encontrada para {site}: {score}")
        resultados.append([site, score])
    else:
        log(f"Erro ao obter a pontuação para {site}")

# Salvar em CSV
log("Salvando resultados no CSV...")
with open("resultados_accessmonitor.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Site", "Pontuação"])
    writer.writerows(resultados)

log("Processo concluído. Resultados salvos em resultados.csv")

# Fechar o navegador
driver.quit()