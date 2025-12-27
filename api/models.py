# models.py

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


# =========================
# Schema detectado
# =========================

class SchemaDetectado(BaseModel):
    numericas: List[str] = Field(..., example=["receita", "quantidade"])
    categoricas: List[str] = Field(..., example=["loja", "categoria"])
    temporais: List[str] = Field(..., example=["data"])


# =========================
# KPI genérico
# =========================

class KPIValores(BaseModel):
    soma: float
    media: float
    min: float
    max: float


class KPIsGenericos(BaseModel):
    """
    KPIs por coluna numérica.
    Ex:
    {
        "receita": { "soma": 10000, "media": 500, ... },
        "quantidade": { ... }
    }
    """
    kpis: Dict[str, KPIValores]


# =========================
# Definição de gráfico
# =========================

class DefinicaoGrafico(BaseModel):
    type: str = Field(..., example="bar")
    title: str = Field(..., example="Receita por loja")
    x: str = Field(..., example="loja")
    y: str = Field(..., example="receita")
    aggregation: Optional[str] = Field(None, example="sum")
    top_n: Optional[int] = Field(None, example=10)


# =========================
# Resposta do dashboard
# =========================

class DashboardResponse(BaseModel):
    schema: SchemaDetectado
    kpis: Dict[str, KPIValores]
    graficos: List[DefinicaoGrafico]


# =========================
# Filtros genéricos
# =========================

class FiltroTemporal(BaseModel):
    inicio: Optional[str] = None
    fim: Optional[str] = None


class Filtros(BaseModel):
    """
    Exemplo:
    {
        "loja": "SP",
        "data": { "inicio": "2024-01-01", "fim": "2024-12-31" }
    }
    """
    filtros: Dict[str, Any]
