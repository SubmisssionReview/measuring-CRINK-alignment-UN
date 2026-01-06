# Troubleshooting Guide

## Common Issues and Solutions

### 1. Data File Not Found

**Error:**
```
FileNotFoundError: Data file not found: data/processed/UNGA_voting_records_filtered.csv
```

**Causes:**
- Data files not downloaded from Harvard Dataverse
- Files placed in wrong directory
- File name doesn't match exactly

**Solutions:**

1. **Download data from Harvard Dataverse:**
   - Visit the CRINK UN Voting Alignment dataverse entry
   - Download all CSV files in `data/` folder
   - Extract to `data/processed/` directory

2. **Verify file location:**
   ```bash
   # Check that files exist
   ls -la data/processed/
   
   # Should show:
   # UNGA_voting_records_filtered.csv
   # ODA_data_for_analysis.csv (if available)
   # etc.
   ```

3. **Check file names exactly:**
   - File names are case-sensitive on Linux/Mac
   - Spaces in names are preserved
   - Match the exact name from dataverse

---

### 2. Python Package Import Errors

**Error:**
```
ModuleNotFoundError: No module named 'pandas'
```

**Solutions:**

1. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Check Python environment:**
   ```bash
   python --version  # Should be 3.9+
   which python      # Verify correct interpreter
   ```

3. **Use virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **For Jupyter notebooks:**
   ```bash
   # Ensure Jupyter can see the environment
   pip install ipykernel
   python -m ipykernel install --user --name crink --display-name "Python (CRINK)"
   ```

---

### 3. Jupyter Notebook Kernel Issues

**Error:**
```
ModuleNotFoundError when running notebook cells
```

**Solutions:**

1. **Verify kernel:**
   - Top right of notebook shows kernel name
   - Click to change kernel if needed
   - Select the environment where requirements are installed

2. **Reinstall kernel connection:**
   ```bash
   python -m ipykernel install --user --name crink
   ```

3. **Test imports in notebook:**
   ```python
   import sys
   print(sys.executable)  # Check which Python is running
   import pandas as pd
   print(pd.__version__)
   ```

---

### 4. OpenAI API Key Errors

**Error:**
```
AuthenticationError: Invalid API key provided
```

**Causes:**
- API key not set as environment variable
- API key is invalid or expired
- OpenAI account has no API credits

**Solutions:**

1. **Set environment variable:**
   ```bash
   # On Linux/Mac
   export OPEN_AI_API="your-api-key-here"
   
   # On Windows PowerShell
   $env:OPEN_AI_API = "your-api-key-here"
   
   # On Windows CMD
   set OPEN_AI_API=your-api-key-here
   ```

2. **Verify API key is set:**
   ```python
   import os
   print(os.environ.get('OPEN_AI_API'))  # Should show your key
   ```

3. **Create .env file (for local development only):**
   - Copy `.env.example` to `.env`
   - Edit `.env` with your actual API key
   - `.env` is in `.gitignore` - won't be committed

4. **Check OpenAI account:**
   - Login to https://platform.openai.com/account/billing/overview
   - Verify API key is valid
   - Check usage and remaining credits

---

### 5. Path/Directory Issues

**Error:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'C:\\Users\\...'
```

**Causes:**
- Hard-coded absolute paths
- Directory doesn't exist
- Wrong working directory in notebook

**Solutions:**

1. **Use relative paths (CORRECT):**
   ```python
   from pathlib import Path
   data_dir = Path.cwd().parent / "data" / "processed"  # Relative
   ```

2. **Never use hard-coded paths (WRONG):**
   ```python
   # Don't do this:
   df = pd.read_csv("C:\\Users\\Lucian\\OneDrive - Tulane...\\data.csv")
   ```

3. **Check working directory in notebook:**
   ```python
   import os
   print(os.getcwd())  # Should show notebook directory or repo root
   ```

4. **Create directories if missing:**
   ```python
   results_dir = Path("results")
   results_dir.mkdir(parents=True, exist_ok=True)
   ```

---

### 6. Pivot Table Issues

**Error:**
```
KeyError: 'undl_id' or 'ms_name' not found in pivot
```

**Causes:**
- Column names different in your CSV
- Data format different than expected
- Typo in column name

**Solutions:**

1. **Check CSV structure:**
   ```python
   df = pd.read_csv("data/processed/your_file.csv")
   print(df.columns)  # List all columns
   print(df.head())   # Show first few rows
   ```

2. **Map column names if different:**
   ```python
   df = df.rename(columns={
       'actual_col_name': 'expected_col_name',
       'country': 'ms_name'
   })
   ```

3. **Handle missing columns:**
   ```python
   if 'undl_id' not in df.columns:
       print("Warning: undl_id column not found")
       df['undl_id'] = df.index  # Create from index
   ```

---

### 7. Memory Issues with Large Data

**Error:**
```
MemoryError: Unable to allocate X.XX GiB
```

**Causes:**
- Large pivot tables in memory
- Creating multiple copies of dataframe
- Insufficient system RAM

**Solutions:**

1. **Process in chunks:**
   ```python
   # Instead of loading all at once:
   for chunk in pd.read_csv(filepath, chunksize=10000):
       # Process chunk
   ```

2. **Delete unnecessary columns:**
   ```python
   df = df[['undl_id', 'ms_name', 'ms_vote', 'date']]
   ```

3. **Use efficient dtypes:**
   ```python
   df['year'] = df['year'].astype('int16')  # Instead of int64
   df['ms_vote'] = df['ms_vote'].astype('category')
   ```

4. **Increase available memory:**
   - Close other applications
   - Restart Jupyter kernel
   - Consider upgrading system RAM

---

### 8. Figure Saving Issues

**Error:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'results/figure.png'
```

**Solutions:**

```python
from pathlib import Path

results_dir = Path("results")
results_dir.mkdir(parents=True, exist_ok=True)  # Create if missing

# Save figure
plt.savefig(results_dir / 'figure_01.png', dpi=300, bbox_inches='tight')
```

---

### 9. Data Type Mismatches

**Error:**
```
TypeError: '>=' not supported between 'str' and 'int'
```

**Causes:**
- Year column is string instead of integer
- Vote column has unexpected values
- Mixed data types in column

**Solutions:**

```python
# Convert to correct type
df['year'] = pd.to_numeric(df['year'], errors='coerce')
df['ms_vote'] = df['ms_vote'].astype('str')

# Check for invalid values
print(df[df['year'].isna()])  # Find conversion failures
print(df['ms_vote'].unique())  # Check what values exist
```

---

### 10. Matplotlib Display Issues

**Error:**
```
No module named 'matplotlib' or 
ImportError: cannot import name '_path'
```

**Solutions:**

1. **Install matplotlib:**
   ```bash
   pip install matplotlib
   ```

2. **In Jupyter, enable inline display:**
   ```python
   %matplotlib inline
   ```

3. **Check backend:**
   ```python
   import matplotlib
   print(matplotlib.get_backend())
   ```

---

## Performance Tips

### Speed Up Data Loading

```python
# Use efficient reading
df = pd.read_csv(filepath, 
                  dtype={'year': 'int16', 'ms_vote': 'category'},
                  usecols=['undl_id', 'ms_name', 'ms_vote', 'date', 'year'])
```

### Speed Up Pivot Operations

```python
# Subset before pivoting
df_subset = df[['undl_id', 'date', 'ms_name', 'ms_vote']]
pivot = df_subset.pivot_table(index=['undl_id', 'date'], 
                               columns='ms_name',
                               values='ms_vote')
```

### Monitor Memory Usage

```python
import psutil
process = psutil.Process()
print(f"Memory usage: {process.memory_info().rss / 1024 / 1024:.1f} MB")
```

---

## Getting Help

1. **Check GitHub Issues:** Search existing issues for your problem
2. **Review Notebook Comments:** Each notebook cell has explanatory text
3. **Read Documentation:** Check `docs/` folder for detailed information
4. **Run Diagnostics:**
   ```python
   import sys
   print(f"Python: {sys.version}")
   import pandas
   print(f"Pandas: {pandas.__version__}")
   ```

---

## Testing Your Setup

Run this Python script to verify everything is configured correctly:

```python
#!/usr/bin/env python3
"""Test CRINK UN Voting Analysis setup."""

import sys
from pathlib import Path

print("=" * 50)
print("SETUP DIAGNOSTIC TEST")
print("=" * 50)

# Check Python version
print(f"\n✓ Python version: {sys.version}")
if sys.version_info < (3, 9):
    print("  ⚠ WARNING: Python 3.9+ recommended")

# Check required packages
packages = {
    'pandas': 'data manipulation',
    'numpy': 'numerical computation',
    'matplotlib': 'plotting',
    'seaborn': 'statistical visualization',
    'jupyter': 'interactive notebooks'
}

print("\nChecking packages:")
for pkg, desc in packages.items():
    try:
        mod = __import__(pkg)
        version = getattr(mod, '__version__', 'unknown')
        print(f"  ✓ {pkg} ({version}) - {desc}")
    except ImportError:
        print(f"  ✗ {pkg} - MISSING - {desc}")

# Check directories
print("\nChecking directories:")
dirs = ['data/processed', 'results', 'docs', 'notebooks', 'src']
for d in dirs:
    path = Path(d)
    status = "✓" if path.exists() else "✗"
    print(f"  {status} {d}")

# Check API key
import os
api_key = os.environ.get('OPEN_AI_API')
if api_key:
    key_preview = api_key[:4] + "..." + api_key[-4:]
    print(f"\n✓ OpenAI API key found: {key_preview}")
else:
    print("\n⚠ OpenAI API key not set (OPEN_AI_API environment variable)")

print("\n" + "=" * 50)
print("Diagnostic complete!")
print("=" * 50)
```

Save as `test_setup.py` and run:
```bash
python test_setup.py
```

---

## Still Having Issues?

1. **Document the error:** Copy full error message and traceback
2. **Note your environment:** Python version, OS, key packages
3. **Create minimal reproducible example:** Code that shows the problem
4. **Open GitHub issue:** Include all above information
