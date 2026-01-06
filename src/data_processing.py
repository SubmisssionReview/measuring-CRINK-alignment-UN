"""
Data processing utilities for CRINK UN voting alignment analysis.

This module provides functions for loading, cleaning, and preparing
UN General Assembly voting data for alignment analysis.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import Counter


class VotingDataLoader:
    """Load and prepare UN voting records for analysis."""
    
    def __init__(self, data_dir: Path):
        """
        Initialize data loader.
        
        Parameters
        ----------
        data_dir : Path
            Directory containing voting data CSV files
        """
        self.data_dir = Path(data_dir)
    
    def load_voting_data(self, filename: str) -> pd.DataFrame:
        """
        Load voting data from CSV file.
        
        Parameters
        ----------
        filename : str
            Name of CSV file to load
            
        Returns
        -------
        pd.DataFrame
            Voting data with columns: ms_name, ms_vote, date, undl_id
        """
        filepath = self.data_dir / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"Data file not found: {filepath}")
        
        df = pd.read_csv(filepath, encoding='utf-8')
        
        # Standardize country names
        if 'ms_name' in df.columns:
            df['ms_name'] = df['ms_name'].replace({'USSR': 'RUSSIAN FEDERATION'})
        
        # Convert dates
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df['year'] = df['date'].dt.year
        
        return df
    
    def filter_by_period(self, df: pd.DataFrame, start_year: int, end_year: int) -> pd.DataFrame:
        """
        Filter voting data to specified time period.
        
        Parameters
        ----------
        df : pd.DataFrame
            Voting data
        start_year : int
            Start year (inclusive)
        end_year : int
            End year (inclusive)
            
        Returns
        -------
        pd.DataFrame
            Filtered voting data
        """
        if 'year' not in df.columns:
            raise ValueError("DataFrame must have 'year' column")
        
        return df[(df['year'] >= start_year) & (df['year'] <= end_year)].copy()
    
    def create_vote_pivot(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create pivot table with one row per resolution.
        
        Parameters
        ----------
        df : pd.DataFrame
            Voting data with ms_vote column
            
        Returns
        -------
        pd.DataFrame
            Pivot table with countries as columns and votes as values
        """
        pivot = df.pivot_table(
            index=['undl_id', 'date'],
            columns='ms_name',
            values='ms_vote',
            aggfunc='first'
        ).reset_index()
        
        if 'date' in pivot.columns:
            pivot['year'] = pd.to_datetime(pivot['date']).dt.year
        
        return pivot


class CRINKAnalyzer:
    """Analyze voting patterns of CRINK countries."""
    
    CRINK_COUNTRIES = {
        'CHINA': 'CHN',
        'RUSSIAN FEDERATION': 'RUS',
        'IRAN (ISLAMIC REPUBLIC OF)': 'IRN',
        "DEMOCRATIC PEOPLE'S REPUBLIC OF KOREA": 'PRK'
    }
    
    WESTERN_COUNTRIES = {
        'UNITED STATES': 'USA',
        'GERMANY': 'GER',
        'FRANCE': 'FRA',
        'UNITED KINGDOM': 'UK'
    }
    
    def __init__(self, vote_pivot: pd.DataFrame):
        """
        Initialize analyzer with voting pivot table.
        
        Parameters
        ----------
        vote_pivot : pd.DataFrame
            Pivot table with one row per resolution
        """
        self.vote_pivot = vote_pivot.copy()
    
    def calculate_crink_votes(self) -> pd.DataFrame:
        """
        Calculate CRINK group vote and agreement patterns.
        
        Returns
        -------
        pd.DataFrame
            Original pivot table with added columns:
            - crink_votes: list of individual votes
            - crink_group_vote: most common vote
            - agreement_count: number of countries voting with majority
        """
        crink_list = list(self.CRINK_COUNTRIES.keys())
        
        # Extract CRINK votes
        self.vote_pivot['crink_votes'] = self.vote_pivot.apply(
            lambda row: [row[c] for c in crink_list if c in row.index and pd.notna(row[c])],
            axis=1
        )
        
        # Most common vote
        self.vote_pivot['crink_group_vote'] = self.vote_pivot['crink_votes'].apply(
            lambda votes: Counter(votes).most_common(1)[0][0] if votes else None
        )
        
        # Agreement count (minimum 2 countries needed)
        self.vote_pivot['agreement_count'] = self.vote_pivot['crink_votes'].apply(
            self._count_agreement
        )
        
        return self.vote_pivot
    
    @staticmethod
    def _count_agreement(votes: List[str]) -> Optional[int]:
        """
        Count number of countries voting with the group majority.
        
        Returns None if fewer than 2 countries or no majority vote.
        """
        if len(votes) < 2:
            return None
        
        counts = Counter(votes)
        most_common_vote, count = counts.most_common(1)[0]
        
        return count if count >= 2 else None
    
    def calculate_dyadic_alignment(self, countries: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Calculate pairwise voting alignment.
        
        Parameters
        ----------
        countries : Optional[List[str]]
            List of country names to analyze. If None, uses CRINK countries.
            
        Returns
        -------
        pd.DataFrame
            Alignment statistics for each country pair
        """
        if countries is None:
            countries = list(self.CRINK_COUNTRIES.keys())
        
        alignment_data = []
        
        for i, country1 in enumerate(countries):
            for country2 in countries[i+1:]:
                if country1 in self.vote_pivot.columns and country2 in self.vote_pivot.columns:
                    both_voted = self.vote_pivot[
                        (self.vote_pivot[country1].notna()) & 
                        (self.vote_pivot[country2].notna())
                    ]
                    
                    if len(both_voted) > 0:
                        identical = (both_voted[country1] == both_voted[country2]).sum()
                        total = len(both_voted)
                        
                        alignment_data.append({
                            'country1': country1.split()[0],
                            'country2': country2.split()[0],
                            'votes_identical': identical,
                            'votes_total': total,
                            'alignment_pct': 100 * identical / total
                        })
        
        df_alignment = pd.DataFrame(alignment_data)
        return df_alignment.sort_values('alignment_pct', ascending=False)
    
    def calculate_western_alignment(self) -> pd.DataFrame:
        """
        Calculate CRINK vs Western democracies alignment.
        
        Returns
        -------
        pd.DataFrame
            Same pivot table with added columns for Western voting
        """
        western_list = list(self.WESTERN_COUNTRIES.keys())
        
        # Extract Western votes
        self.vote_pivot['western_votes'] = self.vote_pivot.apply(
            lambda row: [row[c] for c in western_list if c in row.index and pd.notna(row[c])],
            axis=1
        )
        
        # Most common Western vote
        self.vote_pivot['western_group_vote'] = self.vote_pivot['western_votes'].apply(
            lambda votes: Counter(votes).most_common(1)[0][0] if votes else None
        )
        
        # Western agreement count
        self.vote_pivot['western_agreement_count'] = self.vote_pivot['western_votes'].apply(
            self._count_agreement
        )
        
        # CRINK vs Western comparison
        self.vote_pivot['crink_vs_western'] = (
            (self.vote_pivot['crink_group_vote'] == self.vote_pivot['western_group_vote']) & 
            self.vote_pivot['agreement_count'].notna() &
            self.vote_pivot['western_agreement_count'].notna()
        )
        
        return self.vote_pivot
    
    def get_summary_stats(self) -> Dict[str, any]:
        """
        Get summary statistics of CRINK voting.
        
        Returns
        -------
        Dict
            Summary statistics including agreement counts and percentages
        """
        stats = {
            'total_resolutions': len(self.vote_pivot),
            'total_crink_votes': self.vote_pivot['agreement_count'].notna().sum(),
            'votes_2way': (self.vote_pivot['agreement_count'] == 2).sum(),
            'votes_3way': (self.vote_pivot['agreement_count'] == 3).sum(),
            'votes_4way': (self.vote_pivot['agreement_count'] == 4).sum(),
        }
        
        total_agreement = stats['total_crink_votes']
        if total_agreement > 0:
            stats['pct_2way'] = 100 * stats['votes_2way'] / total_agreement
            stats['pct_3way'] = 100 * stats['votes_3way'] / total_agreement
            stats['pct_4way'] = 100 * stats['votes_4way'] / total_agreement
        
        return stats
