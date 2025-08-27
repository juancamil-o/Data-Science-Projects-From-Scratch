# transformacion.py
import os
from datetime import date, timedelta
import pandas as pd
import fsspec  # para NDJSON en S3

DEFAULT_JSON_PATH = os.getenv("JSON_PATH", "datosDeHoy.json")
DEFAULT_OUT_DIR   = os.getenv("OUT_DIR", "datos")  # puede ser "s3://mi-bucket/datos"
DEFAULT_FORMAT    = os.getenv("OUT_FORMAT", "parquet")

NUMERIC_COLS = ["nit_entidad", "documento_proveedor", "valor_del_contrato"]
DATE_COL     = "fecha_de_firma"

def _leer_json_flexible(path: str) -> pd.DataFrame:
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
    out_dir: str = DEFAULT_OUT_DIR,                 # <-- acepta "s3://bucket/datos"
    out_format: str = DEFAULT_FORMAT,               # "parquet" | "csv" | "ndjson"
    storage_options: dict | None = None,            # dict para credenciales/perfil/endpoint
) -> tuple[str, int]:
    """
    Escribe un archivo diario en out_dir/AAAA-MM-DD.(parquet|csv|ndjson).
    Soporta rutas locales y S3.
    """
    try:
        d = int(dias_retro)
    except (TypeError, ValueError):
        raise ValueError("dias_retro debe ser entero o convertible a entero")

    fecha_str = (date.today() - timedelta(days=d)).strftime("%Y-%m-%d")

    df = _leer_json_flexible(json_path).copy()
    if DATE_COL in df.columns:
        df[DATE_COL] = pd.to_datetime(df[DATE_COL], errors="coerce")
        df = df[df[DATE_COL].dt.strftime("%Y-%m-%d") == fecha_str].copy()
    else:
        df["fecha_objetivo"] = fecha_str

    df = _coerce_numeric(df)

    # Construye la ruta de salida
    suffix = {"parquet": "parquet", "csv": "csv", "ndjson": "ndjson", "jsonl": "ndjson"}[out_format.lower()]
    out_path = f"{out_dir.rstrip('/')}/{fecha_str}.{suffix}"

    # Si es local, crea carpeta; en S3 no hace falta (prefijo “lógico”)
    if not out_dir.startswith("s3://"):
        os.makedirs(out_dir, exist_ok=True)

    # Escribir según formato
    if suffix == "parquet":
        df.to_parquet(out_path, index=False, storage_options=storage_options)
    elif suffix == "csv":
        df.to_csv(out_path, index=False, storage_options=storage_options)
    else:  # ndjson
        # fsspec gestiona la conexión a S3
        with fsspec.open(out_path, "w", **(storage_options or {})) as f:
            for rec in df.to_dict(orient="records"):
                # evita dependencias extra; usa json estándar
                import json as _json
                f.write(_json.dumps(rec, ensure_ascii=False) + "\n")

    print(f"✅ Silver diario escrito: {out_path} ({len(df)} filas)")
    return out_path, len(df)
