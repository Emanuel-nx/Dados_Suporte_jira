# 📊 Dados_Suporte_Jira

## 📌 Índice
1. [Sobre o Projeto](#sobre-o-projeto)
2. [Tecnologias Utilizadas](#tecnologias-utilizadas)
3. [Pré-requisitos](#pré-requisitos)
4. [Instalação e Configuração](#instalação-e-configuração)
5. [Explicação do Código](#explicação-do-código)
6. [Automação da Execução](#automação-da-execução)
7. [Glossário](#glossário)
8. [Contribuição](#contribuição)
9. [Licença](#licença)

---

## 📖 Sobre o Projeto
Este projeto foi desenvolvido para **automatizar a coleta e análise de dados de suporte do Jira**. O objetivo principal é alimentar um dashboard no **Looker Studio** com informações extraídas do Jira, tratadas em Python e armazenadas em uma **planilha do Google**. O script foi automatizado para rodar diariamente, garantindo a atualização contínua do dashboard.

### 🚀 Funcionalidades
✅ Extração de dados do Jira via API
✅ Tratamento e formatação dos dados
✅ Armazenamento dos dados em uma planilha do Google
✅ Automação diária do processo

---

## 🛠 Tecnologias Utilizadas
- **Python 3.x**
- **JIRA API** para consulta dos dados
- **Google Sheets API** para armazenamento dos dados
- **Looker Studio** para visualização dos dados
- **Bibliotecas:** `pandas`, `jira`, `gspread`, `google-auth`, `dotenv`

---

## 🔧 Pré-requisitos
Antes de começar, você precisará ter instalado:
- **Python 3.x**
- **pip (gerenciador de pacotes do Python)**
- **Conta no Jira e API Token**
- **Credenciais de acesso ao Google Sheets**

---

## 💾 Instalação e Configuração
### 1️⃣ Clonar o Repositório
```bash
  git clone https://github.com/seu-usuario/Dados_Suporte_Jira.git
  cd Dados_Suporte_Jira
```

### 2️⃣ Instalar Dependências
```bash
  pip install -r requirements.txt
```

### 3️⃣ Configurar Variáveis Sensíveis
Crie um arquivo **.env** na raiz do projeto e adicione:
```
SERVER=https://seu-dominio.atlassian.net/
JIRA_USER=seu_email@dominio.com
JIRA_API_TOKEN=seu_token
FILTER=10425
SERVICE_ACCOUNT=caminho/para/credenciais.json
scope_file=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
```
> ⚠️ O arquivo `.env` já está no `.gitignore`, evitando que suas credenciais sejam expostas.

---

## 📝 Explicação do Código
### 1️⃣ Conectar ao Jira
```python
from jira import JIRA
import os
from dotenv import load_dotenv, find_dotenv

# Carregar credenciais do .env
load_dotenv(find_dotenv())

JIRA_SERVER = os.getenv("SERVER")
EMAIL = os.getenv("JIRA_USER")
API_TOKEN = os.getenv("JIRA_API_TOKEN")

# Autenticação no Jira
jira = JIRA(server=JIRA_SERVER, basic_auth=(EMAIL, API_TOKEN))
```
Este trecho **autentica no Jira** usando as credenciais armazenadas no `.env`.

### 2️⃣ Buscar Dados do Jira
```python
FILTER_ID = os.getenv("FILTER")
query = f"filter={FILTER_ID}"
issues = []
start_at = 0
batch_size = 100  

while True:
    batch = jira.search_issues(query, startAt=start_at, maxResults=batch_size)
    if not batch:
        break
    issues.extend(batch)
    start_at += batch_size
```
Aqui buscamos os **chamados de suporte** do Jira utilizando um filtro pré-definido.

### 3️⃣ Salvar os Dados no Google Sheets
```python
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# Autenticar no Google Sheets
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT")
scope = os.getenv("scope_file")
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scope)
client = gspread.authorize(creds)

# Abrir a planilha pelo nome
spreadsheet = client.open("Dashboard Data")  
sheet = spreadsheet.sheet1  

# Criar um DataFrame e atualizar a planilha
sheet.clear()
sheet.update([df.columns.values.tolist()] + df.values.tolist())

print("✅ Dados enviados para o Google Sheets com sucesso!")
```
Aqui os dados são **inseridos em uma planilha do Google**, permitindo integração com o **Looker Studio**.

---

## ⏰ Automação da Execução
Para garantir a atualização diária dos dados, você pode usar o **Task Scheduler (Windows)** ou **Crontab (Linux/Mac)**.

### Windows (Task Scheduler)
1. Abra o **Agendador de Tarefas**
2. Crie uma nova tarefa e selecione "Executar um programa"
3. Configure para executar o script Python diariamente:
```bash
python caminho/do/seu/script.py
```

### Linux/Mac (Crontab)
Edite o crontab:
```bash
crontab -e
```
Adicione a linha:
```bash
0 6 * * * /usr/bin/python3 /caminho/do/seu/script.py
```
Isso executará o script todo dia às **06:00 da manhã**.

---

## 📚 Glossário
- **Jira API**: Interface que permite interação com os dados do Jira.
- **Looker Studio**: Plataforma do Google para criação de dashboards interativos.
- **Google Sheets API**: Permite manipular planilhas do Google via código.
- **Crontab/Task Scheduler**: Ferramentas para automação de tarefas recorrentes.

---

## 🤝 Contribuição
Sinta-se à vontade para contribuir! Para isso:
1. Faça um **fork** do projeto
2. Crie uma **branch** (`git checkout -b feature-nova`)
3. Commit suas mudanças (`git commit -m 'Adicionando nova feature'`)
4. Faça um **push** (`git push origin feature-nova`)
5. Abra um **Pull Request**

---

## 📜 Licença
Este projeto está licenciado sob a **MIT License**. Sinta-se livre para usá-lo e modificá-lo conforme necessário!

📩 **Dúvidas ou sugestões?** Entre em contato! 😊

