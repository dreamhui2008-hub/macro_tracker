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
- [x] Set up Python environment (`venv`, `requirements.txt`)
- [x] Register for free [FRED API key](https://fred.stlouisfed.org/docs/api/api_key.html)
- [x] Pull one indicator (e.g. US 10Y Yield) via `fredapi`
- [x] Expand to full indicator list
- [x] Store data in a pandas DataFrame
- [x] Print clean output to terminal

**Deliverable:** Script that runs locally and prints a table of indicators with latest values ✅

---

### Phase 2 — Visualization
- [x] Add plotly charts per indicator
- [x] Summary view showing all indicators at a glance (subplot grid)
- [x] Configurable time window (e.g. 1Y, 5Y)
- [x] Combinatorial overlay (select multiple indicators on one chart)

**Deliverable:** Local script that produces interactive charts in browser

---

### Phase 3 — Dashboard
- [ ] Rebuild as a Streamlit app
- [ ] Interactive controls (date range picker, indicator selector)
- [ ] Combinatorial chart with multiselect
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
| Indicator | Source | Series ID |
|---|---|---|
| US 10Y Treasury Yield | FRED | `DGS10` |
| CPI (All Items) | BLS / FRED | `CPIAUCSL` |
| Core PCE | BEA / FRED | `PCEPILFE` |
| Michigan Consumer Sentiment | U of Michigan / FRED | `UMCSENT` ⚠️ 1 month delay |
| SOFR | NY Fed / FRED | `SOFR` |
| Nonfarm Payrolls | BLS API | `CES0000000001` |

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

# Add your API keys to .env
FRED_API_KEY=your_fred_key
BLS_API_KEY=your_bls_key
```

> FRED key: [fred.stlouisfed.org](https://fred.stlouisfed.org/docs/api/api_key.html)  
> BLS key: [data.bls.gov/registrationEngine](https://data.bls.gov/registrationEngine/)

---

## Project Structure (target)

```
macro-tracker/
├── main.py              # Entry point
├── fetch.py             # API calls and data fetching
├── visualize.py         # Chart generation
├── app.py               # Streamlit dashboard
├── requirements.txt
├── .env
└── README.md
```

---

## Status

🟡 **Phase 3 in progress**

---

## License

MIT