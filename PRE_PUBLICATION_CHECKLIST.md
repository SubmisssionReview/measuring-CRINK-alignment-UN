# Pre-Publication Verification Checklist

**Before pushing to GitHub and uploading to Dataverse, verify:**

---

## ✅ Code Quality

- [ ] All notebooks run without errors
  - Notebook 1: 01_topic_distribution.ipynb
  - Notebook 2: 02_alignment_metrics.ipynb

- [ ] All Python modules import correctly
  ```python
  from src.data_processing import VotingDataLoader, CRINKAnalyzer
  from src.alignment_metrics import AlignmentMetrics
  from src.visualization import AlignmentPlots
  ```

- [ ] No print statements left in (except intentional output)

- [ ] No hard-coded paths in any file
  ```
  ✗ DON'T: "C:\Users\Lucian\OneDrive\data.csv"
  ✓ DO: Path("data") / "processed" / "data.csv"
  ```

- [ ] All imports are available in requirements.txt

- [ ] No API keys or secrets in any file
  - Check all .py files for OPEN_AI_API
  - Check all .ipynb files for API keys
  - Verify .env is in .gitignore

---

## ✅ Documentation

- [ ] README.md is complete and clear
- [ ] QUICK_START.md is helpful and accurate
- [ ] docs/methodology.md explains approach
- [ ] docs/data_dictionary.md covers all variables
- [ ] docs/troubleshooting.md addresses common issues
- [ ] CITATION.cff has correct metadata
- [ ] LICENSE file present (MIT)
- [ ] GITHUB-SETUP.md has clear instructions
- [ ] PROJECT_COMPLETION_REPORT.md documents deliverables

---

## ✅ Repository Structure

- [ ] Directory structure matches spec:
  ```
  notebooks/
  src/
  docs/
  data/
  results/
  ```

- [ ] No unnecessary files
  - [ ] No .DS_Store (macOS)
  - [ ] No __pycache__
  - [ ] No .pyc files
  - [ ] No Jupyter checkpoint folders
  - [ ] No .env file (only .env.example)

- [ ] .gitignore is comprehensive
  - [ ] Excludes data files
  - [ ] Excludes .env
  - [ ] Excludes outputs
  - [ ] Excludes cache

---

## ✅ Data Files

- [ ] Data files NOT included in repository
  - [ ] No CSV files committed
  - [ ] Users must download from Dataverse
  - [ ] data/processed/ directory exists but is empty

- [ ] .gitkeep files present in needed directories
  - [ ] data/processed/.gitkeep
  - [ ] data/mappings/.gitkeep
  - [ ] results/.gitkeep

---

## ✅ Notebooks

**Notebook 1: 01_topic_distribution.ipynb**
- [ ] Section 1: Configuration complete with comments
- [ ] Section 2: Data loading with error handling
- [ ] Section 3: CRINK voting analysis
- [ ] Section 4: Visualizations with proper labels
- [ ] Section 5: Tables with exports
- [ ] Section 6: Summary statistics
- [ ] All figures save to results/
- [ ] All tables export to results/
- [ ] Cell 1: Imports only (no execution issues)
- [ ] Cell 2-3: Configuration with help text
- [ ] Cell 4-5: Data loading and cleaning
- [ ] Cell 6-7: CRINK calculation
- [ ] Cell 8-10: Figures and tables
- [ ] Cell 11-13: Summary reports

**Notebook 2: 02_alignment_metrics.ipynb**
- [ ] Similar structure as Notebook 1
- [ ] Advanced metrics section
- [ ] Topic analysis (works with/without mappings)
- [ ] Western democracies comparison
- [ ] All figures and tables export correctly

---

## ✅ Python Modules

**src/data_processing.py**
- [ ] VotingDataLoader class present
- [ ] CRINKAnalyzer class present
- [ ] All methods have docstrings
- [ ] Type hints on all functions
- [ ] Error handling for missing files
- [ ] Handles missing data gracefully

**src/alignment_metrics.py**
- [ ] 4+ metric classes present
- [ ] All formulas documented
- [ ] Examples in docstrings
- [ ] Type hints throughout
- [ ] Proper error handling

**src/visualization.py**
- [ ] PlotConfig class for styling
- [ ] AlignmentPlots with multiple chart types
- [ ] DyadicPlots for pairwise analysis
- [ ] PublicationFigures for export
- [ ] DPI and size configuration
- [ ] Black/white and color modes

**src/__init__.py**
- [ ] Module docstring present
- [ ] All classes exported
- [ ] Version number (__version__)
- [ ] Author attribution

---

## ✅ Configuration Files

**requirements.txt**
- [ ] All packages pinned to versions
- [ ] pandas >= 1.5.0
- [ ] numpy >= 1.23.0
- [ ] matplotlib >= 3.7.0
- [ ] jupyter
- [ ] ipython
- [ ] hdbscan (if using clustering)
- [ ] openai (for API access)
- [ ] No duplicate entries

**.gitignore**
- [ ] Includes: .env
- [ ] Includes: *.pyc
- [ ] Includes: __pycache__/
- [ ] Includes: .ipynb_checkpoints/
- [ ] Includes: data/
- [ ] Includes: results/ (except structure)
- [ ] Includes: .DS_Store
- [ ] Includes: .vscode/
- [ ] Includes: venv/

**.env.example**
- [ ] Shows OPEN_AI_API format
- [ ] Clear instructions
- [ ] Safe values (no actual key)

**CITATION.cff**
- [ ] Title matches project
- [ ] Authors correct
- [ ] License is MIT
- [ ] Repository URL correct
- [ ] Version number matches
- [ ] Valid YAML syntax

---

## ✅ File Headers & Comments

**All .py files should have:**
- [ ] Module docstring at top
- [ ] Author/source attribution (if applicable)
- [ ] License notice (implied by repository)

**All notebooks should have:**
- [ ] Title markdown cell
- [ ] Overview section
- [ ] Data source references
- [ ] Expected outputs documented
- [ ] Clear section headers

**All documentation should have:**
- [ ] Clear title
- [ ] Table of contents or structure
- [ ] Examples where applicable
- [ ] Links to related docs

---

## ✅ Testing

**Notebooks:**
- [ ] Notebook 1 runs without errors (fresh kernel)
- [ ] Notebook 2 runs without errors (fresh kernel)
- [ ] All outputs generate correctly
- [ ] Figures save to results/
- [ ] Tables save to results/
- [ ] Summary statistics print correctly

**Modules:**
- [ ] Can import without errors
- [ ] Sample functions work correctly
- [ ] Error handling works
- [ ] Type hints don't cause issues

**Paths:**
- [ ] Relative paths work from notebook directory
- [ ] Results directory created if missing
- [ ] Data directory checked for files
- [ ] No assumption about working directory

---

## ✅ Git Preparation

- [ ] Local git repository initialized
- [ ] All files tracked (git add .)
- [ ] Initial commit created
- [ ] No uncommitted changes

```bash
# Verify git status
git status

# Should show: "On branch main, nothing to commit"
```

---

## ✅ Before GitHub Push

1. [ ] GitHub repository created (empty, no README)
   - Repository name: measuring-CRINK-alignment-UN
   - Owner: LBumeder
   - Visibility: Public
   - Initialize with: Nothing (empty)

2. [ ] Add remote:
   ```bash
   git remote add origin https://github.com/LBumeder/measuring-CRINK-alignment-UN
   git branch -M main
   git push -u origin main
   ```

3. [ ] Verify on GitHub:
   - Repository appears
   - All files present
   - README displays correctly
   - QUICK_START.md visible

---

## ✅ Before Dataverse Upload

1. [ ] Data files prepared
   - UNGA_voting_records_filtered.csv
   - Any topic mapping files
   - Any supplementary data

2. [ ] Metadata prepared
   - Title: "CRINK UN Voting Alignment: UN General Assembly Voting Records and Analysis Code"
   - Authors: [Your names]
   - Description: Overview of project
   - Keywords: UN voting, international relations, voting alignment, CRINK

3. [ ] README for Dataverse
   - How to download and use
   - Link to GitHub repository
   - Citation format
   - Data sources and periods

4. [ ] License selection
   - Data: CC0 or CC-BY (check university requirements)
   - Code: Already MIT on GitHub

---

## ✅ Documentation Review

**README.md should mention:**
- [ ] What this project does
- [ ] Who should use it
- [ ] Quick-start instructions
- [ ] Data requirements
- [ ] Link to QUICK_START.md
- [ ] Link to full documentation
- [ ] How to cite
- [ ] License information

**QUICK_START.md should be:**
- [ ] Less than 5 minutes to read
- [ ] Step-by-step installation
- [ ] Simple example usage
- [ ] Link to full docs
- [ ] Troubleshooting link

**Troubleshooting.md should cover:**
- [ ] Data file not found
- [ ] Import errors
- [ ] Path issues
- [ ] Kernel problems
- [ ] API key issues
- [ ] Memory issues
- [ ] Common errors

---

## ✅ Final Checks

**Run this diagnostic script:**
```python
#!/usr/bin/env python3
import os
from pathlib import Path
import importlib

print("FINAL VERIFICATION")
print("=" * 50)

# Check structure
required_dirs = ['notebooks', 'src', 'docs', 'data', 'results']
for d in required_dirs:
    p = Path(d)
    print(f"{'✓' if p.exists() else '✗'} {d}/")

# Check files
required_files = [
    'README.md', 'requirements.txt', '.gitignore', 
    'CITATION.cff', 'LICENSE', 'QUICK_START.md'
]
for f in required_files:
    p = Path(f)
    print(f"{'✓' if p.exists() else '✗'} {f}")

# Check notebooks
notebooks = list(Path('notebooks').glob('*.ipynb'))
print(f"\nNotebooks: {len(notebooks)} found")
for nb in notebooks:
    print(f"  ✓ {nb.name}")

# Check modules
modules = ['data_processing.py', 'alignment_metrics.py', 'visualization.py']
print(f"\nModules in src/:")
for mod in modules:
    p = Path('src') / mod
    print(f"  {'✓' if p.exists() else '✗'} {mod}")

# Check imports
print("\nImport tests:")
try:
    from src.data_processing import VotingDataLoader, CRINKAnalyzer
    print("  ✓ data_processing imports")
except ImportError as e:
    print(f"  ✗ data_processing: {e}")

try:
    from src.alignment_metrics import AlignmentMetrics
    print("  ✓ alignment_metrics imports")
except ImportError as e:
    print(f"  ✗ alignment_metrics: {e}")

try:
    from src.visualization import PlotConfig
    print("  ✓ visualization imports")
except ImportError as e:
    print(f"  ✗ visualization: {e}")

print("\n" + "=" * 50)
print("Verification complete!")
```

---

## ✅ Git Final Checks

```bash
# Verify git is clean
git status

# Should output:
# On branch main
# nothing to commit, working tree clean

# Verify remotes
git remote -v
# Should show origin pointing to GitHub repo

# Verify commit log
git log --oneline | head -5
# Should show initial commit
```

---

## ✅ Last Minute

**Before pushing, ask:**
- [ ] Have I included API keys anywhere? (Should be NO)
- [ ] Have I hard-coded any paths? (Should be NO)
- [ ] Are all dependencies in requirements.txt? (Should be YES)
- [ ] Do notebooks run fresh? (Should be YES)
- [ ] Is documentation complete? (Should be YES)
- [ ] Is code professional quality? (Should be YES)

---

## 🎯 If All Checks Pass

**You're ready to:**
1. ✅ Push to GitHub
2. ✅ Upload to Harvard Dataverse
3. ✅ Submit with journal article
4. ✅ Share with research community
5. ✅ Enable reproducible research

---

## 📝 Checklist Summary

- **Code Quality:** [  ] Complete
- **Documentation:** [  ] Complete  
- **Repository Structure:** [  ] Complete
- **Data Files:** [  ] Excluded (by design)
- **Configuration:** [  ] Complete
- **Testing:** [  ] Passed
- **Git Ready:** [  ] Prepared
- **GitHub Ready:** [  ] Repository created
- **Dataverse Ready:** [  ] Metadata prepared

---

**When all boxes are checked:** You're ready to publish! ✅🚀

**Next Step:** Follow GITHUB-SETUP.md to push to GitHub
