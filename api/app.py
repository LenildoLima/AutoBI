# /autoBi/api/app.py

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import uuid
import sys

# 🔹 Adiciona o root do projeto ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.main import run

app = FastAPI(
    title="API Multiagente de Análise de Dados",
    version="1.0.0"
)

# 🔹 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ======================================================
# 🔹 ROTAS BÁSICAS
# ======================================================

@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "API Multiagente ativa"
    }

# ======================================================
# 🔹 ROTA DE UPLOAD (COMPATÍVEL COM LOVABLE)
# ======================================================

@app.post("/analisar")
def analisar_arquivo(file: UploadFile = File(...)):
    """
    Recebe um arquivo CSV enviado pelo frontend (Lovable),
    salva temporariamente e devolve a análise completa.
    """

    nome_arquivo = f"{uuid.uuid4()}_{file.filename}"
    caminho_arquivo = os.path.join(UPLOAD_DIR, nome_arquivo)

    with open(caminho_arquivo, "wb") as f:
        shutil.copyfileobj(file.file, f)

    resultado = run(caminho_arquivo)
    return resultado

# ======================================================
# 🔹 ROTAS PARA O AUTO BI
# ======================================================

@app.get("/datasets")
def listar_datasets():
    return {
        "datasets": [
            {
                "id": "upload",
                "name": "Arquivo enviado pelo usuário"
            }
        ]
    }

@app.get("/datasets/{dataset_id}/analysis")
def analisar_dataset(dataset_id: str):
    arquivos = [f for f in os.listdir(UPLOAD_DIR) if f.endswith(".csv")]

    if not arquivos:
        return {"error": "Nenhum arquivo CSV disponível. Envie um arquivo primeiro."}

    arquivos.sort(key=lambda x: os.path.getmtime(os.path.join(UPLOAD_DIR, x)))
    caminho_arquivo = os.path.join(UPLOAD_DIR, arquivos[-1])

    resultado = run(caminho_arquivo)
    return resultado
