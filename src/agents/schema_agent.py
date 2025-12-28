# autooBi/src/agents/schema_agent.py

def format_label(text: str) -> str:
    """Transforma snake_case em Proper Case (ex: receita_total -> Receita Total)"""
    return text.replace("_", " ").title()

def gerar_schema(schema_detectado: dict) -> dict:
    columns = []

    # Mapeamento de tipos para o Dashboard
    mapa_tipos = {
        "temporais": "date",
        "categoricas": "category",
        "numericas": "number"
    }

    for grupo, tipo_label in mapa_tipos.items():
        for col in schema_detectado.get(grupo, []):
            columns.append({
                "name": col,
                "label": format_label(col), # Nome amigável para o cabeçalho
                "type": tipo_label
            })

    return {"schema": {"columns": columns}}

