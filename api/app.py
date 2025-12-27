# app.py

# api/app.py

from fastapi import FastAPI, UploadFile, File
import shutil
import os
import uuid
import sys

# 🔹 Adiciona o root do projeto ao path para achar main.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.main import run

app = FastAPI(title="API Multiagente de Análise de Dados")

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def root():
    return {"status": "ok", "message": "API Multiagente ativa"}


@app.post("/analisar")
def analisar_csv(arquivo: UploadFile = File(...)):
    """
    Recebe qualquer CSV, salva temporariamente e devolve análise completa.
    """
    # Cria nome único para evitar conflito
    nome_arquivo = f"{uuid.uuid4()}_{arquivo.filename}"
    caminho_arquivo = os.path.join(UPLOAD_DIR, nome_arquivo)

    # Salva o arquivo enviado
    with open(caminho_arquivo, "wb") as f:
        shutil.copyfileobj(arquivo.file, f)

    # Executa o pipeline multiagente
    resultado = run(caminho_arquivo)

    return resultado



