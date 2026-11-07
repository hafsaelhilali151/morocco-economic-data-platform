# Modèle de données (couche marts)

| Table | Type | Grain (1 ligne = ...) | Colonnes clés |
|---|---|---|---|
| dim_date | Dimension | un jour | date_key, date, année, mois, jour, jour de semaine |
| dim_currency | Dimension | une devise | currency_key, libellé, multiplicateur (1, 10, 100) |
| dim_maturity | Dimension | une maturité de bon du Trésor | maturity_key, libellé |
| fact_monia | Fait | un jour | date_key, taux (%), volume (MDH) |
| fact_exchange_rate | Fait | une devise x un jour | date_key, currency_key, cours en MAD pour 1 unité |
| fact_treasury_auction | Fait | une maturité x une adjudication | date_key, maturity_key, montant proposé, montant adjugé, taux moyen pondéré |