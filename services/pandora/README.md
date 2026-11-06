# PANDORA SERVICE (services/pandora)
> **The Forensic Knowledge Graph Engine — Unmasking the "Who & Why" of Global Conflict.**

Pandora answers the legal and ethical question: ***Cui bono?* ("Who profits?")**  
It ingests open defense contracts, beneficial corporate ownership trees, and arms delivery records to trace the money behind active battlefields and military logistics.

---

## Tech Stack & Dependencies

* **Language:** Python 3.12+ (managed with `uv`)
* **API Framework:** `fastapi`, `uvicorn`, `pydantic`
* **Graph Engine:** `kuzu` (Embedded, in-process C++ property graph database)
* **Entity Resolution & Deduplication:** `rapidfuzz` (fuzzy string matching)
* **Data Processing & Scrapers:** `polars` (high-performance tabular queries), `httpx` (async HTTP)

---

## Directory & File Blueprint

```text
services/pandora/
├── pyproject.toml
├── uv.lock
├── README.md
├── main.py                     # FastAPI server entry point
│
├── graph/                      # Kùzu Graph Engine
│   ├── __init__.py
│   ├── db.py                   # Kùzu Database connection pool & lifecycle
│   ├── schema.py               # Node & Rel table DDL scripts (Cypher)
│   └── queries.py              # Centrality, shell traversal, and Cui Bono queries
│
├── ingestion/                  # Public Data Ingestion Pipelines
│   ├── __init__.py
│   ├── sam_gov.py              # US DoD contract awards (SAM.gov / FPDS)
│   ├── ted_eu.py               # EU Defense procurement notices (TED)
│   ├── sipri.py                # SIPRI Major Conventional Arms Transfers
│   ├── open_sanctions.py       # OFAC, UN, EU sanctions & front companies
│   └── opencorporates.py       # Beneficial ownership & offshore registries
│
├── resolution/                 # Entity Matching & Deduplication
│   ├── __init__.py
│   └── matcher.py              # Normalizes noisy names into canonical entity IDs
│
└── models/                     # Pydantic Schemas
    ├── __init__.py
    ├── cui_bono.py             # Schema for the UI slide-out inspection dossier
    └── entity.py               # Nodes (Company, Contract, Weapon, Actor)
```

---

## Kùzu Graph Schema (Nodes & Relationships)

### 1. Node Tables
* **`Company`**: `id STRING, name STRING, country STRING, ticker STRING, is_shell BOOLEAN, PRIMARY KEY (id)`
* **`Contract`**: `id STRING, title STRING, agency STRING, amount_usd INT64, award_date DATE, PRIMARY KEY (id)`
* **`WeaponSystem`**: `id STRING, name STRING, category STRING, PRIMARY KEY (id)` (e.g., 155mm Shell, Patriot PAC-3)
* **`Actor`**: `id STRING, name STRING, type STRING, PRIMARY KEY (id)` (Nation state, militia, government department)
* **`ResourceDeposit`**: `id STRING, name STRING, mineral_type STRING, lat DOUBLE, lon DOUBLE, PRIMARY KEY (id)`

### 2. Relationship (Rel) Tables
* **`OWNS`** (`FROM Company TO Company`): `percent_equity DOUBLE` (Detects multi-tier offshore shell networks)
* **`AWARDED_TO`** (`FROM Contract TO Company`)
* **`FUNDED_BY`** (`FROM Contract TO Actor`)
* **`MANUFACTURES`** (`FROM Company TO WeaponSystem`)
* **`SUPPLIED`** (`FROM WeaponSystem TO Actor`): `quantity INT64, year INT64`
* **`CONTESTS`** (`FROM Actor TO ResourceDeposit`): Direct link between military clashes and critical mineral/oil deposits

---

## Core API Endpoints to Implement in `main.py`

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/cui-bono/{entity_id}` | Returns complete financial trail: manufacturer, prime contractor, contracts, and stock ticker. |
| `GET` | `/api/v1/network/ownership-chain/{company_id}` | Traverses the `OWNS` edges to uncover ultimate beneficial owners through offshore shells. |
| `GET` | `/api/v1/contracts/search?q={query}` | Searches defense procurement database for contracts matching weapon types or keywords. |
| `GET` | `/api/v1/resources/motives?lat={lat}&lon={lon}&radius_km=100` | Checks whether active conflict coordinates intersect with mining or energy concessions. |

---

## Implementation Roadmap (Step-by-Step)

### Phase 1: Database Initialization (`graph/db.py` & `schema.py`)
1. Implement `KuzuDatabase` singleton class managing the local Kùzu database file (`./data/pandora_kuzu`).
2. Write initial DDL queries in `schema.py` to create the Node and Rel tables on startup.

### Phase 2: Ingestion Baseline (`ingestion/sipri.py` & `sam_gov.py`)
1. Ingest SIPRI conventional arms transfers CSV (provides ground truth on which states supply arms to other states).
2. Build an async client for SAM.gov public contract notices to ingest DoD defense prime awards.

### Phase 3: Entity Resolution (`resolution/matcher.py`)
1. Use `rapidfuzz.process.extractOne` with token-sort ratio to map variants (e.g., *"Lockheed Martin Global Inc."*, *"Lockheed Martin Overseas Ltd."*) to canonical entity ID `LMT`.

### Phase 4: Fast Cypher Queries (`graph/queries.py`)
1. Implement `get_cui_bono_dossier(entity_name: str)`:
   ```cypher
   MATCH (c:Company)-[:MANUFACTURES]->(w:WeaponSystem)
   OPTIONAL MATCH (k:Contract)-[:AWARDED_TO]->(c)
   OPTIONAL MATCH (parent:Company)-[:OWNS]->(c)
   WHERE w.name = $weapon_name OR c.name = $company_name
   RETURN c, w, k, parent;
   ```
2. Connect queries to FastAPI route handlers.

---

## Running the Service
```bash
# Inside services/pandora
uv run uvicorn main:app --reload --port 8001
```
Interactive Swagger docs: `http://localhost:8001/docs`
