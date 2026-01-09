# Measuring CRINK Alignment in the UN

This repository contains python code for measuring the political alignment of China, Russia, Iran, and North Korea (CRINK) in the United Nations voting record. The data can be used to replicate the findings of the accompanying research article "Emerging Bloc or Fragmented Coalition? Voting Behavior of China, Russia, Iran, and North Korea at the UN" (forthcoming 2026). 

## Overview

This research examines the frequency, configuration, and issue-specific contours of CRINK voting alignment using United Nations General Assembly (UNGA) plenary from 1991-2024 and First Committee voting records from 2003-2024. The analysis situates CRINK alignment relative to Western democracies and the UN majority, providing a systematic assessment of whether these four countries constitute a cohesive authoritarian bloc or a fragmented coalition.

## Key Findings

- **Plenary Voting**: Marked consolidation of CRINK collective voting since the early 2000s, rising from ~30-40% to ~60-65% by 2024
- **First Committee**: Substantially lower alignment (~25-35%) without sustained upward trajectory on security/disarmament issues
- **Coalition Structure**: Group-of-four and triadic voting dominate over dyadic alignment; China occupies a central anchoring position
- **Issue-Specific**: Cohesion on outer-space security and cyber governance; fragmentation on humanitarian and arms-control agendas
- **Western Comparison**: Parallel trends of rising intra-group cohesion with declining majority alignment, reflecting broader polarization

## Data Sources

### Primary Data
- **UNGA Plenary Votes**: UN General Assembly voting records (1991-2024) from the [UN Digital Library](https://digitallibrary.un.org/record/4060887?ln=en)
- **First Committee Votes**: UN General Assembly First Committee voting data (2003-2024) on security, disarmament, and arms control issues from the [UNODA Resolutions Database](https://resolutions.unoda.org/)

### Data Availability
Raw UNGA voting records are publicly available from the UN. Processed datasets and First Committee data will be available through [Harvard Dataverse](https://dataverse.harvard.edu/) for reproducibility.

## Repository Structure

```
measuring-CRINK-alignment-UN/
├── README.md                           # This file
├── LICENSE                             # MIT License
├── requirements.txt                    # Python dependencies
├── .gitignore                          # Git ignore patterns
├── .env.example                        # Template for environment variables
│
├── data/
│   ├── raw/                           # Original data files (not in repo)
│   ├── processed/                     # Cleaned/processed datasets
│   ├── mappings/                      # Pre-computed embeddings and topic mappings
│   └── metadata.json                  # Data provenance and versions
│
├── notebooks/
│   ├── 01_alignment_metrics.ipynb     # CRINK alignment metrics (Figure 1-9; Table 3-5)
│   └── 02_generating_topic_analysis.ipynb  # Topic-level voting analysis (Table 2)
│
├── src/
│   ├── __init__.py
│   ├── data_processing.py             # Data loading and cleaning
│   ├── alignment_metrics.py           # Alignment calculation functions
│   └── visualization.py               # Plotting functions
│
├── config/
│   ├── config.yaml                    # Analysis configuration (no secrets)
│   └── .env.example                   # Template for environment variables
│
├── results/
│   └── .gitkeep                       # Output plots and tables
│
└── docs/
    ├── methodology.md                 # Detailed methodology
    ├── data_dictionary.md             # Data column descriptions
    └── troubleshooting.md             # Common issues and solutions
```

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/SubmisssionReview/measuring-CRINK-alignment-UN.git
cd measuring-CRINK-alignment-UN
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API Access

Create a `.env` file in the project root with your OpenAI API key:

```
OPEN_AI_API=your_api_key_here
```

See `.env.example` for the template.

### 4. Download Data

Download the processed datasets from Harvard Dataverse (link to be provided upon publication). Place them in the `data/processed/` directory.

### 5. Run Notebooks

Open and execute the notebooks in order:

```bash
jupyter notebook notebooks/01_alignment_metrics.ipynb
jupyter notebook notebooks/02_topic_distribution.ipynb
```

## Reproducibility

The analysis in this project is reproducable if the following settings are kept stable. 

- **Fixed random seeds** for all stochastic operations
- **Pinned package versions** in `requirements.txt`
- **Documented configurations** with commented values used in published research
- **Topic mapping history** preserved via timestamped JSON files
- **All API calls logged** for transparency

### Environment

- **Python**: 3.9+
- **OpenAI API**: Required for topic mapping (gpt-4o-mini model)
- **Data**: Pre-computed embeddings cached to avoid redundant API calls

## Analysis Configuration

Key parameters (used in published research):

```python
# Topic analysis
EMBEDDING_MODEL = ─text-embedding-3-large─
HDBSCAN_MIN_CLUSTER_SIZE = 10
TARGET_META_TOPICS = 20

# Geographic groups (hard-coded)
CRINK_COUNTRIES = [
    'CHINA',
    'RUSSIAN FEDERATION',
    'IRAN (ISLAMIC REPUBLIC OF)',
    ─DEMOCRATIC PEOPLE'S REPUBLIC OF KOREA─
]

WESTERN_COUNTRIES = [
    'UNITED STATES',
    'GERMANY',
    'FRANCE',
    'UNITED KINGDOM'
]

# Analysis periods (configurable but documented)
UNGA_START_YEAR = 1991
FIRST_COMMITTEE_START_YEAR = 2003
END_YEAR = 2024
```

## Documentation

- **[Methodology](docs/methodology.md)**: Detailed explanation of data sources, processing steps, and analytical approach
- **[Data Dictionary](docs/data_dictionary.md)**: Complete description of all dataset columns and variables
- **[Troubleshooting](docs/troubleshooting.md)**: Solutions to common issues

## Citation

Citation information will be provided upon publication.

## Data Availability

Processed datasets and reproducible notebooks will be available at:
- **GitHub**: [Repository URL to be added upon publication]
- **Harvard Dataverse**: [Link to be added] (DOI: TBD)

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## Contact

For questions or issues, please open an issue on the repository.
