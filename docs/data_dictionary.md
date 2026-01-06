# Data Dictionary: CRINK UN Voting Alignment Analysis

## File Overview

This document describes all variables in the datasets used in the CRINK UN voting alignment analysis.

## Core Voting Data Files

### `UNGA_voting_records_filtered.csv`

**Description:** UN General Assembly plenary voting records, 1991-2024

**Size:** ~250,000 rows (individual country votes)

**Time Period:** 1991-2024

**Variables:**

| Variable | Type | Description | Example | Notes |
|----------|------|-------------|---------|-------|
| `undl_id` | String | UN Digital Library resolution identifier | "A/RES/76/1" | Unique per resolution |
| `date` | Date | Vote date | "2021-09-20" | YYYY-MM-DD format |
| `year` | Integer | Calendar year | 2021 | Derived from date |
| `ms_name` | String | UN member state name | "UNITED STATES" | Standardized country name |
| `country_code` | String | ISO 3-letter country code | "USA" | When available |
| `ms_vote` | String | Vote on resolution | "Y", "N", "A" | Y=Yes, N=No, A=Abstain |
| `topic` | String | Resolution topic category | "Human Rights" | When available from title analysis |
| `title` | String | Official resolution title | "Resolution on Climate Action" | Descriptive resolution title |

**Data Quality:**
- Missing `ms_vote` indicates non-vote (absence, not eligible)
- All country names standardized to UN official naming conventions
- Covers 193 UN Member States

---

### `first_committee_voting_records.csv`

**Description:** UN First Committee (Disarmament and International Security) voting records

**Size:** ~15,000 rows

**Time Period:** 2003-2024

**Variables:** Same as UNGA voting records, with topic focusing on disarmament and security issues

---

## Processed/Aggregated Files

### `crink_yearly_statistics_[DATE].csv`

**Description:** Annual CRINK voting agreement statistics

**Generated:** After running Notebook 1

**Variables:**

| Variable | Type | Description | Range | Notes |
|----------|------|-------------|-------|-------|
| `year` | Integer | Calendar year | 1991-2024 | One row per year |
| `total_votes` | Integer | Total resolutions with 2+ CRINK agreement | 1+ | Count of resolutions |
| `votes_2way` | Integer | Resolutions with 2-country CRINK alignment | 0+ | 2 countries voting together |
| `votes_3way` | Integer | Resolutions with 3-country CRINK alignment | 0+ | 3 countries voting together |
| `votes_4way` | Integer | Resolutions with all 4-country CRINK alignment | 0+ | All 4 countries unanimous |
| `votes_with_majority` | Integer | CRINK votes aligned with UN majority | 0+ | Count matching UN consensus |
| `pct_2way` | Float | Percentage of resolutions with 2-way agreement | 0-100 | Percentage of agreement votes |
| `pct_3way` | Float | Percentage of resolutions with 3-way agreement | 0-100 | Percentage of agreement votes |
| `pct_4way` | Float | Percentage of resolutions with 4-way agreement | 0-100 | Percentage of agreement votes |
| `pct_majority` | Float | Percentage aligned with UN majority | 0-100 | Among all resolutions |

---

### `crink_dyadic_alignment_[DATE].csv`

**Description:** Pairwise voting alignment between CRINK countries

**Generated:** After running Notebook 1

**Variables:**

| Variable | Type | Description | Example | Notes |
|----------|------|-------------|---------|-------|
| `country1` | String | First country name | "China" | Standardized name (shortened) |
| `country2` | String | Second country name | "Russia" | Standardized name (shortened) |
| `alignment_pct` | Float | Percentage voting alignment | 87.3 | 0-100 scale |
| `identical_votes` | Integer | Number of identically cast votes | 1825 | Count of matching votes |
| `total_votes` | Integer | Total votes where both countries participated | 2090 | Denominator for percentage |

**Interpretation:**
- Higher `alignment_pct` indicates stronger bilateral voting coordination
- `total_votes` varies by country pair (different participation rates)

---

### `crink_voting_records_[DATE].csv`

**Description:** Full voting records with CRINK analysis variables

**Generated:** After running Notebook 1

**Variables:**

| Variable | Type | Description | Values | Notes |
|----------|------|-------------|--------|-------|
| `undl_id` | String | Resolution identifier | "A/RES/76/1" | UN official ID |
| `date` | Date | Vote date | "2021-09-20" | YYYY-MM-DD |
| `year` | Integer | Calendar year | 1991-2024 | For time series |
| `crink_group_vote` | String | CRINK majority vote | "Y", "N", "A" | Most common CRINK vote |
| `agreement_count` | Integer | Number CRINK countries in majority | 2, 3, 4 | Null if <2 countries agree |
| `un_majority_vote` | String | UN-wide majority vote | "Y", "N", "A" | Most common global vote |
| `crink_with_majority` | Integer | Alignment with UN majority | 0, 1 | 1 if CRINK matches global majority |

---

### `table_01_topic_alignment_[DATE].csv`

**Description:** Topic-level alignment statistics (when topic mappings available)

**Variables:**

| Variable | Type | Description | Notes |
|----------|------|-------------|-------|
| `meta_topic_label` | String | Topic category | e.g., "Human Rights" |
| `total_votes` | Integer | Resolutions in this topic | Count |
| `crink_agreement` | Integer | Resolutions with 2+ CRINK agreement | Subset of total |
| `votes_4way` | Integer | Resolutions with 4-way CRINK unanimity | Subset |
| `votes_3way` | Integer | Resolutions with 3-way CRINK agreement | Subset |
| `votes_2way` | Integer | Resolutions with 2-way CRINK agreement | Subset |
| `pct_agreement` | Float | Percentage with 2+ CRINK agreement | 0-100 |

---

### `table_02_dyadic_alignment_[DATE].csv`

**Description:** Full dyadic alignment matrix (all country pairs)

**Format:** Square matrix where:
- Rows: Country names
- Columns: Country names
- Values: Alignment percentage (0-100)
- Diagonal: 100 (self-alignment)
- Symmetric: Alignment is reciprocal

**Usage:** For heatmaps and visual comparison

---

### `table_03_pair_statistics_[DATE].csv`

**Description:** Detailed statistics for all country pairs

**Variables:**

| Variable | Type | Description |
|----------|------|-------------|
| `Country 1` | String | First country (shortened) |
| `Country 2` | String | Second country (shortened) |
| `Total Votes` | Integer | Joint voting occasions |
| `Agreement` | Integer | Identical votes |
| `Agreement %` | Float | Alignment percentage (0-100) |

---

## Topic Mapping Files (Optional)

### `meta_topic_mapping.json`

**Description:** Mapping of resolution IDs to topic assignments

**Format:** JSON with structure:
```json
{
  "A/RES/76/1": {
    "meta_topic_id": 5,
    "meta_topic_label": "Human Rights",
    "confidence": 0.92
  },
  ...
}
```

**Variables:**
- `meta_topic_id`: Numeric topic identifier (1-20)
- `meta_topic_label`: Human-readable topic name
- `confidence`: LLM confidence in assignment (0-1)

---

## Naming Conventions

### Country Names (Standardized)

| Code | Full UN Name | Region |
|------|-------------|--------|
| CHN | CHINA | Asia-Pacific |
| RUS | RUSSIAN FEDERATION | Europe/Asia |
| IRN | IRAN (ISLAMIC REPUBLIC OF) | Middle East |
| PRK | DEMOCRATIC PEOPLE'S REPUBLIC OF KOREA | Asia-Pacific |
| USA | UNITED STATES | Americas |
| GER | GERMANY | Europe |
| FRA | FRANCE | Europe |
| UK | UNITED KINGDOM | Europe |

### File Naming Conventions

- Date stamps: `_YYYYMMDD` (e.g., `_20240115`)
- Versioning: Files with timestamps indicate regeneration date
- Versions: Each analysis run creates new files with current date

---

## Data Validation Checklist

When processing new data:

- [ ] All country names match standardized list
- [ ] Dates are in YYYY-MM-DD format
- [ ] Votes are 'Y', 'N', or 'A' (or missing)
- [ ] No duplicate rows per country-resolution pair
- [ ] `agreement_count` is 2-4 or null (never 0 or 1)
- [ ] `alignment_pct` values are 0-100
- [ ] Year matches date if both present

---

## Data Access and Download

**Official Source:** UN Digital Library
- URL: https://digitallibrary.un.org/record/4060887
- Download: CSV format, complete voting records
- Update Frequency: Annual

**Harvard Dataverse:**
- Contains processed/cleaned versions
- Includes pre-computed topic mappings
- README with exact data versions used

---

## Missing Data Codes

| Code | Meaning |
|------|---------|
| (blank) | Country did not vote / absent |
| "Y" | Voted Yes |
| "N" | Voted No |
| "A" | Abstained |
| NA/None | Data not available |

**Note:** Missing values are NOT imputed. Analysis uses only available votes.

---

## Temporal Coverage Notes

| Period | Data Source | Coverage |
|--------|-------------|----------|
| 1946-1990 | UN Digital Library | Available but not used |
| 1991-2024 | UN Digital Library | Primary analysis period |
| 2003-2024 | Manual collection | First Committee data |
| 2025+ | Not available | Future data collection required |

**Why 1991?** Marks post-Cold War era with:
- Soviet Union transition to Russian Federation
- Modern geopolitical coalitions
- Digital record availability
