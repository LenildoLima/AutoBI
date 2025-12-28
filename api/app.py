# /autoBi/api/app.py

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import uuid
import sys

# 🔹 Adiciona o root do projeto ao path para achar main.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.main import run

app = FastAPI(
    title="API Multiagente de Análise de Dados",
    version="1.0.0"
)

# 🔹 CORS (necessário para Lovable, frontend, ngrok, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # depois podemos restringir
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
# 🔹 ROTA EXISTENTE (mantida)
# ======================================================

@app.post("/analisar")
def analisar_arquivo(arquivo: UploadFile = File(...)):
    """
    Recebe um arquivo (CSV por enquanto),
    salva temporariamente e devolve análise completa.
    """
    nome_arquivo = f"{uuid.uuid4()}_{arquivo.filename}"
    caminho_arquivo = os.path.join(UPLOAD_DIR, nome_arquivo)

    with open(caminho_arquivo, "wb") as f:
        shutil.copyfileobj(arquivo.file, f)

    resultado = run(caminho_arquivo)

    return resultado


# ======================================================
# 🔹 NOVAS ROTAS PARA O LOVABLE (AUTO BI)
# ======================================================

@app.get("/datasets")
def listar_datasets():
    """
    Lista datasets disponíveis para o dashboard.
    Por enquanto são exemplos fixos.
    No futuro: banco, múltiplos uploads, histórico.
    """
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
    if not os.path.exists(UPLOAD_DIR):
        return {"error": "Diretório de uploads não existe."}
        
    arquivos = [f for f in os.listdir(UPLOAD_DIR) if f.endswith('.csv')]

    if not arquivos:
        return {"error": "Nenhum arquivo CSV disponível. Envie um arquivo primeiro."}

    # Pega o arquivo mais recente
    arquivos.sort(key=lambda x: os.path.getmtime(os.path.join(UPLOAD_DIR, x)))
    caminho_arquivo = os.path.join(UPLOAD_DIR, arquivos[-1])

    try:
        resultado = run(caminho_arquivo)
        return resultado # Retornando o JSON limpo, sem a vírgula
    except Exception as e:
        return {"error": f"Erro ao processar análise: {str(e)}"}