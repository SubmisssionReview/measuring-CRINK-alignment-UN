# Quick Start Guide

**Get results in 10 minutes** | [Full Documentation](docs/)

## Prerequisites (One-time Setup)

### 1. Install Python
- Download Python 3.9 or later from https://www.python.org
- Verify installation: `python --version`

### 2. Install Dependencies
```bash
# From the repository directory
pip install -r requirements.txt
```

### 3. Download Data
1. Visit [Harvard Dataverse - CRINK UN Voting](https://dataverse.harvard.edu)
2. Download all CSV files
3. Place in: `data/processed/`

### 4. Set OpenAI API Key (Optional)
```bash
# Linux/macOS
export OPEN_AI_API="your-api-key-here"

# Windows PowerShell
$env:OPEN_AI_API = "your-api-key-here"

# Or create .env file (copy .env.example and edit)
```

## Running the Notebooks

### Option A: Command Line
```bash
# Start Jupyter
jupyter notebook

# Open notebooks/01_topic_distribution.ipynb
# Click "Run All Cells" or run cells one at a time
```

### Option B: VS Code
1. Open VS Code
2. Install Python extension
3. Open `notebooks/01_topic_distribution.ipynb`
4. Select kernel from top-right dropdown
5. Click "Run All" or run individual cells

## What Each Notebook Does

### Notebook 1: Topic Distribution (5-10 minutes)
**File:** `notebooks/01_topic_distribution.ipynb`

**Generates:**
- 2 publication-quality figures
- 3 CSV tables with statistics
- Summary statistics report

**Key Outputs:**
- `results/figure_01_crink_cohesion.png` - CRINK voting trends
- `results/figure_02_coalition_sizes.png` - Coalition distribution
- `results/crink_dyadic_alignment_[DATE].csv` - Pairwise statistics

**Expected Result:** Reproduces Figures 1-3 from published article

### Notebook 2: Alignment Metrics (5-10 minutes)
**File:** `notebooks/02_alignment_metrics.ipynb`

**Generates:**
- 2 additional publication-quality figures
- 3 detailed statistical tables
- Comparative analysis (CRINK vs Western democracies)

**Key Outputs:**
- `results/figure_04_topic_distribution.png` - Topic analysis
- `results/figure_05_alignment_heatmap.png` - Country comparison
- Multiple CSV tables with detailed statistics

**Expected Result:** Reproduces Figures 4-9 and Tables 4-5 from article

## Customization

### Change Country Groups
Edit cells in **Section 1: Configuration**
```python
CRINK_COUNTRIES = {
    'CHINA': 'CHN',
    'RUSSIAN FEDERATION': 'RUS',
    # Add or remove countries here
}
```

### Change Time Period
```python
UNGA_START_YEAR = 1991      # Change start year
END_YEAR = 2024             # Change end year
```

### Change Dataset
```python
dataset_choice = 'UNGA_voting_records_filtered.csv'  # Change filename
```

### Change Figure Style
```python
PLOT_STYLE = 'bw'          # 'bw' for black/white, 'color' for color
FIGURE_SIZE = (14, 5)      # Change figure dimensions (width, height)
DPI = 300                  # Change resolution
```

## Common Issues

### "Data file not found"
- Verify files are in `data/processed/`
- Check file names match exactly (case-sensitive)
- See [Troubleshooting Guide](docs/troubleshooting.md#1-data-file-not-found)

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "API key error"
- Only needed if modifying to regenerate topic mappings
- Most users can ignore this (pre-computed mappings available)
- See [API Key Setup](docs/troubleshooting.md#4-openai-api-key-errors)

### Jupyter kernel issues
- Select correct kernel from top-right dropdown
- If missing, reinstall: `python -m ipykernel install --user`

**More help:** See [Full Troubleshooting Guide](docs/troubleshooting.md)

## Understanding Results

### Figures Explained

**Figure 1: CRINK Cohesion and UN Alignment**
- Shows percentage of resolutions where all 4 CRINK countries vote together
- Shows percentage aligned with UN majority
- Trend from 1991-2024

**Figure 2: Coalition Size Distribution**
- Shows breakdown of how many CRINK countries vote together
- 2-way: 2 countries voting together
- 3-way: 3 countries voting together
- 4-way: All 4 countries unanimous (strongest alignment)

**Figure 3+: Additional Metrics**
- See data tables for detailed statistics
- CSV exports available for further analysis

### Tables Explained

**Dyadic Alignment Table**
- Shows pairwise voting agreement percentages
- Example: China-Russia agreement = 87.3% (voted identically 87.3% of the time)
- All 6 possible pairs within CRINK

**Topic-Level Statistics**
- For each resolution topic
- Count of resolutions in that topic
- Percentage with 2+ CRINK agreement
- Useful for identifying issue-specific coalitions

**Yearly Trends**
- Year-by-year breakdown
- Total votes analyzed per year
- Coalition size distribution per year
- UN majority alignment trends

## Interpreting CRINK Alignment

**High Alignment (>80%)**
- CRINK countries voting very similarly
- Acting as cohesive voting bloc
- Often on controversial/polarizing issues

**Medium Alignment (50-80%)**
- Countries mostly aligned but some divergence
- Coalition splits on specific issues
- Topic-dependent voting

**Low Alignment (<50%)**
- Countries frequently voting differently
- No clear CRINK position
- Issues with internal disagreement

## Output Files Explained

### PNG Figures
- Publication-quality graphics (300 DPI)
- Black/white or color (configurable)
- Ready for journal submission
- Located in `results/` folder

### CSV Tables
- Statistical summaries
- Timestamped for version tracking
- Can be imported into Excel/Stata/R
- Column headers clearly labeled

### HTML/LaTeX (Advanced)
- When available, automatically formatted
- Ready for paste into academic papers
- Generated by some analyses

## Reproducing Exact Published Results

To get identical figures to those in the published article:

1. **Use exact same parameters** (already configured in notebooks)
2. **Use same data source** (UN Digital Library, 1991-2024)
3. **Run with no modifications** to Section 1 configuration
4. **Check all figures save** to `results/` folder

**If results differ:**
- Check data is complete (no missing files)
- Verify time period matches (1991-2024)
- See troubleshooting guide for help

## Using Code in Your Research

### Import and Reuse Modules
```python
from src.data_processing import VotingDataLoader, CRINKAnalyzer
from src.alignment_metrics import AlignmentMetrics
from src.visualization import AlignmentPlots, PlotConfig

# Load data
loader = VotingDataLoader("data/processed")
df = loader.load_voting_data("UNGA_voting_records_filtered.csv")

# Analyze
analyzer = CRINKAnalyzer(loader.create_vote_pivot(df))
alignment = analyzer.calculate_dyadic_alignment()

# Visualize
config = PlotConfig(style='color')
fig, ax = AlignmentPlots.plot_dyadic_rankings(alignment, config=config)
```

### Adapt for Different Analysis
- Use `CRINKAnalyzer` with different country groups
- Modify country definitions in configuration
- Reuse metrics and visualization functions
- See code documentation for API details

## Next Steps

1. **Run the notebooks** to reproduce figures
2. **Examine the code** to understand methodology
3. **Read documentation** for detailed explanation
4. **Modify parameters** to explore variations
5. **Cite the work** in your research (see README.md)

## Getting Help

**For errors:** Check [docs/troubleshooting.md](docs/troubleshooting.md)

**For methodology:** See [docs/methodology.md](docs/methodology.md)

**For data structure:** See [docs/data_dictionary.md](docs/data_dictionary.md)

**For code:** Review comments in notebooks and source files

## Success Checklist

After running the notebooks, you should have:

- [ ] Both notebooks run without errors
- [ ] Figures saved in `results/` folder
- [ ] CSV files generated with timestamped names
- [ ] Summary statistics printed in notebook output
- [ ] Able to compare figures with published article
- [ ] No missing data files or import errors

✅ If all checks pass, you've successfully reproduced the analysis!

---

**Ready to get started?** Open `notebooks/01_topic_distribution.ipynb` and run it now!

For questions, see the [full documentation](docs/) or [troubleshooting guide](docs/troubleshooting.md).
