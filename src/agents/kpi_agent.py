# kpi_agent.py

def gerar_kpis(df):
    kpis = []

    numericas = df.select_dtypes(include=["int", "float"]).columns
    temporais = df.select_dtypes(include=["datetime64[ns]"]).columns

    for col in numericas:
        kpis.append({
            "field": col,
            "sum": round(float(df[col].sum()), 2),
            "avg": round(float(df[col].mean()), 2),
            "min": round(float(df[col].min()), 2),
            "max": round(float(df[col].max()), 2)
        })

    for col in temporais:
        kpis.append({
            "field": col,
            "min": str(df[col].min().date()),
            "max": str(df[col].max().date())
        })

    return {"kpis": kpis}


