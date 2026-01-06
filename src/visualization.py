"""
Visualization utilities for CRINK UN voting alignment analysis.

This module provides functions for creating publication-quality
figures and plots for alignment analysis.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class PlotConfig:
    """Configuration for plot styling and settings."""
    
    def __init__(self, style: str = 'bw', figsize: Tuple = (14, 5), dpi: int = 300):
        """
        Initialize plot configuration.
        
        Parameters
        ----------
        style : str
            Plot style - 'bw' for black/white or 'color'
        figsize : Tuple
            Figure size (width, height)
        dpi : int
            Resolution in dots per inch
        """
        self.style = style
        self.figsize = figsize
        self.dpi = dpi
        
        # Color schemes
        if style == 'bw':
            self.primary_color = 'black'
            self.secondary_color = 'gray'
            self.accent_color = 'darkgray'
            self.cmap = 'Greys'
        else:
            self.primary_color = '#E74C3C'
            self.secondary_color = '#3498DB'
            self.accent_color = '#F39C12'
            self.cmap = 'RdYlGn'
    
    def get_colors(self, n: int) -> List[str]:
        """Get list of n colors from colormap."""
        if self.style == 'bw':
            return plt.cm.Greys(np.linspace(0.4, 0.8, n))
        else:
            return plt.cm.Set3(np.linspace(0, 1, n))


class AlignmentPlots:
    """Create alignment-related visualizations."""
    
    @staticmethod
    def plot_time_series_alignment(
        df: pd.DataFrame,
        year_col: str,
        pct_col: str,
        title: str = "Alignment Over Time",
        config: Optional[PlotConfig] = None
    ) -> Tuple[plt.Figure, plt.Axes]:
        """
        Create time series plot of alignment percentages.
        
        Parameters
        ----------
        df : pd.DataFrame
            Data with year and percentage columns
        year_col : str
            Name of year column
        pct_col : str
            Name of percentage column
        title : str
            Plot title
        config : Optional[PlotConfig]
            Plot configuration
            
        Returns
        -------
        Tuple[plt.Figure, plt.Axes]
            Figure and axes objects
        """
        if config is None:
            config = PlotConfig()
        
        fig, ax = plt.subplots(figsize=config.figsize, dpi=100)
        
        ax.plot(
            df[year_col],
            df[pct_col],
            color=config.primary_color,
            linewidth=2.5,
            marker='o',
            markersize=5
        )
        
        ax.set_xlabel('Year', fontsize=11, fontweight='bold')
        ax.set_ylabel('Alignment (%)', fontsize=11, fontweight='bold')
        ax.set_title(title, fontsize=12, fontweight='bold', pad=20)
        ax.set_ylim(0, 100)
        ax.grid(axis='y', linestyle=':', alpha=0.5)
        
        return fig, ax
    
    @staticmethod
    def plot_stacked_bar(
        df: pd.DataFrame,
        x_col: str,
        y_cols: List[str],
        labels: List[str],
        title: str = "Stacked Distribution",
        config: Optional[PlotConfig] = None
    ) -> Tuple[plt.Figure, plt.Axes]:
        """
        Create stacked bar chart.
        
        Parameters
        ----------
        df : pd.DataFrame
            Data for plotting
        x_col : str
            Column for x-axis (typically years)
        y_cols : List[str]
            Columns to stack
        labels : List[str]
            Labels for stacked components
        title : str
            Plot title
        config : Optional[PlotConfig]
            Plot configuration
            
        Returns
        -------
        Tuple[plt.Figure, plt.Axes]
            Figure and axes objects
        """
        if config is None:
            config = PlotConfig()
        
        fig, ax = plt.subplots(figsize=config.figsize, dpi=100)
        
        colors = config.get_colors(len(y_cols))
        
        x = df[x_col].values
        width = 0.6
        bottom = np.zeros(len(df))
        
        for i, (y_col, label) in enumerate(zip(y_cols, labels)):
            ax.bar(
                x,
                df[y_col],
                width,
                label=label,
                bottom=bottom,
                color=colors[i]
            )
            bottom += df[y_col].values
        
        ax.set_xlabel('Year', fontsize=11, fontweight='bold')
        ax.set_ylabel('Percentage (%)', fontsize=11, fontweight='bold')
        ax.set_title(title, fontsize=12, fontweight='bold', pad=20)
        ax.set_ylim(0, 100)
        ax.legend(loc='upper right', frameon=False, fontsize=10)
        ax.grid(axis='y', linestyle=':', alpha=0.5)
        
        return fig, ax
    
    @staticmethod
    def plot_heatmap(
        df: pd.DataFrame,
        title: str = "Alignment Matrix",
        config: Optional[PlotConfig] = None,
        annot: bool = True
    ) -> Tuple[plt.Figure, plt.Axes]:
        """
        Create heatmap of alignment matrix.
        
        Parameters
        ----------
        df : pd.DataFrame
            Square matrix of alignment values
        title : str
            Plot title
        config : Optional[PlotConfig]
            Plot configuration
        annot : bool
            Whether to annotate cells with values
            
        Returns
        -------
        Tuple[plt.Figure, plt.Axes]
            Figure and axes objects
        """
        if config is None:
            config = PlotConfig()
        
        fig, ax = plt.subplots(figsize=(12, 10), dpi=100)
        
        sns.heatmap(
            df,
            annot=annot,
            fmt='.0f',
            cmap=config.cmap,
            vmin=0,
            vmax=100,
            cbar_kws={'label': 'Alignment (%)'},
            ax=ax,
            linewidths=0.5
        )
        
        ax.set_title(title, fontsize=12, fontweight='bold', pad=20)
        
        return fig, ax
    
    @staticmethod
    def plot_horizontal_bar(
        df: pd.DataFrame,
        label_col: str,
        value_col: str,
        title: str = "Distribution",
        config: Optional[PlotConfig] = None
    ) -> Tuple[plt.Figure, plt.Axes]:
        """
        Create horizontal bar chart.
        
        Parameters
        ----------
        df : pd.DataFrame
            Data with labels and values
        label_col : str
            Column with category labels
        value_col : str
            Column with values
        title : str
            Plot title
        config : Optional[PlotConfig]
            Plot configuration
            
        Returns
        -------
        Tuple[plt.Figure, plt.Axes]
            Figure and axes objects
        """
        if config is None:
            config = PlotConfig()
        
        fig, ax = plt.subplots(figsize=(14, 8), dpi=100)
        
        # Sort by value
        df_sorted = df.sort_values(value_col, ascending=True)
        
        colors = config.get_colors(len(df_sorted))
        
        ax.barh(
            range(len(df_sorted)),
            df_sorted[value_col],
            color=colors
        )
        
        ax.set_yticks(range(len(df_sorted)))
        ax.set_yticklabels(df_sorted[label_col], fontsize=9)
        ax.set_xlabel('Value', fontsize=11, fontweight='bold')
        ax.set_title(title, fontsize=12, fontweight='bold', pad=20)
        ax.grid(axis='x', linestyle=':', alpha=0.5)
        
        return fig, ax


class DyadicPlots:
    """Visualizations for dyadic (pairwise) relationships."""
    
    @staticmethod
    def plot_dyadic_rankings(
        df: pd.DataFrame,
        title: str = "Dyadic Alignment Rankings",
        config: Optional[PlotConfig] = None
    ) -> Tuple[plt.Figure, plt.Axes]:
        """
        Create plot ranking dyadic alignments.
        
        Parameters
        ----------
        df : pd.DataFrame
            Dyadic alignment data with columns: country1, country2, alignment_pct
        title : str
            Plot title
        config : Optional[PlotConfig]
            Plot configuration
            
        Returns
        -------
        Tuple[plt.Figure, plt.Axes]
            Figure and axes objects
        """
        if config is None:
            config = PlotConfig()
        
        fig, ax = plt.subplots(figsize=config.figsize, dpi=100)
        
        # Create pair labels
        df_plot = df.copy()
        df_plot['pair'] = df_plot['country1'] + ' - ' + df_plot['country2']
        df_plot = df_plot.sort_values('alignment_pct', ascending=True)
        
        colors = config.get_colors(len(df_plot))
        
        ax.barh(
            range(len(df_plot)),
            df_plot['alignment_pct'],
            color=colors
        )
        
        ax.set_yticks(range(len(df_plot)))
        ax.set_yticklabels(df_plot['pair'], fontsize=9)
        ax.set_xlabel('Alignment (%)', fontsize=11, fontweight='bold')
        ax.set_title(title, fontsize=12, fontweight='bold', pad=20)
        ax.set_xlim(0, 100)
        ax.grid(axis='x', linestyle=':', alpha=0.5)
        
        return fig, ax


class PublicationFigures:
    """Generate publication-ready figures."""
    
    @staticmethod
    def save_figure(
        fig: plt.Figure,
        filepath: Path,
        dpi: int = 300,
        bbox_inches: str = 'tight'
    ) -> None:
        """
        Save figure with publication-quality settings.
        
        Parameters
        ----------
        fig : plt.Figure
            Figure object
        filepath : Path
            Output file path
        dpi : int
            Resolution in dots per inch
        bbox_inches : str
            Bounding box setting
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        fig.savefig(filepath, dpi=dpi, bbox_inches=bbox_inches)
        print(f"✓ Saved: {filepath.name}")
    
    @staticmethod
    def create_figure_caption(
        title: str,
        description: str,
        data_period: str,
        notes: Optional[str] = None
    ) -> str:
        """
        Format a figure caption for publication.
        
        Parameters
        ----------
        title : str
            Figure title
        description : str
            Brief description of what the figure shows
        data_period : str
            Time period of data
        notes : Optional[str]
            Additional notes
            
        Returns
        -------
        str
            Formatted caption
        """
        caption = f"{title}. {description} ({data_period})."
        
        if notes:
            caption += f" {notes}"
        
        return caption
