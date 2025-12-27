# manager_agent.py

from src.agents.schema_agent import gerar_schema
from src.agents.kpi_agent import gerar_kpis
from src.agents.charts_agent import gerar_charts
from src.agents.table_agent import gerar_tabelas
from src.agents.filter_agent import gerar_filtros


def gerar_dashboard_payload(df, schema_detectado):
    schema = gerar_schema(schema_detectado)

    return {
        **schema,
        **gerar_kpis(df),
        **gerar_charts(df, schema),   # df + schema é correto aqui
        **gerar_tabelas(schema),      # só schema, sem df
        **gerar_filtros(schema)
    }



