# autoBi/src/agents/manager_agent.py

from src.agents.schema_agent import gerar_schema
from src.agents.kpi_agent import gerar_kpis
from src.agents.charts_agent import gerar_charts
from src.agents.table_agent import gerar_tabelas
from src.agents.filter_agent import gerar_filtros

def gerar_dashboard_payload(df, schema_detectado):
    # 1. Primeiro geramos o Schema (que agora tem os labels amigáveis)
    # Ele é a "espinha dorsal" para os outros agentes
    schema = gerar_schema(schema_detectado)

    # 2. Combinamos as respostas de todos os agentes especialistas
    return {
        **schema,                             # Estrutura de colunas e tipos
        **gerar_kpis(df),                     # Totais e médias (formatados)
        **gerar_charts(df, schema),           # Definições de gráficos (com labels)
        **gerar_tabelas(df, schema),          # Dados reais para a grade (head 100)
        **gerar_filtros(schema)               # Configuração dos filtros de UI
    }



