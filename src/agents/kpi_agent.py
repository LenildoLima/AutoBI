# autoBi/src/agents/kpi_agent.py

def gerar_kpis(df):
    kpis_formatados = []
    
    numericas = df.select_dtypes(include=["int", "float"]).columns
    
    for col in numericas:
        valor_total = float(df[col].sum())
        
        # Lógica simples para decidir o formato
        formato = "currency" if "receita" in col or "preco" in col or "valor" in col else "number"
        
        kpis_formatados.append({
            "label": f"Total de {col.replace('_', ' ').title()}",
            "value": round(valor_total, 2),
            "format": formato
        })

    return {"kpis": kpis_formatados}


