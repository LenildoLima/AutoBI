# teste_charts.py

import pandas as pd
from charts_agent import gerar_graficos_para_lovable

# 1. Carregar CSV de vendas (ou DataFrame já tratado)
df = pd.read_csv("data/vendas_tratadas.csv")

# 2. Gerar gráficos
graficos = gerar_graficos_para_lovable(df)

# 3. Exibir gráficos interativos
# Plotly abre automaticamente no navegador se rodar show()
for nome, grafico in graficos.items():
    print(f"Exibindo gráfico: {nome}")
    grafico.show()
