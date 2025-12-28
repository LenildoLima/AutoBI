# autoBi/src/analysis.py 

import pandas as pd
from typing import Dict, List, Tuple


def carregar_dados(caminho_csv: str) -> Tuple[pd.DataFrame, Dict[str, List[str]]]:
    if not caminho_csv:
        raise ValueError("Caminho do arquivo não informado")

    df = pd.read_csv(caminho_csv)

    if df.empty:
        raise ValueError("CSV vazio")

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

    total = len(df)

    for col in df.columns:
        tentativa_data = pd.to_datetime(df[col], errors="coerce", dayfirst=True)
        if tentativa_data.notna().sum() / total >= 0.8:
            df[col] = tentativa_data
            schema["temporais"].append(col)
            continue

        tentativa_num = pd.to_numeric(df[col], errors="coerce")
        if tentativa_num.notna().sum() / total >= 0.8:
            df[col] = tentativa_num
            schema["numericas"].append(col)
            continue

        df[col] = df[col].astype(str).str.strip()
        schema["categoricas"].append(col)

    df = df.dropna(how="all").dropna(axis=1, how="all").reset_index(drop=True)

    return df, schema
