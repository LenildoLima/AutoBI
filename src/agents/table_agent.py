# autoBi/src/agents/table_agent.py

import pandas as pd

def gerar_tabelas(df: pd.DataFrame, schema: dict) -> dict:
    """
    Gera a estrutura da tabela e popula com os dados reais do DataFrame.
    """
    # Selecionamos as colunas baseadas no schema detectado
    colunas = [c["name"] for c in schema["schema"]["columns"]]
    
    # Convertemos as primeiras 100 linhas para uma lista de dicionários
    # O orient="records" cria o formato: [{"col1": val1, "col2": val2}, ...]
    dados_preview = df[colunas].head(100).to_dict(orient="records")

    return {
        "tables": [
            {
                "id": "tabela_principal",
                "title": "Visualização dos Dados",
                "columns": colunas,
                "rows": dados_preview,
                "pagination": True,
                "total_rows": len(df)
            }
        ]
    }

