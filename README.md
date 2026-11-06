# PROJECT PITHOS (πίθος)
> **A 4D Planetary Intelligence & Conflict Forensics Engine for Humanity.**  
> Built to serve mankind by providing radical transparency into who profits from war (**Pandora**) and predictive foresight to safeguard civilian life (**Elpis**).

---

## Architecture Overview

Project Pithos brings together real-time OSINT telemetry, forensic knowledge graphs, and predictive kinematic & stochastic models into a unified 4D operational picture.

```
                            ┌──────────────────────────────┐
                            │        PROJECT PITHOS        │
                            │   The 4D Planetary Engine    │
                            └──────────────┬───────────────┘
                                           │
                   ┌───────────────────────┴───────────────────────┐
                   ▼                                               ▼
    ┌─────────────────────────────┐                 ┌─────────────────────────────┐
    │       MODULE: PANDORA       │                 │        MODULE: ELPIS        │
    │  The "Who & Why" Forensics  │                 │    The "Future" Forecaster  │
    ├─────────────────────────────┤                 ├─────────────────────────────┤
    │ • Arms procurement & money  │                 │ • 4D timeline scrubber      │
    │ • Shell company networks    │                 │ • Hawkes escalation math    │
    │ • Defense contracts         │                 │ • Civilian early warnings   │
    │ • Resource motive mapping   │                 │ • Anomaly surge detection   │
    └─────────────────────────────┘                 └─────────────────────────────┘
```

---

## Workspace Structure

The repository is organized as a polyglot monorepo:
* **Node.js / TypeScript Workspace:** Managed with `pnpm` (Next.js web app and shared UI/configs).
* **Python Services:** Managed with `uv` (FastAPI services backed by C++ engines like Kùzu and NumPy).

```text
pithos/
├── apps/
│   └── web/                   # Next.js 16 + Cesium 4D Tactical Globe (pnpm)
│
├── services/
│   ├── pandora/               # Forensic Knowledge Graph API (Python 3.12 / uv)
│   └── elpis/                 # Predictive Simulation & Hawkes Math API (Python 3.12 / uv)
│
├── packages/
│   ├── ui/                    # Shared React UI components (shadcn / Tailwind)
│   ├── typescript-config/     # Shared tsconfig definitions
│   └── eslint-config/         # Shared ESLint rules
│
├── pnpm-workspace.yaml        # Node workspace root
└── README.md                  # System Documentation
```

---

## Quickstart

### Prerequisites
* **Node.js:** `>= 20.x` or `24.x`
* **pnpm:** `>= 9.x`
* **Python:** `>= 3.11` (managed automatically via `uv`)
* **uv:** Install via `curl -LsSf https://astral.sh/uv/install.sh | sh`

### 1. Install & Build Web Application
```bash
# Install node dependencies
pnpm install

# Start Next.js frontend (http://localhost:3000)
pnpm --filter web dev
```

### 2. Start Pandora Service (Forensic Graph)
```bash
cd services/pandora
uv run uvicorn main:app --reload --port 8001
# API docs available at: http://localhost:8001/docs
```

### 3. Start Elpis Service (Predictive Simulation)
```bash
cd services/elpis
uv run uvicorn main:app --reload --port 8002
# API docs available at: http://localhost:8002/docs
```

---

## Detailed Component Documentation

* 🌐 [**Web Application (`apps/web`)**](apps/web/README.md): Next.js 16, Cesium 3D Photorealistic Tiles, 4D Timeline Scrubber, Tactical HUD, and shaders.
* 🔍 [**Pandora Service (`services/pandora`)**](services/pandora/README.md): Kùzu graph schema, defense contracts, entity resolution (RapidFuzz), and shell company de-cloaking.
* 🔮 [**Elpis Service (`services/elpis`)**](services/elpis/README.md): Hawkes point processes, Kalman trajectory smoothing, ST-DBSCAN anomaly detection, and civilian vulnerability models.

---

## Core Mission & Guiding Principles

1. **Symmetric Scrutiny:** Every military coalition, state actor, and defense prime is subject to the exact same algorithms. No national exemptions.
2. **Civilians First:** Predictive intelligence is designed to protect civilian corridors, monitor humanitarian supply lifelines, and eliminate surprise aggression.
3. **Open Source & Unclassified:** Exclusively uses openly broadcast telemetry (ADS-B, AIS) and unclassified public records (SIPRI, SAM.gov, OpenSanctions, GDELT).
