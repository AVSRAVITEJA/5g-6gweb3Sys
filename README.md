# DeTrust-RAN 

**DeTrust-RAN** is an AI-powered, blockchain-backed framework for real-time 5G/6G network resource allocation. It combines simulated (or hardware-sourced) network telemetry with a machine-learning decision engine and an on-chain audit trail to intelligently allocate bandwidth slices — while prioritising socially important traffic such as emergency services and rural connectivity.

---

## Table of Contents

1. [What the Project Does](#what-the-project-does)  
2. [System Architecture](#system-architecture)  
3. [Project Structure](#project-structure)  
4. [Module Breakdown](#module-breakdown)  
   - [network/ — Network Simulator](#network----network-simulator)  
   - [ai/ — AI Decision Engines](#ai----ai-decision-engines)  
   - [ml/ — ML Training Pipeline](#ml----ml-training-pipeline)  
   - [blockchain/ — Blockchain Layer](#blockchain----blockchain-layer)  
   - [server/ — ESP32 API Server](#server----esp32-api-server)  
   - [backend/ — Data Ingestion Backend](#backend----data-ingestion-backend)  
   - [dashboard/ — Streamlit Dashboard](#dashboard----streamlit-dashboard)  
   - [frontend/ — Lightweight HTML Frontend](#frontend----lightweight-html-frontend)  
   - [hardware/ — ESP32 Firmware](#hardware----esp32-firmware)  
5. [Data Flow (End-to-End)](#data-flow-end-to-end)  
6. [Network Slice Types](#network-slice-types)  
7. [Traffic Priority System](#traffic-priority-system)  
8. [Installation & Setup](#installation--setup)  
9. [Running the Project](#running-the-project)  
10. [Troubleshooting & Notes](#troubleshooting--notes)  

---

## What the Project Does

Modern 5G and next-generation 6G networks need to serve vastly different types of users simultaneously — from emergency responders who need guaranteed, low-latency connectivity, to rural communities with limited infrastructure, to ordinary consumers streaming video. Deciding how to split limited radio bandwidth between these competing demands in real time — a problem called **network slicing** — is traditionally handled by rigid, pre-programmed rules. DeTrust-RAN replaces those rules with a live AI decision engine, adds a blockchain audit trail so every allocation decision is permanently recorded and verifiable, and ties it all to a real IoT device (ESP32) that acts as the network sensor at the edge.

In practical terms: a sensor (real or simulated) continuously reports network conditions such as latency, packet loss, congestion, and user count. This data is sent over HTTP to a central Flask server. An ML model (Random Forest classifier, trained on synthetic network data) reads those conditions and assigns one of three bandwidth tiers — **High Priority (80 %)**, **Medium Priority (50 %)**, or **Best Effort (30 %)** — to the current slice. The decision, along with a timestamp and traffic context, is then logged to a blockchain (a stub in demo mode; a full Solidity smart contract is included for real deployment). A Streamlit dashboard and a plain HTML/JS page both poll the server every two seconds and display live charts of latency, packet loss, bandwidth decisions, and recent blockchain transaction hashes — giving operators a transparent, real-time view of exactly how and why the network is being managed.

DeTrust-RAN simulates a 5G/6G Radio Access Network (RAN) base station that:

1. **Collects network telemetry** — either from a real ESP32 microcontroller over Wi-Fi or from a software simulator — including latency, packet loss, congestion level, active user count, and traffic type.
2. **Makes AI-driven slicing decisions** — a trained Random Forest classifier (or a rule-based fallback) decides which of three network slice tiers to activate and how much bandwidth (in %) to allocate.
3. **Logs every decision immutably** — each slice allocation is logged on a blockchain (currently in demo mode; a Solidity smart contract is provided for real deployment).
4. **Visualises everything in real time** — a Streamlit dashboard (and a lightweight HTML/JS page) shows live metrics, the AI's decision, and recent blockchain transaction hashes.

The project demonstrates how **edge computing + ML + Web3** can work together at the network layer for trustworthy, transparent, and socially responsible resource allocation.

---

## System Architecture

```
┌─────────────────────┐        ┌──────────────────────────────────────┐
│  ESP32 Firmware     │──WiFi→ │  server/api_server.py  (Flask :5000) │
│  hardware/esp32_node│        │  backend/data_dashboard.py  (:5001)  │
└─────────────────────┘        └───────────────┬──────────────────────┘
         OR                                    │ POST /ingest
┌─────────────────────┐                        ▼
│ backend/state_feeder│──POST→ ┌───────────────────────────────┐
│ (simulated telemetry)│       │  dashboard/realtime_stream.py │
└─────────────────────┘        │  ┌─────────────────────────┐  │
                                │  │  ai/ml_decision_engine  │ │
                                │  └──────────┬──────────────┘ │
                                │             │ decision       │
                                │  ┌──────────▼──────────────┐ │
                                │  │ blockchain/web3_clients │ │
                                │  └──────────┬──────────────┘ │
                                │             │ tx_hash        │
                                └─────────────┼────────────────┘
                                              ▼
                               ┌──────────────────────────────┐
                               │  dashboard/app.py (Streamlit)│
                               │  frontend/ (HTML/JS)         │
                               └──────────────────────────────┘
```

---

## Project Structure

```
5g-6gnetworks/
├── main.py                        # Standalone CLI runner (simulator + AI + blockchain)
├── requirements.txt               # Python dependencies
│
├── network/
│   ├── __init__.py
│   └── simulator.py               # Generates random network state snapshots
│
├── ai/
│   ├── ml_decision_engine.py      # ML-based (+ fallback) slicing decision engine
│   └── rule_decision_engine.py    # Pure rule-based simulator + CSV logger
│
├── ml/
│   ├── generate_dataset.py        # Generates synthetic training CSV (3 000 rows)
│   ├── train_model.py             # Trains RandomForest; saves .pkl files
│   ├── network_dataset.csv        # Generated training data
│   ├── slice_model.pkl            # Trained Random Forest model
│   └── label_encoder.pkl          # LabelEncoder for traffic_type feature
│
├── blockchain/
│   ├── __init__.py
│   ├── web3_clients.py            # BlockchainClient (demo logging)
│   └── contracts/
│       └── networkGovernance.sol  # Solidity smart contract for on-chain logging
│
├── server/
│   ├── __init__.py
│   └── api_server.py              # Flask server (:5000) — receives ESP32 telemetry
│
├── backend/
│   ├── __init__.py
│   ├── data_dashboard.py          # Flask server (:5001) — /ingest + /latest endpoints
│   └── state_feeder.py            # Simulated state pusher (replaces real ESP32)
│
├── dashboard/
│   ├── __init__.py
│   ├── app.py                     # Streamlit real-time dashboard UI
│   ├── realtime_stream.py         # Connects AI engine + blockchain; caches latest decision
│   ├── data_generator.py          # Standalone data + decision generator for testing
│   ├── decision_engine.py         # Simple rule engine used by data_generator
│   ├── esp32_client.py            # HTTP client to fetch data from backend
│   └── blockchain_logger.py       # Stub blockchain logger (returns demo tx hash)
│
├── frontend/
│   ├── index.html                 # Minimal network dashboard HTML page
│   ├── app.js                     # Polls backend /latest every 2 s and updates UI
│   └── style.css                  # Dark-themed card layout styles
│
├── hardware/
│   └── esp32_node/
│       └── esp32_node.ino         # Arduino sketch: connects to Wi-Fi + POSTs telemetry
│
└── data/
    └── simulated_logs.csv         # Output of rule_decision_engine simulation (50 rows)
```

---

## Module Breakdown

### `network/` — Network Simulator

**File:** `network/simulator.py`

`NetworkSimulator.get_state()` generates a random snapshot of the network at a given instant:

| Field | Range / Values | Description |
|---|---|---|
| `timestamp` | UTC ISO string | When the snapshot was taken |
| `latency_ms` | 20 – 150 ms | Simulated round-trip latency |
| `packet_loss` | 0.0 – 5.0 % | Simulated packet loss rate |
| `congestion_level` | 1 – 10 | 1 = light, 10 = severely congested |
| `active_users` | 10 – 500 | Number of concurrent UEs (User Equipments) |
| `traffic_type` | EMERGENCY / RURAL / NORMAL | Type of traffic on this slice |

This module is used by `main.py` when running in standalone mode without a real ESP32.

---

### `ai/` — AI Decision Engines

#### `ai/ml_decision_engine.py` — Primary Engine

`MLDecisionEngine` is the unified inference interface used by the Flask servers, the Streamlit dashboard, and the standalone runner.

**Initialisation:** Tries to load `ai/models/slicing_model.pkl`. If the file is not found, it automatically falls back to rule-based logic — so the system always produces a valid output.

**Inputs (from network state):**

| Feature | Source |
|---|---|
| `latency_ms` | Network state |
| `packet_loss` | Network state |
| `congestion_level` | Network state |
| `active_users` | Network state |
| `traffic_type` | Network state |

**Output decision mapping:**

| Class | `decision` | `bandwidth_allocated` |
|---|---|---|
| 0 | `BEST_EFFORT` | 30 % |
| 1 | `MEDIUM_PRIORITY_SLICE` | 50 % |
| 2 | `HIGH_PRIORITY_SLICE` | 80 % |

**Fallback rule logic (when no model file is found):**
- `traffic_type == EMERGENCY` → `HIGH_PRIORITY_SLICE` (80 %)
- `congestion_level > 7` → `MEDIUM_PRIORITY_SLICE` (50 %)
- Everything else → `BEST_EFFORT` (30 %)

#### `ai/rule_decision_engine.py` — Standalone Simulation + CSV Logger

`run_simulation()` runs 50 iterations of state generation, prints each state to console, and writes all rows to `data/simulated_logs.csv`. Includes four traffic types: `EMERGENCY`, `HEALTHCARE`, `RURAL`, `NORMAL`, with weighted random sampling (EMERGENCY least frequent at 10 %).

Run independently:
```bash
python ai/rule_decision_engine.py
```

---

### `ml/` — ML Training Pipeline

Two scripts that build the Machine Learning model from scratch.

#### Step 1 — Generate Dataset: `ml/generate_dataset.py`

Produces `ml/network_dataset.csv` with 3 000 synthetic rows.  
Features: `latency`, `packet_loss`, `congestion`, `active_users`, `traffic_type`  
Labels (rule-generated): `HIGH` / `MEDIUM` / `LOW`

Label logic:
```
EMERGENCY traffic  → HIGH
congestion > 7     → HIGH
RURAL traffic      → MEDIUM
everything else    → LOW
```

```bash
python ml/generate_dataset.py
```

#### Step 2 — Train Model: `ml/train_model.py`

Trains a `RandomForestClassifier` (100 trees, max depth 10) on the generated dataset.  
Encodes `traffic_type` with `LabelEncoder`.

Saves:
- `ml/slice_model.pkl` — the trained classifier
- `ml/label_encoder.pkl` — the traffic type encoder

```bash
python ml/train_model.py
```

> **Note:** The AI engine (`ai/ml_decision_engine.py`) currently looks for the model at `ai/models/slicing_model.pkl`. After training, copy the `.pkl` files to `ai/models/` for live ML inference.

---

### `blockchain/` — Blockchain Layer

#### `blockchain/web3_clients.py` — BlockchainClient

Currently in **demo mode**: prints decision details to console and returns a hardcoded `0xDEMO_TRANSACTION_HASH`. Ready to be wired to a real Ethereum node (via the `web3` library listed in `requirements.txt`).

#### `blockchain/contracts/networkGovernance.sol` — Solidity Smart Contract

A Solidity 0.8.x contract for on-chain decision logging.

```solidity
struct DecisionLog {
    string decision;      // e.g. "HIGH_PRIORITY_SLICE"
    uint256 bandwidth;    // e.g. 80
    string context;       // traffic type
    uint256 timestamp;    // block.timestamp
}
```

Functions:
- `logDecision(decision, bandwidth, context)` — appends a new log entry
- `getLogsCount()` — returns total number of logged decisions

Deploy on any EVM-compatible chain (Ethereum, Polygon, etc.) and connect `web3_clients.py` to it for production use.

---

### `server/` — ESP32 API Server

**File:** `server/api_server.py`  
**Port:** 5000

A Flask server that acts as the **direct receiver** for the ESP32 firmware.

**Endpoint:** `POST /telemetry`

Accepts JSON:
```json
{
  "latency_ms": 45,
  "packet_loss": 1.2,
  "congestion_level": 5,
  "active_users": 120,
  "traffic_type": "NORMAL"
}
```

Runs the ML decision engine → logs to blockchain → returns:
```json
{
  "slice": "MEDIUM_PRIORITY_SLICE",
  "bandwidth": 50
}
```

```bash
python server/api_server.py
```

---

### `backend/` — Data Ingestion Backend

#### `backend/data_dashboard.py` — Flask Backend for Dashboard
**Port:** 5001

| Endpoint | Method | Description |
|---|---|---|
| `/ingest` | `POST` | Accepts network state, runs AI + blockchain pipeline, caches result |
| `/latest` | `GET` | Returns the most recent AI decision (or a "waiting" status) |

This is the **central hub** that both the Streamlit dashboard and HTML frontend read from.

```bash
python backend/data_dashboard.py
```

#### `backend/state_feeder.py` — Simulated ESP32 Replacement

When no physical ESP32 is available, `state_feeder.py` continuously generates random network state data every 2 seconds and POSTs it to `http://127.0.0.1:5001/ingest` — effectively acting as a software stand-in for the hardware device.

```bash
python backend/state_feeder.py
```

---

### `dashboard/` — Streamlit Dashboard

**File:** `dashboard/app.py`  
**Run with:** `streamlit run dashboard/app.py`

A full real-time monitoring UI built with Streamlit. Every 2 seconds it polls `http://127.0.0.1:5001/latest` and updates the following visualisations:

| Panel | Description |
|---|---|
| Avg Latency (ms) | Running mean of all collected data points |
| Avg Packet Loss (%) | Running mean |
| Active Users | Latest value |
| Bandwidth Allocation Over Time | Line chart of bandwidth decisions |
| Traffic Context Distribution | Bar chart of EMERGENCY / RURAL / NORMAL counts |
| Network Metrics Timeline | Combined line chart: latency, packet loss, congestion |
| Recent Blockchain Logged Decisions | Table showing last 10 tx_hash entries |

**Supporting files:**

| File | Role |
|---|---|
| `realtime_stream.py` | The bridge: receives state → calls ML engine → calls blockchain → caches result |
| `data_generator.py` | Self-contained data + decision generator (for testing the dashboard standalone) |
| `decision_engine.py` | Rule-based slicer used only by `data_generator.py` |
| `esp32_client.py` | HTTP helper to fetch data from the backend (used when integrating with ESP32) |
| `blockchain_logger.py` | Stub that returns a demo transaction hash |

---

### `frontend/` — Lightweight HTML Frontend

A minimal browser-based dashboard that does the same thing as the Streamlit UI but requires no Python.

- **`index.html`** — Card layout showing Latency, Packet Loss, Active Users, and the full latest AI decision JSON
- **`app.js`** — Calls `http://127.0.0.1:5001/latest` every 2 seconds via `fetch()` and updates the DOM
- **`style.css`** — Dark navy theme (`#0f172a` background, `#38bdf8` accent)

Open `frontend/index.html` directly in a browser while the backend is running.

---

### `hardware/` — ESP32 Firmware

**File:** `hardware/esp32_node/esp32_node.ino`  
**Target board:** ESP32 (Arduino-compatible)

The firmware connects to a Wi-Fi network and every 5 seconds POSTs a JSON payload of simulated network metrics to the backend server:

```json
{
  "latency_ms": 63,
  "packet_loss": 1.4,
  "congestion_level": 3,
  "active_users": 127,
  "traffic_type": "NORMAL"
}
```

**Configuration (edit before flashing):**

| Variable | Default | Description |
|---|---|---|
| `ssid` | `"Raviii"` | Wi-Fi network name |
| `password` | `"11080505"` | Wi-Fi password |
| `serverURL` | `http://10.233.22.234:5001/ingest` | Backend IP — **set to your laptop's local IP** |

Flash using the Arduino IDE with the ESP32 board support package installed.

---

## Data Flow (End-to-End)

```
[Telemetry Source]
       │
       │  HTTP POST (JSON with latency, packet_loss, congestion, users, traffic_type)
       ▼
[Flask Backend :5001  /ingest]
       │
       │  calls process_network_state(state)
       ▼
[dashboard/realtime_stream.py]
       │
       ├── MLDecisionEngine.predict(state)
       │       └─ Returns: { decision, bandwidth_allocated, social_context }
       │
       └── BlockchainClient.log_decision(decision)
               └─ Returns: tx_hash (demo: "0xDEMO_TRANSACTION_HASH")
       │
       │  Merges: state + decision + tx_hash → latest_decision (cached globally)
       ▼
[GET /latest]
       │
       ├──▶ Streamlit dashboard (dashboard/app.py) — every 2 s
       └──▶ HTML frontend (frontend/app.js)        — every 2 s
```

---

## Network Slice Types

| Slice | Bandwidth | When Assigned |
|---|---|---|
| `HIGH_PRIORITY_SLICE` | 80 % | Emergency traffic or high congestion |
| `MEDIUM_PRIORITY_SLICE` | 50 % | Rural connectivity or moderate congestion |
| `BEST_EFFORT` | 30 % | Normal background traffic |

---

## Traffic Priority System

The system recognises three traffic classifications and maps them to slices:

| Traffic Type | Priority | Typical Use Case |
|---|---|---|
| `EMERGENCY` | Highest | Ambulance / police / disaster response comms |
| `RURAL` | Medium | Connectivity for underserved / remote areas |
| `NORMAL` | Standard | Regular consumer / enterprise traffic |

This social responsibility layer is a core design principle of DeTrust-RAN.

---

## Installation & Setup

### Prerequisites

- Python 3.9+
- pip
- Arduino IDE (only if using real ESP32 hardware)

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies:**

| Package | Purpose |
|---|---|
| `pandas` | Data handling in ML pipeline and dashboard |
| `numpy` | Numerical operations in ML engine |
| `scikit-learn` | Random Forest model training |
| `matplotlib` | Plotting (available for charts) |
| `web3` | Ethereum blockchain client (ready for production wiring) |
| `joblib` | Model serialisation (`.pkl` files) |
| `streamlit` | Real-time dashboard UI |
| `plotly` | Interactive charting in dashboard |

You will also need `flask` and `flask-cors` for the backend servers (not currently listed in `requirements.txt` — install manually):

```bash
pip install flask flask-cors requests
```

---

## Running the Project

There are two main modes. Choose one depending on whether you have an ESP32.

---

### Mode A — Fully Simulated (No Hardware)

Open **three terminals** in the project root:

**Terminal 1 — Start the backend Flask server:**
```bash
python backend/data_dashboard.py
```
Runs on `http://127.0.0.1:5001`

**Terminal 2 — Start the simulated data feeder:**
```bash
python backend/state_feeder.py
```
Sends random network state to the backend every 2 seconds.

**Terminal 3 — Launch the Streamlit dashboard:**
```bash
streamlit run dashboard/app.py
```
Opens the live dashboard at `http://localhost:8501`

*Optionally, open `frontend/index.html` in your browser for the lightweight view.*

---

### Mode B — With Real ESP32 Hardware

**Step 1.** Flash the firmware:
- Open `hardware/esp32_node/esp32_node.ino` in Arduino IDE
- Update `ssid`, `password`, and `serverURL` (use your laptop's local IP)
- Flash to the ESP32

**Step 2.** Start the backend (Terminal 1):
```bash
python backend/data_dashboard.py
```

**Step 3.** The ESP32 will POST to `/ingest` automatically every 5 seconds.

**Step 4.** Start the dashboard (Terminal 2):
```bash
streamlit run dashboard/app.py
```

---

### Mode C — Standalone CLI (Debug / Demo)

Runs the full loop (simulate → AI decide → blockchain log) in a single terminal with no web server:

```bash
python main.py
```

---

### Regenerate the ML Model (Optional)

If you want to retrain the model from scratch:

```bash
# Step 1: Generate 3000-row synthetic dataset
python ml/generate_dataset.py

# Step 2: Train the RandomForest model
python ml/train_model.py

# Step 3: Copy model to expected location
copy ml\slice_model.pkl ai\models\slicing_model.pkl
```

---

## Troubleshooting & Notes

| Issue | Fix |
|---|---|
| `ML model not found, using rule-based fallback` | The AI engine defaults gracefully. Copy `ml/slice_model.pkl` to `ai/models/slicing_model.pkl` after training. |
| `Backend not reachable` in Streamlit | Start `backend/data_dashboard.py` first. |
| ESP32 not connecting | Check `ssid` / `password` / `serverURL` IP in the `.ino` file. |
| `flask_cors` not found | Run `pip install flask flask-cors` |
| Blockchain logs show `0xDEMO_TRANSACTION_HASH` | Expected in demo mode. For real logging, deploy `networkGovernance.sol` and wire `blockchain/web3_clients.py` to your node. |

---

> **Project Name:** DeTrust-RAN  
> **Domain:** 5G/6G Network Slicing · Edge AI · Blockchain Governance  
> **Stack:** Python · Flask · Streamlit · scikit-learn · Solidity · ESP32 (Arduino)
