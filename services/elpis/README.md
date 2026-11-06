# ELPIS SERVICE (services/elpis)
> **The Predictive Simulation Engine — 4D Foresight & Civilian Safeguarding.**

Elpis translates physical telemetry and historical event streams into **forward probabilistic simulation**.  
Its mission is to eliminate strategic surprise, detect military build-ups weeks before kinetic action, and provide early warnings so civilians and humanitarian organizations have time to act.

---

## Tech Stack & Dependencies

* **Language:** Python 3.12+ (managed with `uv`)
* **API Framework:** `fastapi`, `uvicorn`, `pydantic`
* **Mathematics & Optimization:** `numpy`, `scipy`
* **State Estimation & Kinematics:** `filterpy` (Extended Kalman Filter & Particle Filters)
* **Point Process Forecasting:** `tick` (Hawkes point processes) or custom vectorized NumPy MLE kernel

---

## Directory & File Blueprint

```text
services/elpis/
├── pyproject.toml
├── uv.lock
├── README.md
├── main.py                     # FastAPI server entry point
│
├── math_models/                # Mathematical & Stochastic Models
│   ├── __init__.py
│   ├── hawkes.py               # Multivariate Hawkes Point Process (escalation cascade)
│   ├── kalman.py               # Extended Kalman Filter (continuous trajectory smoothing)
│   ├── particle.py             # Particle Filter (dead-reckoning for transponder-dark assets)
│   └── anomaly.py              # ST-DBSCAN Spatio-temporal anomaly detection (airlift surges)
│
├── simulation/                 # 4D Forward Simulation Engine
│   ├── __init__.py
│   ├── world_state.py          # State snapshot at time t (T-30d to T+14d)
│   ├── monte_carlo.py          # Vectorized Monte Carlo runner (uncertainty bands)
│   └── branches.py             # Branching scenarios (Base, Escalation, De-escalation)
│
├── humanitarian/               # Civilian Protection Horizon
│   ├── __init__.py
│   ├── corridors.py            # Evacuation bottleneck and bridge destruction risk
│   └── supply_chain.py         # Hospital medical/fuel exhaustion projections
│
└── ingestion/                  # Event & Signal Baselines
    ├── __init__.py
    ├── acled.py                # ACLED political violence dataset (training ground truth)
    ├── gdelt.py                # GDELT real-time news Goldstein conflict scores
    └── polymarket.py           # Geopolitical prediction market odds (Bayesian priors)
```

---

## Mathematical Formulations

### 1. Multivariate Hawkes Point Process (Escalation Cascades)
Models the self-exciting, retaliatory nature of conflict where an attack in Sector $m$ triggers follow-up strikes in Sector $n$:
$$\lambda_m(t) = \mu_m + \sum_{n} \sum_{t_i < t} \alpha_{mn} \cdot e^{-\beta_{mn}(t - t_i)}$$
* $\mu_m$: Baseline tension rate of the sector.
* $\alpha_{mn}$: Cross-excitation intensity (how strongly an attack by actor $m$ provokes actor $n$).
* $\beta_{mn}$: Decay rate (how fast tensions simmer down over time if no new sparks occur).

### 2. Particle Filters for Transponder-Dark Ships & Flights
When a military cargo plane or vessel disables its transponder, Elpis spawns $N = 5,000$ particles representing candidate positions:
$$x_k^i = f(x_{k-1}^i, u_k) + w_k^i$$
* Particles are weighted by maximum engine speed, historical corridor routes, and ocean/wind vectors from weather APIs.
* **Output:** A probabilistic **uncertainty cloud polygon** rendered directly in Cesium.

### 3. Spatio-Temporal Anomaly Detection (Airlift Pre-Pulse)
Applies ST-DBSCAN over OpenSky transponders:
* Identifies clusters of heavy transports (e.g., Il-76, C-17, An-124) arriving at staging airfields within a 72-hour window.
* An anomaly score $> 3\sigma$ triggers an automatic **Logistics Pre-Pulse Alert**.

---

## Core API Endpoints to Implement in `main.py`

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/forecast/escalation?sector={sector_id}&horizon_hours=48` | Returns Hawkes intensity $\lambda(t)$ and probability of retaliatory strikes in the next 48 hours. |
| `GET` | `/api/v1/simulation/timeline?t_offset_hours={offset}&scenario={id}` | Returns simulated entity positions, active risk cones, and hot zones for time $T + \Delta t$. |
| `GET` | `/api/v1/tracking/dark-asset/{id}` | Returns the dead-reckoning probability cloud for a vessel or aircraft that went dark. |
| `GET` | `/api/v1/humanitarian/corridors?region={id}` | Returns risk scores for civilian evacuation corridors and highway bottlenecks. |

---

## Implementation Roadmap (Step-by-Step)

### Phase 1: Kinematic Tracking & Smoothing (`math_models/kalman.py`)
1. Implement a 6-state Extended Kalman Filter (Position $[x, y, z]$, Velocity $[\dot{x}, \dot{y}, \dot{z}]$) in ECEF coordinates.
2. Smooth incoming noisy ADS-B and AIS GPS reports into continuous, jitter-free flight vectors.

### Phase 2: Historical Conflict Ingestion (`ingestion/acled.py`)
1. Ingest historical conflict event data (e.g., from ACLED or GDELT).
2. Group incidents into spatial bins (using H3 hexagons) and timestamps.

### Phase 3: Hawkes Process Calibration (`math_models/hawkes.py`)
1. Fit the Hawkes kernel parameters ($\mu, \alpha, \beta$) via Maximum Likelihood Estimation (MLE) using historical skirmish sequences.
2. Expose the forward intensity function to calculate 24h, 48h, and 7-day escalation probabilities.

### Phase 4: Forward Simulation & Timeline Dispatcher (`simulation/world_state.py`)
1. Build the world-state generator that takes the current map state at $T_0$, applies the Hawkes probabilities and kinematic vectors, and outputs snapshot arrays for $T+1\text{h}, T+6\text{h}, T+24\text{h}, T+7\text{d}$.
2. Connect to the FastAPI route handler to feed the Next.js 4D time scrubber.

---

## Running the Service
```bash
# Inside services/elpis
uv run uvicorn main:app --reload --port 8002
```
Interactive Swagger docs: `http://localhost:8002/docs`
