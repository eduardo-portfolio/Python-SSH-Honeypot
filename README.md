# SSH Honeypot - Python & Integração de Telegram para Logs

## Objetivo
O projeto consiste no desenvolvimento de uma porta 22 SSH propositalmente vulnerável para atrair ataques. O sistema escuta conexões na porta, registra tentativas de acesso, e envia notificações em tempo real via Telegram.

### Habilidades Aprendidas 

- Bibliotecas paramiko e socket.
- Sockets TCP e conexões SSH
- Integração com APIs externas
- Automação em Python

### Ferramentas Usadas 

- Kali Linux (VMware Pro)
- Python3  
- Telegram 

## Meus passos

Por questões de organização, criei uma pasta para o aplicativo. 


<img width="367" height="117" alt="image" src="https://github.com/user-attachments/assets/e70b364d-4bb2-4eb2-8206-5266267ec53e" />


Com Python3 já imbutido na máquina, criei  o arquivo .py com o comando "nano" e o acessei. 


<img width="367" height="117" alt="image" src="https://github.com/user-attachments/assets/9bb89ad2-6fba-46dd-a030-5391a0c8c362" />

Bibliotecas e módulos que foram importados. 

<img width="855" height="123" alt="image" src="https://github.com/user-attachments/assets/99d3db26-bff0-4c32-9804-88682eb4abed" />

Preparei as configurações para o Telegram, BOT_TOKEN para reconhecimento do bot com token, CHAT_ID para inserir o ID do chat que gerei com o bot 
e URL da API do Telegram para enviar mensagens.

<img width="676" height="73" alt="image" src="https://github.com/user-attachments/assets/951e0571-56cc-4bb6-8fad-9f0ebe2f7ff9" />

Esta classe diz ao Paramiko o que fazer quando alguém tenta entrar pelo SSH. Quando o atacante envia usuário+senha, ela pega o IP, grava a tentativa (log + print) e manda notificação tanto no CLI quanto via Telegram. Depois finge que a autenticação deu certo para manter a sessão aberta e coletar mais informações.

<img width="456" height="196" alt="image" src="https://github.com/user-attachments/assets/8a2bef80-4d28-4f0f-8c9e-7d86525b6fd2" />

Iniciei um servidor TCP que escuta na porta -p 2222 pois estava havendo conflitos na porta -p 22.
Para cada conexão criei uma thread que executa o "handle_connection", permitindo atender várias conexões.

<img width="614" height="270" alt="image" src="https://github.com/user-attachments/assets/99ba0cd2-8e21-434e-ae53-07fb93d6d01e" />

Fiz executar a função "send_telegram_message", que envia uma mensagem para o chat no Telegram usando a API do bot. Se o bot token ou o chat ID não estiverem corretamente configurados, ela não tenta enviar a mensagem. Quando configurado corretamente, monta um payload com as informações necessárias e tenta enviar a mensagem via requests.post. Se a requisição falhar, ela registra um erro 


<img width="467" height="63" alt="image" src="https://github.com/user-attachments/assets/ca61b26e-bf5e-4c01-9b9e-8ac288df5767" />


Mas o erro não interrompe a execução do honeypot. 


<img width="603" height="292" alt="image" src="https://github.com/user-attachments/assets/7c322ae9-f090-4086-b149-bf140e75d16d" />


Quando tudo estava funcionando, fui no telegram e procurei pelo BotFather, ele entrega o ChatID e os Tokens necessários para que eu me conecte com o .py. 

<img width="410" height="74" alt="image" src="https://github.com/user-attachments/assets/abd7308a-fb09-44eb-acf4-3d1150816e65" />

Daqui foi simples, passei o ChatID e o Token do Bot para o script e executei o Listener. Em outro terminal no mesmo dispositivo simulei a tentativa de ataque (ssh -o StrictHostKeyChecking=no server@IP_DO_SERVER -p PORTA) para gerar os logs de alerta. 


<img width="808" height="427" alt="image" src="https://github.com/user-attachments/assets/a3758f76-4bf6-41f2-8262-1d52c37de46e" />













