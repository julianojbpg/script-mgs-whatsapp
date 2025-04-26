import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

# Lê a planilha Excel
contatos = pd.read_excel("contatos.xlsx")  # precisa ter coluna 'telefone'
mensagem = "Olá! Esta é uma mensagem automática enviada via Python 😊"

# Inicia o navegador Chrome
driver = webdriver.Chrome()  # precisa estar na mesma pasta
driver.get("https://web.whatsapp.com")

input("📲 Escaneie o QR Code do WhatsApp Web e pressione Enter aqui...")

# Envia mensagem para cada número
for telefone in contatos["telefone"]:
    print(f"Enviando para: {telefone}")  # Depuração
    link = f"https://web.whatsapp.com/send?phone={telefone}&text={mensagem}"
    driver.get(link)
    time.sleep(20)  # Aumenta o tempo de espera para garantir que tudo carregue

    try:
        # Tente localizar o botão de envio com o novo XPath
        btn_enviar = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div/div[4]/button/span')
        btn_enviar.click()
        print(f"✅ Mensagem enviada para {telefone}")
        time.sleep(5)
    except Exception as e:
        print(f"❌ Erro ao enviar para {telefone}: {e}")

driver.quit()
