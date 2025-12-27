import pandas as pd

def gerar_charts(df: pd.DataFrame, schema: dict) -> dict:
    charts = []

    colunas_data = [c["name"] for c in schema["schema"]["columns"] if c["type"] == "date"]
    colunas_num = [c["name"] for c in schema["schema"]["columns"] if c["type"] == "number"]
    colunas_cat = [c["name"] for c in schema["schema"]["columns"] if c["type"] == "category"]

    if colunas_data and colunas_num:
        charts.append({
            "type": "line",
            "x": colunas_data[0],
            "y": colunas_num[0],
            "title": f"Evolução de {colunas_num[0]}"
        })

    if colunas_cat and colunas_num:
        charts.append({
            "type": "bar",
            "x": colunas_cat[0],
            "y": colunas_num[0],
            "title": f"{colunas_num[0]} por {colunas_cat[0]}"
        })

    return {"charts": charts}

