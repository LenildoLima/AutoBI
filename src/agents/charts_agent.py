# autoBi/src/agents/charts_agent.py

import pandas as pd

def gerar_charts(df: pd.DataFrame, schema: dict) -> dict:
    charts = []
    cols = schema["schema"]["columns"]

    # Busca o label amigável baseado no nome técnico
    def get_label(name):
        return next((c["label"] for c in cols if c["name"] == name), name)

    colunas_data = [c["name"] for c in cols if c["type"] == "date"]
    colunas_num = [c["name"] for c in cols if c["type"] == "number"]
    colunas_cat = [c["name"] for c in cols if c["type"] == "category"]

    if colunas_data and colunas_num:
        y_col = colunas_num[0]
        charts.append({
            "type": "line",
            "x": colunas_data[0],
            "y": y_col,
            "title": f"Evolução de {get_label(y_col)}"
        })

    if colunas_cat and colunas_num:
        y_col = colunas_num[0]
        x_col = colunas_cat[0]
        charts.append({
            "type": "bar",
            "x": x_col,
            "y": y_col,
            "title": f"{get_label(y_col)} por {get_label(x_col)}"
        })

    return {"charts": charts}

