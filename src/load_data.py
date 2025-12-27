# load_data.py

import pandas as pd
from typing import Tuple, Dict, List
from collections import Counter
import re


def carregar_dados(caminho_csv: str) -> Tuple[pd.DataFrame, Dict[str, List[str]]]:
    """
    AGENTE DE INGESTÃO (ROBUSTO)

    Responsável por:
    - Ler qualquer CSV
    - Padronizar colunas
    - Inferir tipos corretamente
    - Tratar datas SEM warnings
    - Evitar datas falsas (1970-01-01)
    - Retornar DataFrame tratado + schema detectado
    """

    try:
        df = pd.read_csv(caminho_csv)
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_csv}")

    if df.empty:
        raise ValueError("O arquivo CSV está vazio.")

    # Padronização de colunas
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    schema = {
        "numericas": [],
        "categoricas": [],
        "temporais": []
    }

    total_linhas = len(df)

    for col in df.columns:
        serie = df[col]

        # ============================
        # 1️⃣ TENTATIVA NUMÉRICA PRIMEIRO
        # ============================
        tentativa_num = pd.to_numeric(serie, errors="coerce")

        if tentativa_num.notna().sum() / total_linhas >= 0.85:
            df[col] = tentativa_num
            schema["numericas"].append(col)
            continue

        # ============================
        # 2️⃣ DETECÇÃO DE ANO ISOLADO
        # ============================
        if re.search(r"year|ano", col):
            tentativa_ano = pd.to_numeric(serie, errors="coerce")
            if tentativa_ano.between(1900, 2100).sum() / total_linhas >= 0.85:
                df[col] = pd.to_datetime(
                    tentativa_ano.dropna().astype(int).astype(str) + "-01-01",
                    errors="coerce"
                )
                schema["temporais"].append(col)
                continue

        # ============================
        # 3️⃣ DETECÇÃO DE MÊS ISOLADO
        # ============================
        if re.search(r"month|mes", col):
            tentativa_mes = pd.to_numeric(serie, errors="coerce")
            if tentativa_mes.between(1, 12).sum() / total_linhas >= 0.85:
                df[col] = tentativa_mes.astype("Int64")
                schema["categoricas"].append(col)
                continue

        # ============================
        # 4️⃣ DETECÇÃO DE DATA COMPLETA
        # ============================
        valores = serie.dropna().astype(str)
        formatos_detectados = []

        for v in valores.sample(min(100, len(valores))):
            for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"):
                try:
                    pd.to_datetime(v, format=fmt)
                    formatos_detectados.append(fmt)
                    break
                except Exception:
                    continue

        formato_comum = Counter(formatos_detectados).most_common(1)

        if formato_comum:
            tentativa_data = pd.to_datetime(
                serie,
                format=formato_comum[0][0],
                errors="coerce"
            )

            if tentativa_data.notna().sum() / total_linhas >= 0.85:
                df[col] = tentativa_data
                schema["temporais"].append(col)
                continue

        # ============================
        # 5️⃣ CATEGÓRICA (FALLBACK FINAL)
        # ============================
        df[col] = serie.astype(str).str.strip()
        schema["categoricas"].append(col)

    # Limpeza final
    df = (
        df.dropna(how="all")
          .dropna(axis=1, how="all")
          .reset_index(drop=True)
    )

    return df, schema

