# Source capability probe report

| Metric ID | Source probe | HTTP status | Count | Raw file | SHA-256 |
|---|---|---:|---:|---|---|
| electricity_record_count | Electricity-price JSON | 200 | 24 | `data/raw/hvakosterstrommen_2024-01-15_NO2.json` | `487085e0a60e8e21f5b126f13f6594c7131eb0390699f5cb5515bab7f3bedeac` |
| norges_bank_observation_count | Norges Bank CSV observations | 200 | 22 | `data/raw/norges_bank_EXR_B_EUR_NOK_SP_2024-01.csv` | `86e94ad526fc1cf5f20234171b5c4b4d8cb5ce8186d7f95c2a43f4daacae7f1a` |
| ssb_variable_count | SSB table 07459 metadata variables | 200 | 5 | `data/raw/ssb_table_07459_metadata.json` | `1e2768f2a7d5df087e72078b976a4718b368ef141107c37b32af43a189cc5b9d` |
| nve_record_count | NVE reservoir records dated 2026-10-04 | 200 | 9 | `data/raw/nve_magasinstatistikk_latest.json` | `0b44cb8eb5df14a59787597516db3c402a23f48d40c2d7c60abb177121df78f0` |

All report values are keyed by `metric_id` in `ledger.csv`.
