import time
import pandas as pd
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from threading import Thread

mensagem = ""
driver = None

def log(mensagem_log):
    caixa_logs.insert(tk.END, mensagem_log + "\n")
    caixa_logs.see(tk.END)  # Rola automaticamente

def iniciar_whatsapp():
    global driver
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options)
    driver.get("https://web.whatsapp.com")
    log("✅ WhatsApp Web iniciado. Escaneie o QR Code.")

def enviar_mensagens():
    global mensagem, driver
    contatos = pd.read_excel("contatos.xlsx")

    for telefone in contatos["telefone"]:
        log(f"🔍 Buscando contato: {telefone}")
        try:
            campo_busca = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
            campo_busca.click()
            campo_busca.clear()
            campo_busca.send_keys(telefone)
            campo_busca.send_keys(Keys.ENTER)

            time.sleep(5)

            campo_msg = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
            campo_msg.click()
            campo_msg.send_keys(mensagem)
            campo_msg.send_keys(Keys.ENTER)

            log(f"✅ Mensagem enviada para {telefone}")
            time.sleep(2)
        except Exception as e:
            log(f"❌ Erro com {telefone}: {e}")

    log("✅ Todas as mensagens foram enviadas!")

def salvar_mensagem():
    global mensagem
    mensagem = entry_mensagem.get()
    if not mensagem.strip():
        log("⚠️ Mensagem está vazia.")
        return
    log("💾 Mensagem salva com sucesso!")
    Thread(target=iniciar_whatsapp).start()
    botao_enviar.config(state="normal")

def iniciar_envio():
    Thread(target=enviar_mensagens).start()

# Interface gráfica
janela = tk.Tk()
janela.title("WhatsApp Sender")

tk.Label(janela, text="Digite a mensagem para enviar:").pack(pady=10)

entry_mensagem = tk.Entry(janela, width=50)
entry_mensagem.pack(pady=5)

botao_ok = tk.Button(janela, text="OK - Salvar Mensagem e Abrir WhatsApp", command=salvar_mensagem)
botao_ok.pack(pady=10)

botao_enviar = tk.Button(janela, text="Click - Enviar Mensagens", command=iniciar_envio, state="disabled")
botao_enviar.pack(pady=10)

# Caixinha de log
caixa_logs = tk.Text(janela, height=15, width=60)
caixa_logs.pack(pady=10)

janela.mainloop()
