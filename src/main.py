import os
import time
import json
import requests
import mimetypes
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

DOCUMENT_INTELLIGENCE_ENDPOINT = os.getenv("DOCUMENT_INTELLIGENCE_ENDPOINT")
DOCUMENT_INTELLIGENCE_KEY = os.getenv("DOCUMENT_INTELLIGENCE_KEY")
OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not all([DOCUMENT_INTELLIGENCE_ENDPOINT, DOCUMENT_INTELLIGENCE_KEY, OPENAI_ENDPOINT, OPENAI_API_KEY]):
    raise Exception("Certifique-se de que todas as variáveis de ambiente estão definidas no arquivo .env.")

def analyze_document(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        raise Exception(f"Tipo de arquivo não suportado: {file_path}")

    url = f"{DOCUMENT_INTELLIGENCE_ENDPOINT}formrecognizer/documentModels/prebuilt-layout:analyze?api-version=2023-07-31"
    headers = {
        "Content-Type": mime_type,
        "Ocp-Apim-Subscription-Key": DOCUMENT_INTELLIGENCE_KEY
    }

    with open(file_path, "rb") as f:
        response = requests.post(url, headers=headers, data=f.read())

    if response.status_code != 202:
        raise Exception(f"Erro na análise: {response.text}")

    operation_url = response.headers["operation-location"]
    while True:
        result = requests.get(operation_url, headers=headers)
        data = result.json()
        if data["status"] in ["succeeded", "failed"]:
            break
        time.sleep(2)

    content = data.get("analyzeResult", {}).get("content", "")
    return content

def extract_fields_with_openai(text):
    headers = {
        "Content-Type": "application/json",
        "api-key": OPENAI_API_KEY
    }

    prompt = f"""
Abaixo está o conteúdo de uma nota fiscal. Extraia os seguintes dados: 
- Número da nota fiscal
- Chave de acesso
- Data de emissão
- CNPJ
- Nome da empresa
- Destinatário (CNPJ)
- Destinatário (Nome da empresa)

Se algum campo estiver ausente ou ilegível, indique como "Faltando".
Retorne sem nenhum tipo de formatação no texto.

Conteúdo:
{text}
"""

    payload = {
        "messages": [
            {"role": "system", "content": "Você é um assistente que extrai campos de documentos fiscais."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1,
        "max_tokens": 600
    }

    response = requests.post(OPENAI_ENDPOINT, headers=headers, json=payload)
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]

def main():
    folder_path = "../files"
    if not os.path.exists(folder_path):
        print("❌ Pasta ./files não encontrada.")
        return

    for filename in os.listdir(folder_path):
        if filename.lower().endswith((".pdf", ".png", ".jpg", ".jpeg", ".tiff")):
            file_path = os.path.join(folder_path, filename)
            print(f"📄 Processando: {filename}")
            try:
                texto = analyze_document(file_path)
                dados = extract_fields_with_openai(texto)
                print(f"✅ Resultado para {filename}:{dados}")
            except Exception as e:
                print(f"❌ Erro ao processar {filename}: {e}")

if __name__ == "__main__":
    main()
