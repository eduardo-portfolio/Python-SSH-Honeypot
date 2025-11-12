import socket
import threading
from datetime import datetime
import os
import requests

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage" if BOT_TOKEN else None

def send_telegram_message(text):
    if not BOT_TOKEN or not CHAT_ID:
        return
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        r = requests.post(TELEGRAM_API_URL, data=payload, timeout=5)
        r.raise_for_status()
    except Exception as e:
        print(f"[!] Falha ao enviar Telegram: {e}")

def log_attack(ip, user, pwd):
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    linha = f"[{ts}] IP: {ip} | User: {user} | Pass: {pwd}\n"
    try:
        with open("attacks.log", "a") as f:
            f.write(linha)
    except Exception as e:
        print(f"[!] Erro ao escrever log: {e}")
    print(f"ATAQUE: {ip} -> {user}:{pwd}")
    msg = f" <b>Honeypot SSH - Novo ataque</b>\n<b>IP:</b> {ip}\n<b>User:</b> {user}\n<b>Pass:</b> {pwd}"
    send_telegram_message(msg)

def handle_connection(client, addr):
    try:
        data = client.recv(1024)
        if not data:
            return
        text = data.decode(errors="ignore").strip()
        user = "unknown"
        pwd = text
        log_attack(addr[0], user, pwd)
        resp = f"\r\n{text}: command not found\r\n$ "
        try:
            client.send(resp.encode())
        except Exception:
            pass
    except Exception as e:
        print(f"[ERRO] {e}")
    finally:
        try:
            client.close()
        except Exception:
            pass

def start(host='0.0.0.0', port=2222):
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)
    print(f"Honeypot rodando na porta {port}...")
    print(f"   Teste com: ssh qualquer@127.0.0.1 -p {port}")

    while True:
        client, addr = server.accept()
        print(f"[+] Conexão de {addr[0]}")
        t = threading.Thread(target=handle_connection, args=(client, addr))
        t.daemon = True
        t.start()

if __name__ == "__main__":
    HOST = os.environ.get("HONEYPOT_HOST", "0.0.0.0")
    PORT = int(os.environ.get("HONEYPOT_PORT", "2222"))
    
    start(HOST, PORT) #IP E LOCAL PORT 
