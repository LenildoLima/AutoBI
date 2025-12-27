# filter_agent.py

def gerar_filtros(schema: dict) -> dict:
    filtros = []

    for col in schema["schema"]["columns"]:
        if col["type"] == "date":
            filtros.append({"field": col["name"], "type": "date_range"})
        elif col["type"] == "category":
            filtros.append({"field": col["name"], "type": "select"})
        elif col["type"] == "number":
            filtros.append({"field": col["name"], "type": "range"})

    return {"filters": filtros}

