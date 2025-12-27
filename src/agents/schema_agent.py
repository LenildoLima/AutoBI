# schema_agent.py

def gerar_schema(schema_detectado: dict) -> dict:
    columns = []

    for col in schema_detectado.get("temporais", []):
        columns.append({"name": col, "type": "date"})

    for col in schema_detectado.get("categoricas", []):
        columns.append({"name": col, "type": "category"})

    for col in schema_detectado.get("numericas", []):
        columns.append({"name": col, "type": "number"})

    return {"schema": {"columns": columns}}

