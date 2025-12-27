# table_agent.py

def gerar_tabelas(schema: dict) -> dict:
    return {
        "tables": [
            {
                "columns": [c["name"] for c in schema["schema"]["columns"]],
                "pagination": True
            }
        ]
    }

