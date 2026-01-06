"""
CRINK UN Voting Alignment Analysis Package

This package provides utilities for analyzing voting patterns of CRINK countries
(China, Russia, Iran, North Korea) in the United Nations General Assembly.

Modules:
    - data_processing: Loading and preparing voting data
    - alignment_metrics: Calculating various alignment metrics
    - visualization: Creating publication-quality figures

Example:
    >>> from src.data_processing import VotingDataLoader, CRINKAnalyzer
    >>> from pathlib import Path
    >>> 
    >>> loader = VotingDataLoader(Path("data/processed"))
    >>> df = loader.load_voting_data("UNGA_voting_records_filtered.csv")
"""

__version__ = "1.0.0"
__author__ = "Lucian Bumeder and Sabine Mokry-Frey"

# Import key classes for convenience
try:
    from .data_processing import VotingDataLoader, CRINKAnalyzer
    from .alignment_metrics import AlignmentMetrics, TopicAlignment, MajorityAlignment
    from .visualization import PlotConfig, AlignmentPlots, PublicationFigures
except ImportError:
    # Allow package to be imported even if dependencies not installed
    pass

__all__ = [
    'VotingDataLoader',
    'CRINKAnalyzer',
    'AlignmentMetrics',
    'TopicAlignment',
    'MajorityAlignment',
    'PlotConfig',
    'AlignmentPlots',
    'PublicationFigures'
]
