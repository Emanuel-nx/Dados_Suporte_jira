import pandas as pd
from jira import JIRA
from google.oauth2.service_account import Credentials
import gspread
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
import os
#from google.cloud import bigquery

# Carregar variáveis do .env
load_dotenv(find_dotenv())


# Configurações do Jira
JIRA_SERVER = os.getenv("SERVER")
EMAIL = os.getenv("JIRA_USER")
API_TOKEN = os.getenv("JIRA_API_TOKEN")

# USANDO PARA DEBUGAR A CONEXÃO
# print("Email:", EMAIL)
# print("Token:", "EXISTS" if API_TOKEN else "MISSING")

# Conectar ao Jira
jira = JIRA(server=JIRA_SERVER, basic_auth=(EMAIL, API_TOKEN))

# ID do filtro no Jira
FILTER_ID = os.getenv("FILTER")
query = f"filter={FILTER_ID}"

# Buscar todas as issues com paginação
issues = []
start_at = 0
batch_size = 100  # Jira permite até 1000, mas pode ser ajustado

while True:
    batch = jira.search_issues(query, startAt=start_at, maxResults=batch_size)
    if not batch:
        break
    issues.extend(batch)
    start_at += batch_size

print(f"✅ Total de {len(issues)} issues carregadas.")

# Criar uma lista com os dados das issues
dados = []
for issue in issues:
    fields = issue.fields

    tipo_item = fields.issuetype.name.replace("[System] ", "") if fields.issuetype else ""
    categoria = fields.customfield_10150 if hasattr(fields, 'customfield_10150') and fields.customfield_10150 else fields.customfield_10277 if hasattr(fields, 'customfield_10277') else ""
    status = fields.status.name.replace("Concluída", "Resolvido") if fields.status else ""

    dados.append({
        "TIPO_DE_ITEM": tipo_item,
        "ID": issue.key,
        "RESUMO": fields.summary if fields.summary else "",
        "CHAPTER": fields.customfield_10149 if hasattr(fields, 'customfield_10149') else "",
        "RESPONSAVEL": fields.assignee.displayName if fields.assignee else "",
        "RELATOR": fields.reporter.displayName if fields.reporter else "",
        "CATEGORIA": categoria,
        "PRIORIDADE": fields.priority.name if fields.priority else "",
        "STATUS": status,
        "MOTIVO_DE_PENDENTE": fields.customfield_10125 if hasattr(fields, 'customfield_10125') else "",
        "PLATAFORMA": fields.customfield_10607 if hasattr(fields, 'customfield_10607') else "",
        "FREQUENCIA": fields.customfield_10609 if hasattr(fields, 'customfield_10609') else "",
        "RESOLUCAO": fields.resolution.name if fields.resolution else "Sem Resolução",
        "CRIADO": fields.created if fields.created else "",
        "TIME_UPDATED": fields.updated if hasattr(fields, 'updated') else "",
        "RESOLVIDO": fields.resolutiondate if hasattr(fields, 'resolutiondate') else "",
        "TEMPO GASTO": fields.timespent if fields.timespent else 0,
        "INICIO_DESENVOLVIMENTO": fields.customfield_10137 if hasattr(fields, 'customfield_10137') else "",
        "FINAL_DESENVOLVIMENTO": fields.customfield_10138 if hasattr(fields, 'customfield_10138') else "",
        "TEMPO_ATE_RESOLUCAO": fields.customfield_10773 if hasattr(fields, 'customfield_10773') else "",
        
    })

# Criar um DataFrame do pandas
df = pd.DataFrame(dados)

# 🔹 CONFIGURAÇÃO DO GOOGLE SHEETS
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT")

scope = os.getenv("scope_file")
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scope)
client = gspread.authorize(creds)

# Abrir a planilha pelo nome
spreadsheet = client.open("Dashboard Data")  # Nome da planilha no Google Sheets
sheet = spreadsheet.sheet1  # Primeira aba

# 🔹 Atualizando a planilha
sheet.clear()  # Limpa os dados antigos
sheet.update([df.columns.values.tolist()] + df.values.tolist())  # Atualiza com novos dados

print("✅ Dados enviados para o Google Sheets com sucesso!")
