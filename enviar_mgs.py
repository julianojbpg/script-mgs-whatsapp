import time
import pandas as pd
import urllib.parse
import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Configuração do ChromeDriver
def iniciar_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# Função de log para mostrar mensagens na interface
def log(mensagem):
    log_text.config(state=tk.NORMAL)
    log_text.insert(tk.END, mensagem + "\n")
    log_text.config(state=tk.DISABLED)
    log_text.yview(tk.END)

# Função para salvar a mensagem inserida na interface
def salvar_mensagem():
    global mensagem
    mensagem = campo_texto.get("1.0", tk.END).strip()  # Pegando o conteúdo e removendo caracteres extras
    if mensagem:
        log("✅ Mensagem salva com sucesso!")
    else:
        messagebox.showwarning("Aviso", "Digite a mensagem antes de salvar!")

# Função para iniciar o WhatsApp Web e enviar as mensagens
def enviar_mensagens():
    global driver, mensagem
    if not driver:
        messagebox.showerror("Erro", "WhatsApp Web não foi iniciado ainda!")
        return

    if not mensagem:
        messagebox.showwarning("Aviso", "Você precisa salvar a mensagem primeiro!")
        return

    try:
        contatos = pd.read_excel("contatos.xlsx")  # Precisa ter coluna 'telefone'
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao ler planilha: {e}")
        return

    # Codificando a mensagem para garantir que as quebras de linha sejam mantidas
    mensagem_codificada = urllib.parse.quote(mensagem)

    for telefone in contatos["telefone"]:
        log(f"🔍 Buscando contato: {telefone}")
        link = f"https://web.whatsapp.com/send?phone={telefone}&text={mensagem_codificada}"
        driver.get(link)
        time.sleep(15)

        try:
            btn_enviar = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div/div[4]/button/span')
            btn_enviar.click()
            log(f"✅ Mensagem enviada para {telefone}")
            time.sleep(5)
        except Exception as e:
            log(f"❌ Erro ao enviar para {telefone}: {e}")

    log("✅ Todas as mensagens foram enviadas!")

# Função para abrir o WhatsApp Web
def abrir_whatsapp():
    global driver
    driver = iniciar_driver()
    driver.get("https://web.whatsapp.com")
    log("✅ WhatsApp Web iniciado. Escaneie o QR Code.")
    input("📲 Escaneie o QR Code do WhatsApp Web e pressione Enter aqui...")

# Configuração da interface gráfica
root = tk.Tk()
root.title("Envio de Mensagens WhatsApp")
root.geometry("500x600")  # Ajustei o tamanho da janela
root.config(bg="#303030")  # Cor de fundo RGB(48,48,48)

# Campo de texto para a mensagem
campo_texto = tk.Text(root, height=13, width=50, bg="#000000", fg="#FFFFFF", bd=2, font=("Arial", 12))
campo_texto.pack(pady=10)

# Botão para salvar a mensagem
botao_salvar = tk.Button(root, text="💾 Salvar Mensagem", command=salvar_mensagem, bg="#ee9945", fg="#000000", font=("Arial", 12), relief="flat", padx=20, pady=5)
botao_salvar.pack(pady=5)

# Botão para abrir o WhatsApp Web
botao_abrir = tk.Button(root, text="🌐 Abrir WhatsApp Web", command=abrir_whatsapp, bg="#ee9945", fg="#000000", font=("Arial", 12), relief="flat", padx=20, pady=5)
botao_abrir.pack(pady=5)

# Botão para enviar as mensagens
botao_enviar = tk.Button(root, text="📤 Enviar Mensagens", command=enviar_mensagens, bg="#ee9945", fg="#000000", font=("Arial", 12), relief="flat", padx=20, pady=5)
botao_enviar.pack(pady=5)

# Caixa de logs para exibir o progresso (agora com a mesma altura do campo de texto)
log_text = tk.Text(root, height=8, width=50, state=tk.DISABLED, bg="#000000", fg="#FFFFFF", bd=2, font=("Arial", 12))
log_text.pack(pady=10)

root.mainloop()
