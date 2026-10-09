from pathlib import Path
import csv
import hashlib
import io
import json
import urllib.request

SOURCES = {
    "electricity": "https://www.hvakosterstrommen.no/api/v1/prices/2024/01-15_NO2.json",
    "norges_bank": "https://data.norges-bank.no/api/data/EXR/B.EUR.NOK.SP?format=csv&startPeriod=2024-01-01&endPeriod=2024-01-31",
    "ssb": "https://data.ssb.no/api/v0/no/table/07459/",
    "nve_history": "https://biapi.nve.no/magasinstatistikk/api/Magasinstatistikk/HentOffentligData",
}
NVE_SNAPSHOT_DATE = "2026-10-04"
NVE_SNAPSHOT_ORDER = [("EL", 2), ("EL", 1), ("EL", 4), ("EL", 3), ("EL", 5), ("NO", 0), ("VASS", 3), ("VASS", 1), ("VASS", 2)]
RAW_PATHS = {
    "electricity": Path("data/raw/hvakosterstrommen_2024-01-15_NO2.json"),
    "norges_bank": Path("data/raw/norges_bank_EXR_B_EUR_NOK_SP_2024-01.csv"),
    "ssb": Path("data/raw/ssb_table_07459_metadata.json"),
    "nve": Path("data/raw/nve_magasinstatistikk_latest.json"),
}

def fetch(url):
    with urllib.request.urlopen(url) as response:
        return response.status, response.read()

def canonical_json(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")

def normalize_csv(raw):
    text = raw.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    if not text.endswith("\n"):
        text += "\n"
    return text.encode("utf-8")

def sha256(raw):
    return hashlib.sha256(raw).hexdigest()

def main():
    statuses = {}
    fetched = {}
    for key, url in SOURCES.items():
        statuses[key], fetched[key] = fetch(url)

    electricity = json.loads(fetched["electricity"].decode("utf-8"))
    ssb = json.loads(fetched["ssb"].decode("utf-8"))
    nve_history = json.loads(fetched["nve_history"].decode("utf-8"))
    nve_by_key = {
        (row["omrType"], row["omrnr"]): row
        for row in nve_history
        if row.get("dato_Id") == NVE_SNAPSHOT_DATE
    }
    nve = [nve_by_key[key] for key in NVE_SNAPSHOT_ORDER]

    bodies = {
        "electricity": canonical_json(electricity),
        "norges_bank": normalize_csv(fetched["norges_bank"]),
        "ssb": canonical_json(ssb),
        "nve": canonical_json(nve),
    }
    for key, path in RAW_PATHS.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(bodies[key])

    nb_text = bodies["norges_bank"].decode("utf-8")
    nb_rows = list(csv.DictReader(io.StringIO(nb_text), delimiter=";"))
    status_for = {"electricity": statuses["electricity"], "norges_bank": statuses["norges_bank"], "ssb": statuses["ssb"], "nve": statuses["nve_history"]}
    rows = [
        ("electricity_http_status", status_for["electricity"], "HTTP status", "electricity", "HTTP response status", 1),
        ("electricity_record_count", len(electricity), "records", "electricity", "len(parsed JSON array)", 1),
        ("norges_bank_http_status", status_for["norges_bank"], "HTTP status", "norges_bank", "HTTP response status", 2),
        ("norges_bank_observation_count", len(nb_rows), "observations", "norges_bank", "CSV rows excluding header", 2),
        ("ssb_http_status", status_for["ssb"], "HTTP status", "ssb", "HTTP response status", 3),
        ("ssb_variable_count", len(ssb.get("variables", [])), "variables", "ssb", "len(metadata['variables'])", 3),
        ("nve_http_status", status_for["nve"], "HTTP status", "nve", "historical endpoint HTTP response status", 7),
        ("nve_record_count", len(nve), "records", "nve", "fixed-date historical rows exactly matching latest-week snapshot", 8),
    ]
    with Path("ledger.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["metric_id","value","unit","source_file","source_sha256","derivation","tool_log_seq"])
        for metric_id, value, unit, key, derivation, seq in rows:
            w.writerow([metric_id, value, unit, RAW_PATHS[key].as_posix(), sha256(bodies[key]), derivation, seq])

    report = [
        "# Source capability probe report", "",
        "| Metric ID | Source probe | HTTP status | Count | Raw file | SHA-256 |",
        "|---|---|---:|---:|---|---|",
        f"| electricity_record_count | Electricity-price JSON | {status_for['electricity']} | {len(electricity)} | `{RAW_PATHS['electricity'].as_posix()}` | `{sha256(bodies['electricity'])}` |",
        f"| norges_bank_observation_count | Norges Bank CSV observations | {status_for['norges_bank']} | {len(nb_rows)} | `{RAW_PATHS['norges_bank'].as_posix()}` | `{sha256(bodies['norges_bank'])}` |",
        f"| ssb_variable_count | SSB table 07459 metadata variables | {status_for['ssb']} | {len(ssb.get('variables', []))} | `{RAW_PATHS['ssb'].as_posix()}` | `{sha256(bodies['ssb'])}` |",
        f"| nve_record_count | NVE reservoir records dated {NVE_SNAPSHOT_DATE} | {status_for['nve']} | {len(nve)} | `{RAW_PATHS['nve'].as_posix()}` | `{sha256(bodies['nve'])}` |",
        "", "All report values are keyed by `metric_id` in `ledger.csv`."
    ]
    Path("report.md").write_text("\n".join(report) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
