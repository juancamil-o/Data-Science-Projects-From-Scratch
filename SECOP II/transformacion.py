# transformacion.py
import os
from datetime import date, timedelta
import pandas as pd

# -------- Config por defecto (puedes sobreescribir al llamar la función) --------
DEFAULT_JSON_PATH = os.getenv("JSON_PATH", "datosDeHoy.json")   # NDJSON que generas en extracción
DEFAULT_OUT_DIR   = os.getenv("OUT_DIR", "datos")               # carpeta Silver
DEFAULT_FORMAT    = os.getenv("OUT_FORMAT", "parquet")          # "parquet" | "csv" | "ndjson"

# Campos que solemos normalizar (ajusta a tus columnas reales)
NUMERIC_COLS = ["nit_entidad", "documento_proveedor", "valor_del_contrato"]
DATE_COL     = "fecha_de_firma"

def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def _leer_json_flexible(path: str) -> pd.DataFrame:
    # Soporta JSON Lines y array JSON
    try:
        return pd.read_json(path, lines=True)
    except ValueError:
        return pd.read_json(path)

def _coerce_numeric(df: pd.DataFrame, cols=NUMERIC_COLS) -> pd.DataFrame:
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

def transformar_datos_del_dia(
    dias_retro: int | str = 1,
    json_path: str = DEFAULT_JSON_PATH,
    out_dir: str = DEFAULT_OUT_DIR,
    out_format: str = DEFAULT_FORMAT,
) -> tuple[str, int]:
    """
    Lee el NDJSON de extracción, limpia tipos y guarda el *subset del día objetivo*
    como un archivo diario en ./datos/<YYYY-MM-DD>.(parquet|csv|ndjson).

    Devuelve (ruta_archivo, filas_escritas).
    """
    # Normaliza dias_retro
    try:
        d = int(dias_retro)
    except (TypeError, ValueError):
        raise ValueError("dias_retro debe ser entero o string convertible a entero")

    # Fecha objetivo
    fecha_obj = date.today() - timedelta(days=d)
    fecha_str = fecha_obj.strftime("%Y-%m-%d")

    # Leer datos crudos
    df = _leer_json_flexible(json_path).copy()

    # Parseo de fecha (si existe) y filtrado del día
    if DATE_COL in df.columns:
        df[DATE_COL] = pd.to_datetime(df[DATE_COL], errors="coerce")
        df = df[df[DATE_COL].dt.strftime("%Y-%m-%d") == fecha_str].copy()
    else:
        # Si no existe la columna de fecha, escribimos todo el lote como día objetivo
        df = df.copy()
        df["fecha_objetivo"] = fecha_str

    # Normalizaciones
    df = _coerce_numeric(df)

    # Salida
    _ensure_dir(out_dir)
    if out_format.lower() == "parquet":
        out_path = os.path.join(out_dir, f"{fecha_str}.parquet")
        # requiere pyarrow instalado
        df.to_parquet(out_path, index=False)
    elif out_format.lower() == "csv":
        out_path = os.path.join(out_dir, f"{fecha_str}.csv")
        df.to_csv(out_path, index=False)
    elif out_format.lower() in ("ndjson", "jsonl"):
        out_path = os.path.join(out_dir, f"{fecha_str}.ndjson")
        with open(out_path, "w", encoding="utf-8") as f:
            for rec in df.to_dict(orient="records"):
                f.write(pd.io.json.dumps(rec, ensure_ascii=False) + "\n")
    else:
        raise ValueError("OUT_FORMAT inválido. Usa 'parquet', 'csv' o 'ndjson'.")

    print(f"✅ Silver diario escrito: {out_path} ({len(df)} filas)")
    return out_path, len(df)
