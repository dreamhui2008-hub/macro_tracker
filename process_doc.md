# 📊 Macro Tracker

A Python dashboard that pulls publicly available macroeconomic indicators from FRED and other sources, and displays current values + recent trends on a live public web interface.

---

## What It Does

- Fetches macro indicators (US, EU, Canada) via free public APIs
- Stores and structures data using pandas
- Visualizes trends with interactive charts
- Deploys as a free public dashboard on Streamlit Community Cloud

---

## Project Phases

### Phase 1 — Local Script (MVP)
- [ ] Set up Python environment (`venv`, `requirements.txt`)
- [ ] Register for free [FRED API key](https://fred.stlouisfed.org/docs/api/api_key.html)
- [ ] Pull one indicator (e.g. US 10Y Yield) via `fredapi`
- [ ] Expand to full indicator list
- [ ] Store data in a pandas DataFrame
- [ ] Print clean output to terminal

**Deliverable:** Script that runs locally and prints a table of indicators with latest values

---

### Phase 2 — Visualization
- [ ] Add matplotlib / plotly charts per indicator
- [ ] Configurable time window (e.g. 1Y, 5Y)
- [ ] Summary view showing all indicators at a glance

**Deliverable:** Local script that produces and saves charts as images

---

### Phase 3 — Dashboard
- [ ] Rebuild as a Streamlit app
- [ ] Interactive controls (date range picker, indicator selector)
- [ ] Deploy to [Streamlit Community Cloud](https://streamlit.io/cloud) (free, public URL)

**Deliverable:** Live public website anyone can visit

---

### Phase 4 — Expand Coverage
- [ ] Add EU indicators (ECB, Eurostat)
- [ ] Add Canada indicators (Bank of Canada, StatCan)
- [ ] Add data freshness labels (last updated timestamp per indicator)

---

## Indicator List

### 🇺🇸 United States (Phase 1–3)
| Indicator | Source | FRED Series ID |
|---|---|---|
| ISM Manufacturing PMI | ISM / FRED | `MANEMP` |
| Michigan Consumer Sentiment | U of Michigan / FRED | `UMCSENT` |
| ADP Employment | ADP / FRED | `ADPWNUSNERSA` |
| US 10Y Treasury Yield | FRED | `DGS10` |
| SOFR | NY Fed / FRED | `SOFR` |
| CPI (All Items) | BLS / FRED | `CPIAUCSL` |
| Core PCE | BEA / FRED | `PCEPILFE` |

### 🇪🇺 EU & 🇨🇦 Canada (Phase 4)
| Indicator | Source |
|---|---|
| ECB Deposit Rate | ECB |
| Eurozone CPI | Eurostat |
| Canada CPI | StatCan |
| Bank of Canada Policy Rate | BoC |

---

## Tech Stack

| Layer | Tool |
|---|---|
| Language | Python 3.x |
| Data fetching | `fredapi`, `requests` |
| Data manipulation | `pandas` |
| Visualization | `plotly` |
| Dashboard | `streamlit` |
| Hosting | Streamlit Community Cloud |
| Version control | GitHub |

---

## Getting Started

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/macro-tracker.git
cd macro-tracker

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Add your FRED API key
cp .env.example .env
# Edit .env and paste your key

# Run the script
python main.py
```

---

## Environment Variables

Create a `.env` file in the project root:

```
FRED_API_KEY=your_key_here
```

> Get a free key at [fred.stlouisfed.org](https://fred.stlouisfed.org/docs/api/api_key.html)

---

## Project Structure (target)

```
macro-tracker/
├── main.py              # Entry point
├── fetch.py             # API calls and data fetching
├── process.py           # pandas transformations
├── visualize.py         # Chart generation
├── app.py               # Streamlit dashboard
├── requirements.txt
├── .env.example
└── README.md
```

---

## Status

🟡 **Phase 1 in progress**

---

## License

MIT