# autoBi/src/main.py

from src.load_data import carregar_dados
from src.agents.manager_agent import gerar_dashboard_payload


def run(caminho_entrada: str):
    df, schema_detectado = carregar_dados(caminho_entrada)
    return gerar_dashboard_payload(df, schema_detectado)

