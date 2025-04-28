import time
import pandas as pd
import urllib.parse
import tkinter as tk
from tkinter import messagebox, filedialog
from ttkbootstrap import Style
from ttkbootstrap import ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import sys
import os
import re

# Variáveis globais
driver = None
mensagem = ""
caminho_arquivo_contatos = None

# Função para formatar o número de telefone
def formatar_telefone(telefone):
    telefone = str(telefone)
    telefone = re.sub(r'\D', '', telefone)
    if len(telefone) == 11:
        telefone = '55' + telefone
    else:
        raise ValueError(f"Número de telefone {telefone} com formato inválido!")
    return telefone

# Configuração do ChromeDriver local
def iniciar_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    
    caminho_driver = os.path.join(os.path.abspath("."), "chromedriver.exe")
    service = Service(caminho_driver)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Função de log
def log(mensagem_log):
    log_text.configure(state=tk.NORMAL)
    log_text.insert(tk.END, mensagem_log + "\n")
    log_text.configure(state=tk.DISABLED)
    log_text.yview(tk.END)
    root.update()

# Função para salvar a mensagem
def salvar_mensagem():
    global mensagem
    mensagem = campo_texto.get("1.0", tk.END).strip()
    if mensagem:
        log("✅ Mensagem salva com sucesso!")
    else:
        messagebox.showwarning("Aviso", "Digite a mensagem antes de salvar!")

# Função para escolher o arquivo de contatos
def escolher_arquivo_contatos():
    global caminho_arquivo_contatos
    caminho = filedialog.askopenfilename(
        title="Selecione a planilha de contatos",
        filetypes=[("Arquivos Excel", "*.xlsx")]
    )
    if caminho:
        caminho_arquivo_contatos = caminho
        log(f"✅ Arquivo selecionado: {os.path.basename(caminho)}")
    else:
        messagebox.showwarning("Aviso", "Nenhum arquivo selecionado!")

# Função para enviar mensagens
def enviar_mensagens():
    global driver, mensagem, caminho_arquivo_contatos
    if not driver:
        messagebox.showerror("Erro", "WhatsApp Web não foi iniciado ainda!")
        return

    if not mensagem:
        messagebox.showwarning("Aviso", "Você precisa salvar a mensagem primeiro!")
        return

    if not caminho_arquivo_contatos:
        messagebox.showwarning("Aviso", "Você precisa selecionar a planilha de contatos!")
        return

    try:
        abas = pd.read_excel(caminho_arquivo_contatos, sheet_name=None)
        contatos = pd.concat(abas.values(), ignore_index=True)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao ler a planilha: {e}")
        return

    mensagem_codificada = urllib.parse.quote(mensagem)

    for telefone in contatos["Contato"]:
        try:
            telefone_formatado = formatar_telefone(telefone)
            log(f"🔍 Buscando contato: {telefone_formatado}")
            link = f"https://web.whatsapp.com/send?phone={telefone_formatado}&text={mensagem_codificada}"
            driver.get(link)
            time.sleep(15)

            try:
                btn_enviar = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div/div[4]/button/span')
                btn_enviar.click()
                log(f"✅ Mensagem enviada para {telefone_formatado}")
                time.sleep(5)
            except Exception as e:
                log(f"❌ Erro ao enviar para {telefone_formatado}: {e}")
        except ValueError as e:
            log(f"❌ Erro ao formatar o número {telefone}: {e}")

    log("✅ Todas as mensagens foram enviadas!")

# Configuração da interface gráfica
style = Style(theme="darkly")
root = style.master
root.title("Envio de Mensagens WhatsApp")
root.geometry("500x700")
root.config(bg="#303030")

# Campo de texto para digitar a mensagem
campo_texto = tk.Text(root, height=10, width=50, font=("Arial", 12), bd=2)
campo_texto.config(fg="#ffffff", bg="#000000")
campo_texto.pack(pady=10)

# Botão para salvar a mensagem
botao_salvar = ttk.Button(root, text="💾 Salvar Mensagem", command=salvar_mensagem, bootstyle="primary", width=30)
botao_salvar.pack(pady=5)

# Botão para escolher o arquivo de contatos
botao_selecionar_arquivo = ttk.Button(root, text="📂 Selecionar Planilha de Contatos", command=escolher_arquivo_contatos, bootstyle="info", width=30)
botao_selecionar_arquivo.pack(pady=5)

# Botão para enviar as mensagens
botao_enviar = ttk.Button(root, text="📤 Enviar Mensagens", command=enviar_mensagens, bootstyle="success", width=30)
botao_enviar.pack(pady=5)

# Caixa de log
log_text = tk.Text(root, height=13, width=50, font=("Arial", 12), bd=2)
log_text.config(fg="#ffffff", bg="#000000", state="disabled")
log_text.pack(pady=10)

# Iniciar o driver automaticamente
try:
    driver = iniciar_driver()
    driver.get("https://web.whatsapp.com")
    log("✅ WhatsApp Web iniciado. Escaneie o QR Code e clique em ENVIAR depois.")
except Exception as e:
    messagebox.showerror("Erro", f"Erro ao iniciar o WhatsApp Web: {e}")

root.mainloop()
