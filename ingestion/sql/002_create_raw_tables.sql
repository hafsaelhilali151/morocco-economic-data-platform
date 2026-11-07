CREATE TABLE IF NOT EXISTS raw.monia (
    indice_monia      TEXT,
    volume_jj         TEXT,
    date_reference    TEXT,
    date_publication  TEXT,
    _source_file      TEXT,
    _ingested_at      TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS raw.cours_reference (
    devise        TEXT,
    date_cours    TEXT,
    cours_moyen   TEXT,
    _source_file  TEXT,
    _ingested_at  TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS raw.bons_tresor (
    date_reglement             TEXT,
    maturite                   TEXT,
    caracteristiques           TEXT,
    montant_propose            TEXT,
    taux_prix_min              TEXT,
    taux_prix_max              TEXT,
    montant_adjuge             TEXT,
    taux_prix_limite           TEXT,
    taux_prix_moyen_pondere    TEXT,
    _source_file               TEXT,
    _ingested_at               TIMESTAMPTZ DEFAULT now()
);