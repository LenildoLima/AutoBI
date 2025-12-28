# autoBi/src/agents/filter_agent.py

def gerar_filtros(schema: dict) -> dict:
    filtros = []

    # Agora iteramos sobre as colunas que já possuem o 'label' vindo do schema_agent
    for col in schema["schema"]["columns"]:
        nome_tecnico = col["name"]
        nome_exibicao = col.get("label", nome_tecnico) # Fallback para o nome técnico se o label não existir
        tipo = col["type"]

        # Estrutura base do filtro seguindo o contrato
        filtro_base = {
            "field": nome_tecnico,
            "label": nome_exibicao, # O frontend usará isso no título do dropdown/input
        }

        if tipo == "date":
            filtro_base["type"] = "date_range"
        elif tipo == "category":
            filtro_base["type"] = "select"
        elif tipo == "number":
            filtro_base["type"] = "range"
        
        filtros.append(filtro_base)

    return {"filters": filtros}

