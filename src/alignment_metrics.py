"""
Alignment metrics and statistical utilities for voting analysis.

This module provides functions for calculating various measures of
voting alignment and coalition strength in UN voting data.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from collections import Counter


class AlignmentMetrics:
    """Calculate various voting alignment metrics."""
    
    @staticmethod
    def jaccard_similarity(votes1: List[str], votes2: List[str]) -> float:
        """
        Calculate Jaccard similarity between two voting patterns.
        
        Parameters
        ----------
        votes1, votes2 : List[str]
            Lists of votes (typically 'Yes', 'No', 'Abstain')
            
        Returns
        -------
        float
            Jaccard similarity (0-1)
        """
        if len(votes1) == 0 or len(votes2) == 0:
            return np.nan
        
        set1 = set(votes1)
        set2 = set(votes2)
        
        if len(set1 | set2) == 0:
            return 0.0
        
        return len(set1 & set2) / len(set1 | set2)
    
    @staticmethod
    def voting_agreement(country1_votes: pd.Series, country2_votes: pd.Series) -> float:
        """
        Calculate percentage of identical votes between two countries.
        
        Parameters
        ----------
        country1_votes, country2_votes : pd.Series
            Series of votes for each country
            
        Returns
        -------
        float
            Percentage agreement (0-100)
        """
        # Filter for votes where both countries have a valid vote
        both_voted = (country1_votes.notna()) & (country2_votes.notna())
        
        if both_voted.sum() == 0:
            return np.nan
        
        identical = (country1_votes[both_voted] == country2_votes[both_voted]).sum()
        total = both_voted.sum()
        
        return 100 * identical / total
    
    @staticmethod
    def coalition_strength(votes: List[str]) -> float:
        """
        Measure how cohesive a group is in their voting.
        
        Returns the percentage of the most common vote.
        
        Parameters
        ----------
        votes : List[str]
            List of votes from group members
            
        Returns
        -------
        float
            Cohesion percentage (0-100)
        """
        if len(votes) == 0:
            return np.nan
        
        counts = Counter(votes)
        most_common_count = counts.most_common(1)[0][1]
        
        return 100 * most_common_count / len(votes)
    
    @staticmethod
    def agreement_variance(votes_by_member: Dict[str, List[str]]) -> float:
        """
        Calculate variance in voting patterns across group members.
        
        Lower variance = more uniform voting patterns.
        
        Parameters
        ----------
        votes_by_member : Dict[str, List[str]]
            Dictionary mapping member names to their vote lists
            
        Returns
        -------
        float
            Variance in agreement percentages
        """
        if len(votes_by_member) < 2:
            return np.nan
        
        # Calculate pairwise agreements
        members = list(votes_by_member.keys())
        agreements = []
        
        for i, m1 in enumerate(members):
            for m2 in members[i+1:]:
                # Count matching votes
                matches = sum(
                    1 for v1, v2 in zip(votes_by_member[m1], votes_by_member[m2])
                    if v1 == v2 and pd.notna(v1) and pd.notna(v2)
                )
                total = sum(
                    1 for v1, v2 in zip(votes_by_member[m1], votes_by_member[m2])
                    if pd.notna(v1) and pd.notna(v2)
                )
                if total > 0:
                    agreements.append(100 * matches / total)
        
        if len(agreements) == 0:
            return np.nan
        
        return np.var(agreements)


class TopicAlignment:
    """Analyze alignment patterns by topic."""
    
    @staticmethod
    def alignment_by_topic(
        df: pd.DataFrame,
        topic_col: str,
        group_countries: List[str]
    ) -> pd.DataFrame:
        """
        Calculate alignment statistics grouped by topic.
        
        Parameters
        ----------
        df : pd.DataFrame
            Voting data with topic column
        topic_col : str
            Name of column containing topic labels
        group_countries : List[str]
            List of country names in the group
            
        Returns
        -------
        pd.DataFrame
            Alignment statistics by topic
        """
        results = []
        
        for topic in df[topic_col].unique():
            topic_data = df[df[topic_col] == topic]
            
            # Count votes
            total_votes = len(topic_data)
            
            # Calculate group agreement
            topic_data['group_votes'] = topic_data.apply(
                lambda row: [row[c] for c in group_countries 
                           if c in row.index and pd.notna(row[c])],
                axis=1
            )
            
            topic_data['agreement_count'] = topic_data['group_votes'].apply(
                lambda votes: sum(1 for v in Counter(votes).values() if v >= 2)
                if len(votes) >= 2 else 0
            )
            
            unanimous = (topic_data['agreement_count'] > 0).sum()
            
            results.append({
                'topic': topic,
                'total_resolutions': total_votes,
                'unanimous_resolutions': unanimous,
                'agreement_pct': 100 * unanimous / total_votes if total_votes > 0 else 0
            })
        
        return pd.DataFrame(results).sort_values('agreement_pct', ascending=False)
    
    @staticmethod
    def voting_divergence_by_topic(
        df: pd.DataFrame,
        topic_col: str,
        countries: List[str]
    ) -> pd.DataFrame:
        """
        Measure voting divergence within a group by topic.
        
        Parameters
        ----------
        df : pd.DataFrame
            Voting data
        topic_col : str
            Name of topic column
        countries : List[str]
            List of country names
            
        Returns
        -------
        pd.DataFrame
            Divergence statistics by topic
        """
        results = []
        
        for topic in df[topic_col].unique():
            topic_data = df[df[topic_col] == topic]
            
            # Calculate pairwise agreements
            agreements = []
            for i, c1 in enumerate(countries):
                for c2 in countries[i+1:]:
                    if c1 in topic_data.columns and c2 in topic_data.columns:
                        both = topic_data[
                            (topic_data[c1].notna()) & (topic_data[c2].notna())
                        ]
                        if len(both) > 0:
                            agreement = 100 * (both[c1] == both[c2]).sum() / len(both)
                            agreements.append(agreement)
            
            if agreements:
                results.append({
                    'topic': topic,
                    'avg_agreement': np.mean(agreements),
                    'agreement_std': np.std(agreements),
                    'min_agreement': np.min(agreements),
                    'max_agreement': np.max(agreements)
                })
        
        return pd.DataFrame(results)


class MajorityAlignment:
    """Analyze alignment with UN majority voting patterns."""
    
    @staticmethod
    def get_majority_vote(df: pd.DataFrame, resolution_id: str) -> Optional[str]:
        """
        Determine the majority vote for a specific resolution.
        
        Parameters
        ----------
        df : pd.DataFrame
            Voting data
        resolution_id : str
            Resolution ID
            
        Returns
        -------
        Optional[str]
            Majority vote ('Y', 'N', 'A') or None if indeterminate
        """
        resolution_votes = df[df['undl_id'] == resolution_id]['ms_vote']
        
        if len(resolution_votes) == 0:
            return None
        
        vote_counts = resolution_votes.value_counts()
        
        if len(vote_counts) == 0:
            return None
        
        return vote_counts.index[0]
    
    @staticmethod
    def calculate_majority_alignment(
        df: pd.DataFrame,
        group_countries: List[str]
    ) -> pd.DataFrame:
        """
        Calculate group alignment with UN majority votes.
        
        Parameters
        ----------
        df : pd.DataFrame
            Voting data with undl_id and ms_vote columns
        group_countries : List[str]
            List of country names in group
            
        Returns
        -------
        pd.DataFrame
            Original dataframe with added columns:
            - 'majority_vote': The majority UN vote for each resolution
            - 'group_majority_vote': The group's most common vote
            - 'aligned_with_majority': Boolean indicating alignment
        """
        df = df.copy()
        
        # Get majority vote per resolution
        majority_votes = df.groupby('undl_id')['ms_vote'].apply(
            lambda x: x.mode()[0] if len(x.mode()) > 0 else None
        ).to_dict()
        
        df['majority_vote'] = df['undl_id'].map(majority_votes)
        
        # Get group majority vote
        df['group_votes'] = df.apply(
            lambda row: [row[c] for c in group_countries 
                        if c in row.index and pd.notna(row[c])],
            axis=1
        )
        
        df['group_majority_vote'] = df['group_votes'].apply(
            lambda votes: Counter(votes).most_common(1)[0][0] if votes else None
        )
        
        # Check alignment
        df['aligned_with_majority'] = (
            (df['group_majority_vote'] == df['majority_vote']) & 
            (df['group_votes'].apply(len) >= 2)
        )
        
        return df
    
    @staticmethod
    def majority_alignment_summary(df: pd.DataFrame) -> Dict[str, any]:
        """
        Get summary statistics of majority alignment.
        
        Parameters
        ----------
        df : pd.DataFrame
            Dataframe with 'aligned_with_majority' column
            
        Returns
        -------
        Dict
            Summary statistics
        """
        aligned = df['aligned_with_majority'].sum()
        total = df['aligned_with_majority'].notna().sum()
        
        return {
            'total_resolutions': total,
            'aligned_resolutions': aligned,
            'alignment_pct': 100 * aligned / total if total > 0 else 0
        }


class TimeSeriesAlignment:
    """Analyze voting alignment trends over time."""
    
    @staticmethod
    def yearly_alignment_stats(
        df: pd.DataFrame,
        year_col: str,
        group_countries: List[str]
    ) -> pd.DataFrame:
        """
        Calculate alignment statistics by year.
        
        Parameters
        ----------
        df : pd.DataFrame
            Voting data with year column
        year_col : str
            Name of year column
        group_countries : List[str]
            List of countries in group
            
        Returns
        -------
        pd.DataFrame
            Yearly alignment statistics
        """
        yearly_stats = []
        
        for year in sorted(df[year_col].unique()):
            year_data = df[df[year_col] == year]
            
            # Calculate votes with agreement
            year_data_copy = year_data.copy()
            year_data_copy['group_votes'] = year_data_copy.apply(
                lambda row: [row[c] for c in group_countries 
                            if c in row.index and pd.notna(row[c])],
                axis=1
            )
            
            total = len(year_data_copy)
            unanimous = sum(
                1 for votes in year_data_copy['group_votes']
                if len(votes) >= 2 and len(set(votes)) == 1
            )
            
            yearly_stats.append({
                'year': year,
                'total_resolutions': total,
                'unanimous_votes': unanimous,
                'unanimity_pct': 100 * unanimous / total if total > 0 else 0
            })
        
        return pd.DataFrame(yearly_stats)
