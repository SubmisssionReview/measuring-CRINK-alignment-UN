# Copilot Instructions for CRINK UN Voting Alignment Analysis

## Project Overview

This is an academic research repository for analyzing UN General Assembly voting patterns of the CRINK bloc (China, Russia, Iran, North Korea). The codebase produces reproducible, publication-ready analysis and visualizations comparing CRINK voting alignment with Western democracies across 1991-2024.

**Key Domain:** Political science / international relations research using UN voting data analysis  
**Core Deliverables:** Two Jupyter notebooks generating 9+ publication figures and statistical tables  
**Architecture:** Modular Python with reusable functions in `src/`, data-driven notebooks, and comprehensive documentation

---

## Architecture & Key Components

### Data Pipeline
- **Input:** UN General Assembly voting CSVs from [UN Digital Library](https://digitallibrary.un.org/)
- **Processing:** Pivot voting records (countries → columns), classify coalition agreements, calculate alignment metrics
- **Output:** Publication figures (PNG/PDF), styled tables (HTML/LaTeX), CSV exports

### Module Structure

**`src/data_processing.py`** - Data loading and normalization
- `VotingDataLoader`: Load CSV files, standardize country names (USSR → RUSSIAN FEDERATION)
- Key method: `load_voting_data()` handles encoding, date conversion, year extraction
- **Convention:** All dates converted to datetime; country names matched exactly against `CRINK_COUNTRIES`/`WESTERN_COUNTRIES` dictionaries

**`src/alignment_metrics.py`** - Statistical calculations
- `AlignmentMetrics`: Core voting similarity measures (Jaccard, voting agreement %, coalition strength)
- `voting_agreement()`: Percentage of identical votes between two countries (handles NaN filtering)
- `coalition_strength()`: How cohesive is a group? (percentage of most common vote)
- **Pattern:** All metrics return numpy.nan for insufficient data (never raise exceptions on small samples)

**`src/visualization.py`** - Plot generation with consistent styling
- Uses `plt.style.use('bw')` for black-and-white publication style
- `FIGURE_SIZE = (14, 5)` and `DPI = 300` are standard across all plots
- Consistent color mapping: CRINK countries have distinct colors, Western countries grouped

### Notebooks

**`notebooks/01_alignment_metrics.ipynb`** (33 cells)
- Overview: Advanced dyadic analysis, topic-level breakdowns, Western comparison, publication figures
- Outputs: Figures 4-9, Tables 4-5
- **Pattern:** Cells 17-24 contain publication figures with dataset switcher (`database='UNGA'` or `'First Committee'`)
- **Key Structure:** 
  - Cells 1-9: Preliminary setup
  - Cells 10-16: China/US-centric dyadic alignment tables with HTML/LaTeX export
  - Cells 17-24: Publication figures (Figure 2, dyad plot, coalition bar chart, anti-US voting)

**`notebooks/02_topic_distribution.ipynb`** (13 cells)
- Overview: Time series of coalition voting, group cohesion trends, UN majority alignment
- Outputs: Figures 1-3, Tables 2-3
- **Pattern:** Each cell is self-contained; later cells depend on earlier dataframes; uses global `CRINK_COUNTRIES`, `WESTERN_COUNTRIES` dicts

---

## Critical Workflows & Commands

### Setup
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Unix

pip install -r requirements.txt
```

### Data Preparation
Place raw CSVs in `data/processed/`:
- `UNGA_voting_records.csv` (893,587 rows, contains 1991-2024)
- `First_Committee_voting_records.csv` (3,300 rows, contains 2003-2024)

**Encoding:** UNGA uses UTF-8; First Committee uses cp1252 (handle in loader)

### Running Analysis
1. **Full Reproducibility:** Execute notebooks top-to-bottom in sequence
2. **Isolated Testing:** Use `test_run.py` (standalone script using only repo files, no hard-coded paths)
3. **Fresh Environment Validation:** Create `.venv_test` for clean dependency check

### Output Validation
- All plots save to `results/` with timestamp: `figure_NAME_DATASET_YYYY-MM-DD_HH-MM-SS.png`
- Tables export to both HTML (browser-ready) and LaTeX (publication-ready)
- Verification metric: UNGA China alignment should be ~76% (±9pp variation acceptable)

---

## Research Conventions & Patterns

### Country Group Definitions
**Always use these exact names:**
```python
CRINK_COUNTRIES = {
    'CHINA': 'CHN',
    'RUSSIAN FEDERATION': 'RUS',  # NOT 'USSR'
    'IRAN (ISLAMIC REPUBLIC OF)': 'IRN',
    "DEMOCRATIC PEOPLE'S REPUBLIC OF KOREA": 'PRK'
}

WESTERN_COUNTRIES = {
    'UNITED STATES': 'USA',
    'GERMANY': 'GER',
    'FRANCE': 'FRA',
    'UNITED KINGDOM': 'UK'
}
```

### Alignment Metrics Definition
- **Coalition:** 2+ CRINK countries voting identically on a resolution
  - Types: 2-way (2 countries), 3-way (3 countries), 4-way (unanimous)
  - Minimum threshold: Must have agreement_count >= 2 to count
- **Group Vote:** Mode (most common vote) of CRINK countries [Y/N/A]
- **Majority Alignment:** Group vote matches UN majority (Y/N/A)
- **Anti-US:** Unanimous CRINK (4-way) voting against US position
- **Jaccard Similarity:** len(intersection) / len(union) of voting sets

### Time Period Filtering
- **UNGA Analysis:** 1991-2024 (post-Cold War baseline)
- **First Committee:** 2003-2024 (specialized disarmament committee)
- Rationale: 1991 marks Soviet → Russian Federation transition; First Committee data begins 2003

### Data Handling Quirks
1. **Encoding:** UNGA is UTF-8; First Committee is cp1252 → standardize in loader
2. **Missing Votes:** NaN (non-voting) excluded from agreement calculations
3. **Small Samples:** Coalition_strength() and voting_agreement() return np.nan if < 2 data points
4. **USSR Standardization:** Automatically replace 'USSR' with 'RUSSIAN FEDERATION' during load

---

## Integration Points & Dependencies

### External Data (Not in Repo)
- **UNGA Voting Records:** [UN Digital Library](https://digitallibrary.un.org/record/4060887?ln=en)
- **First Committee Data:** Manually collected from UN.org (see metadata.json for versions)
- **Dataverse Publication:** Results will be published on [Harvard Dataverse](https://dataverse.harvard.edu/)

### External Libraries
- **pandas:** Data manipulation, pivot tables, CSV I/O
- **matplotlib/seaborn:** Publication-quality plots with 'bw' style
- **numpy:** Numerical operations (Jaccard, percentages)
- **scikit-learn:** (Optional) For clustering if topic analysis added
- **openai:** (Setup Ready) For LLM-based topic consolidation (api key in .env)

### Configuration
- No config files currently used; all settings in notebook cells
- `.env.example` template provided for future API keys
- Paths: All relative to repo root (using `Path.cwd().parent`)

---

## Common Patterns in Notebooks

### Setup Pattern (Cells 1-2)
```python
# Cell 1: Import all libraries at once
import pandas, numpy, matplotlib, seaborn, etc.

# Cell 2: Define constants (CRINK_COUNTRIES, WESTERN_COUNTRIES, paths)
notebook_dir = Path.cwd()
repo_root = notebook_dir.parent
data_dir = repo_root / "data" / "processed"
```

### Data Loading Pattern (Cells 3-4)
```python
# Cell 3: Load CSV file with proper error handling
df = pd.read_csv(csv_path, encoding='utf-8')
if not csv_path.exists():
    raise FileNotFoundError(f"Data file not found: {csv_path}")

# Cell 4: Clean data
df['ms_name'] = df['ms_name'].replace({'USSR': 'RUSSIAN FEDERATION'})
df['date'] = pd.to_datetime(df['date'], errors='coerce')
vote_pivot = df.pivot_table(index=['undl_id','date'], columns='ms_name', values='ms_vote')
```

### Analysis Pattern (Cells 5-N)
```python
# Group votes by CRINK countries
crink_votes = vote_pivot[CRINK_COUNTRIES.keys()].values
agreement_count = (crink_votes == crink_votes[0]).sum()  # Count unanimous votes

# Calculate metrics
alignment_pct = (votes_with_us / total_votes) * 100

# Time series: Group by year and plot
yearly = df.groupby('year').apply(metric_function)
```

### Visualization Pattern
```python
plt.style.use('bw')  # Always use black & white
fig, ax = plt.subplots(figsize=(14, 5), dpi=300)
ax.plot(years, alignment, linewidth=2, marker='o')
ax.set_ylabel('Alignment (%)', fontsize=12)
# Export: plt.savefig(f'results/figure_{name}_{DATASET}_{timestamp}.png')
```

### Export Pattern (Tables)
```python
# HTML export
html_table = styled_table.to_html()
with open(f'results/table_{name}.html', 'w') as f:
    f.write(html_table)

# LaTeX export
latex_table = df.to_latex(index=False, escape=False)
with open(f'results/table_{name}.tex', 'w') as f:
    f.write(latex_table)
```

---

## Documentation References

- **Methodology:** [docs/methodology.md](../docs/methodology.md) - Full analytical approach, country groups rationale, metric definitions
- **Data Dictionary:** [docs/data_dictionary.md](../docs/data_dictionary.md) - All 20+ variables, ranges, missing data codes
- **Troubleshooting:** [docs/troubleshooting.md](../docs/troubleshooting.md) - 10+ common issues with solutions
- **Setup Guide:** [QUICK_START.md](../QUICK_START.md) - 10-minute environment setup
- **Publication Status:** [PROJECT_COMPLETION_REPORT.md](../PROJECT_COMPLETION_REPORT.md) - Complete inventory of deliverables

---

## Key Success Criteria for AI Agents

✅ **Reproducibility First:** Any new analysis must use only data/code in this repo (no external APIs except OpenAI if configured)  
✅ **Exact Country Names:** Match CRINK_COUNTRIES and WESTERN_COUNTRIES dictionaries exactly  
✅ **Publication Ready:** All plots must use 'bw' style, (14,5) size, 300 DPI  
✅ **Test in Fresh Env:** Validate in `.venv_test` to confirm no missing imports  
✅ **Preserve Notebooks:** Keep both notebooks as authoritative sources; refactor to `src/` only if >100 lines  
✅ **Document Thoroughly:** Any new module needs docstrings with parameter/return types and examples

---

## Quick Reference: File Locations

| Purpose | Location | Key Files |
|---------|----------|-----------|
| Raw Data (not in repo) | `data/raw/` | `UNGA_voting_records.csv`, `First_Committee_voting_records.csv` |
| Processed Data | `data/processed/` | Cleaned CSVs, ready for analysis |
| Analysis Code | `src/` | `data_processing.py`, `alignment_metrics.py`, `visualization.py` |
| Interactive Analysis | `notebooks/` | `01_alignment_metrics.ipynb`, `02_topic_distribution.ipynb` |
| Outputs | `results/` | PNG figures, HTML/LaTeX tables, CSV exports |
| Docs | `docs/` | `methodology.md`, `data_dictionary.md`, `troubleshooting.md` |
