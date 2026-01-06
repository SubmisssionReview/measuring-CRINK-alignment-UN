# CRINK UN Voting Alignment: Methodology and Data Dictionary

## Overview

This document describes the data sources, analytical methods, and key variables used in the analysis of CRINK (China, Russia, Iran, North Korea) voting patterns in the United Nations General Assembly.

## Data Sources

### UN General Assembly Voting Records

**Source:** [UN Digital Library - Voting Records](https://digitallibrary.un.org/record/4060887)

**Coverage:**
- **Time Period:** 1946-2024 (analysis uses 1991-2024)
- **Resolutions:** All UNGA plenary and First Committee votes
- **Countries:** 193 UN Member States

**Data Format:**
- CSV files with voting records
- One row per country vote per resolution
- Columns: `undl_id` (resolution ID), `date`, `ms_name` (country name), `ms_vote` (Y/N/A for Yes/No/Abstain)

### Processing Steps

1. **Downloaded** raw voting data from UN Digital Library
2. **Cleaned** country name standardization (e.g., USSR → RUSSIAN FEDERATION)
3. **Converted** dates to standardized format
4. **Filtered** to analysis time periods
5. **Pivoted** to create one-row-per-resolution format for coalition analysis

## Country Groups

### CRINK Countries

| Country | Code | Full Name |
|---------|------|-----------|
| China | CHN | CHINA |
| Russia | RUS | RUSSIAN FEDERATION |
| Iran | IRN | IRAN (ISLAMIC REPUBLIC OF) |
| North Korea | PRK | DEMOCRATIC PEOPLE'S REPUBLIC OF KOREA |

**Selection Rationale:** These four countries are identified as an anti-Western authoritarian coalition that has consistently voted together on major international security issues.

### Western Democracies (Comparison Group)

| Country | Code | Full Name |
|---------|------|-----------|
| United States | USA | UNITED STATES |
| Germany | GER | GERMANY |
| France | FRA | FRANCE |
| United Kingdom | UK | UNITED KINGDOM |

**Selection Rationale:** Established Western democracies with consistent voting patterns and major roles in UN decision-making.

## Key Variables and Metrics

### Vote Variables

**`ms_vote`** - Individual country vote on a resolution
- **Values:** 'Y' (Yes), 'N' (No), 'A' (Abstain)
- **Missing:** Indicates non-voting (absent or not eligible)

**`crink_votes`** - List of votes from all CRINK countries for a resolution
- **Type:** List[str]
- **Used for:** Calculating group voting patterns

**`crink_group_vote`** - Most common vote among CRINK countries
- **Values:** 'Y', 'N', 'A', or None
- **Calculation:** Mode of `crink_votes`
- **Use:** Represents the "CRINK position" on a resolution

### Agreement Metrics

**`agreement_count`** - Number of CRINK countries voting with the group majority
- **Range:** 1-4
- **Minimum Threshold:** 2 countries (votes with only 1 country voting are not counted)
- **Interpretation:**
  - 4: All CRINK countries unanimous
  - 3: Three CRINK countries voting together
  - 2: Two CRINK countries voting together
  - None: Fewer than 2 countries voting together

**`crink_with_majority`** - Binary indicator: CRINK group vote matches UN majority
- **Values:** 1 (aligned), 0 (not aligned), None (indeterminate)
- **Calculation:** `(crink_group_vote == un_majority_vote) & (agreement_count >= 2)`
- **Interpretation:** Shows CRINK's alignment with broader UN consensus

**`anti_us`** - Binary indicator: 4-way CRINK unanimity against US position
- **Calculation:** `(agreement_count == 4) & (crink_group_vote != UNITED_STATES_vote)`
- **Interpretation:** Cases where CRINK acts as unified bloc against the United States

### Time Variables

**`year`** - Calendar year of vote
- **Range:** 1991-2024
- **Used for:** Time series analysis and trend identification

**`date`** - Exact date of vote
- **Format:** YYYY-MM-DD
- **Precision:** Allows for sub-yearly analysis if needed

### Topic Variables (When Available)

**`meta_topic_id`** - Numeric identifier for resolution topic
- **Range:** 1-20
- **Source:** LLM-based consolidation of resolution titles into meta-topics

**`meta_topic_label`** - Descriptive label for resolution topic
- **Examples:** "Human Rights", "Regional Conflicts", "Disarmament"
- **Source:** OpenAI GPT-4o-mini consolidation from clustered topics

## Analysis Periods

### Full UNGA Analysis (1991-2024)
- **Rationale:** Captures full post-Cold War period
- **Resolutions:** ~4,000+
- **Purpose:** Long-term trend analysis, voting pattern evolution

### First Committee Analysis (2003-2024)
- **Rationale:** Disarmament committee voting patterns
- **Coverage:** UN First Committee (UN General Assembly First Committee on Disarmament and International Security)
- **Resolutions:** ~500+
- **Purpose:** Specialized security and disarmament issue analysis

### Post-1991 Period (Why 1991?)
- **Historical Rationale:** Post-Cold War period captures modern voting dynamics
- **Soviet Union:** Transitioned to Russian Federation
- **Geopolitical:** Contemporary coalition structures emerge

## Voting Categories

### Classification of Votes

Votes are classified into categories for analysis:

1. **Coalition Votes** - Resolutions where 2+ CRINK countries vote identically
   - **2-way:** 2 countries voting together
   - **3-way:** 3 countries voting together
   - **4-way:** All 4 countries voting together

2. **Majority Alignment** - CRINK group vote matches UN majority position
   - Calculated as percentage of votes where `crink_with_majority == True`

3. **Divergent Votes** - CRINK countries voting differently
   - When no 2+ countries vote together
   - Suggests internal disagreement

4. **Topic-Based Alignment** - Analysis of coalition patterns by issue area
   - Shows which topics generate CRINK unity
   - Identifies issue-specific coalitions

## Methodology: Alignment Calculations

### Dyadic Alignment

For each pair of countries (e.g., China-Russia):

1. **Identify votes where both countries have a position** (exclude absences)
2. **Count identical votes** (same vote on same resolution)
3. **Calculate percentage:** `(identical votes / total joint votes) × 100`

**Formula:**
```
Dyadic Alignment % = (Σ identical votes) / (Σ joint votes) × 100
```

### Coalition Strength

Measures cohesion within a group on a specific vote:

```
Coalition Strength = (votes for most common position) / (total group votes) × 100
```

**Interpretation:**
- 100%: Perfect unanimity
- 75%: Strong majority
- 50%: Even split
- <50%: Minority position

### Topic-Level Analysis

When topic assignments are available:

1. **Group resolutions by topic** using `meta_topic_label`
2. **Calculate agreement rates per topic:**
   - Resolutions where 2+ CRINK countries vote together
   - Percentage of topic's resolutions with CRINK agreement

3. **Identify patterns:**
   - Topics with high CRINK unity (e.g., anti-Western votes)
   - Topics with CRINK divergence (e.g., trade issues)

## Data Quality Considerations

### Missing Data

**Abstentions:** Recorded as 'A' - full valid votes
**Non-votes:** Missing values indicate:
- Country not present for vote
- Country not eligible to vote
- Data collection gap

**Handling:** Calculations use only available votes; missing data reduces sample size for specific dyads

### Time Coverage Gaps

**Pre-1991 data:** Excluded due to Cold War era differences
**Pre-2003 First Committee:** No data collected; analysis starts 2003

### Country Name Standardization

| Original Name | Standardized | Reason |
|---------------|-------------|---------|
| USSR | RUSSIAN FEDERATION | Soviet Union dissolution (1991) |
| SOUTH YEMEN | (excluded) | Merged with North Yemen (1990) |
| CZECHOSLOVAKIA | (excluded) | Dissolved (1993) |

## Confidence and Limitations

### Strengths
- Complete UN voting record (no sampling)
- Objective, recorded voting positions
- Long historical span (1991-2024)
- High temporal resolution (vote-by-vote)

### Limitations
- UN votes are binary/ternary (Y/N/A) - no intensity measurement
- Absence ≠ disagreement
- Vote not necessarily reflects actual national preference
- Topic classification (if used) based on LLM interpretation
- No weighting for resolution importance or international impact

## Citation and Attribution

When using this data, cite:

1. **UN Data Source:**
   > United Nations General Assembly. Voting Records Database. UN Digital Library. 
   > https://digitallibrary.un.org/record/4060887

2. **This Analysis:**
   > [Author]. CRINK UN Voting Alignment: Reproducible Analysis Repository. 
   > [GitHub URL]. [Year].

## References

### Key Works on UN Voting Analysis
- Voeten, E. (2000). Clashes in the Assembly. International Organization, 54(2), 185-215.
- Dreher, A., Nunnenkamp, P., & Thiele, R. (2008). Does aid for education educate children?. World Development, 36(10), 1737-1753.
- Gartzke, E., & Gleditsch, K. S. (2004). Why democracies don't fight each other. Journal of Peace Research, 41(1), 45-62.

## Contact and Questions

For questions about methodology, data processing, or analysis:
- Check the GitHub repository issues section
- Review notebook documentation in the `notebooks/` folder
- Consult source code comments in `src/` modules
