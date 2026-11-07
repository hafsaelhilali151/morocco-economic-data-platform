import argparse
import logging
from pathlib import Path

import pandas as pd
from sqlalchemy import text

from db import get_engine

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("load_monia")

SAMPLES_DIR = Path(__file__).resolve().parent / "samples"

COLUMN_MAP = {
    "Indice MONIA": "indice_monia",
    "Volume JJ": "volume_jj",
    "Date de référence": "date_reference",
    "Date de publication": "date_publication",
}


def extract(path: Path) -> pd.DataFrame:
    """Lit le CSV tel quel : tout en texte, aucune conversion."""
    return pd.read_csv(
        path,
        sep=";",
        skiprows=2,              # 2 lignes de titre avant l'entête
        dtype=str,               # tout en TEXT, comme dans raw
        keep_default_na=False,   # ne pas transformer les vides en NaN
        encoding="utf-8-sig",
    )


def validate(df: pd.DataFrame) -> None:
    """Contrôles minimum : colonnes attendues présentes, fichier non vide."""
    missing = set(COLUMN_MAP) - set(df.columns)
    if missing:
        raise ValueError(f"Colonnes manquantes : {sorted(missing)}")
    if df.empty:
        raise ValueError("Le fichier ne contient aucune ligne")


def to_raw_shape(df: pd.DataFrame, filename: str) -> pd.DataFrame:
    """Renomme les colonnes et ajoute la provenance. Les valeurs ne changent pas."""
    out = df[list(COLUMN_MAP)].rename(columns=COLUMN_MAP)
    out["_source_file"] = filename
    return out


def already_loaded(engine, filename: str) -> bool:
    query = text("SELECT 1 FROM raw.monia WHERE _source_file = :f LIMIT 1")
    with engine.connect() as conn:
        return conn.execute(query, {"f": filename}).first() is not None


def load_raw(df: pd.DataFrame, engine) -> None:
    df.to_sql(
        "monia",
        engine,
        schema="raw",
        if_exists="append",
        index=False,
        method="multi",
        chunksize=500,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Charge un CSV MONIA dans raw.monia")
    parser.add_argument("path", nargs="?", type=Path, help="Chemin du CSV MONIA")
    args = parser.parse_args()

    path = args.path or next(SAMPLES_DIR.glob("Indice-monia*.csv"))
    log.info("Fichier : %s", path.name)

    engine = get_engine()

    if already_loaded(engine, path.name):
        log.warning("Fichier déjà chargé, on saute.")
        return

    df = extract(path)
    validate(df)
    df = to_raw_shape(df, path.name)

    load_raw(df, engine)
    log.info("%d lignes chargées dans raw.monia", len(df))


if __name__ == "__main__":
    main()