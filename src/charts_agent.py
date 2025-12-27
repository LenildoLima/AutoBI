# charts_agent.py

def gerar_charts(schema: dict) -> dict:
    charts = []

    cols = schema["schema"]["columns"]

    numericas = [c["name"] for c in cols if c["type"] == "number"]
    categoricas = [c["name"] for c in cols if c["type"] == "category"]
    temporais = [c["name"] for c in cols if c["type"] == "date"]

    for d in temporais:
        for n in numericas:
            charts.append({
                "type": "line",
                "x": d,
                "y": n,
                "aggregation": "sum",
                "title": f"{n} ao longo do tempo"
            })

    for c in categoricas:
        for n in numericas:
            charts.append({
                "type": "bar",
                "x": c,
                "y": n,
                "aggregation": "sum",
                "title": f"{n} por {c}"
            })

    return {"charts": charts}
