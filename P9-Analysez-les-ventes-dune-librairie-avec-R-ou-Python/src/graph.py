import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

def plot_lorenz(df: pd.DataFrame, targetCol: str, amountCol: str) -> tuple:
    """
    Make the graph of Lorenz courve

    Args:
        df (pd.DataFrame)
        targetCol (str): the name of the target column ex: client_id
        amountCol (str): the name of the cumulative column

    Returns:
        tuple: (ax, gini) -> (graph, gini coefficient)
    """
    ca_by_target = df.groupby(targetCol)[amountCol].sum().sort_values()
    ca_cumsum = ca_by_target.cumsum() / ca_by_target.sum()
    target_cumsum = np.arange(1, len(ca_cumsum) + 1) / len(ca_cumsum)
    gini = 1 - 2 * np.trapezoid(ca_cumsum, target_cumsum)

    fig, ax = plt.subplots(figsize=(8, 8))

    # courbe de Lorenz
    ax.plot(
        target_cumsum,
        ca_cumsum,
        color='cadetblue', 
        linewidth=2, 
        label='Courbe de Lorenz'
    )

    # droite d'égalité parfaite
    ax.plot(
        [0, 1],
        [0, 1],
        color='gray', 
        linewidth=1, 
        linestyle='--', 
        label='Égalité parfaite'
    )

    ax.fill_between(
        target_cumsum,
        ca_cumsum,
        target_cumsum,
        alpha=0.2, 
        color='cadetblue'
    )
    return (ax, gini)


def plot_heatmap(series: pd.Series, mask: bool = False, xlabel: list = None, ylabel: list = None) -> plt.Axes:
    """
    Make Heatmap

    Args:
        df (pd.DataFrame): 
        mask (bool): if mask upper triangle
        xlabel (list): labels for x axis
        ylabel (list): labels for y axis

    Returns:
        tuple: (corr, ax) -> (DataFrame of correlation, graph)
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    
    ax.set_xlabel("")

    if mask:
        masked = np.triu(np.ones_like(series))
        sns.heatmap(
            series,
            mask=masked,
            fmt='.2f',
            annot=True,
            ax=ax,
            cmap='Blues'
        )
    else:
        sns.heatmap(
        series,
        fmt='.2f',
        annot=True,
        ax=ax,
        cmap='Blues'
    )
    if xlabel:
        ax.set_xticklabels(xlabel, rotation=0)
    if ylabel:
        ax.set_yticklabels(ylabel, rotation=0)
    return ax


def plot_qq(series, col):
    fig, ax = plt.subplots(figsize=(6, 6))
    stats.probplot(series.dropna(), plot=ax)

    # points
    ax.get_lines()[0].set(color='cadetblue', markersize=3, alpha=0.5)
    # ligne de référence
    ax.get_lines()[1].set(color='tomato', linewidth=2)
    
    ax.set_title(f'Q-Q Plot — {col}')
    plt.show()


def plot_scatter(df: pd.DataFrame, col_x: str, col_y: str, title: str = None) -> plt.Axes:
    """
    Make Scatter plot with trend line

    Args:
        df (pd.DataFrame): data
        col_x (str): column for x axis
        col_y (str): column for y axis
        titre (str): title of the graph

    Returns:
        plt.Axes: graph
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(
        df[col_x],
        df[col_y],
        alpha=0.2, 
        color='cadetblue', 
        s=10
    )
    # ligne de tendance
    z = np.polyfit(df[col_x], df[col_y], 1)  # 1 = straight line
    p = np.poly1d(z)  # make the z result into a function
    ax.plot(df[col_x].sort_values(), p(df[col_x].sort_values()), color='tomato', linewidth=2)

    ax.set_xlabel(col_x)
    ax.set_ylabel(col_y)
    ax.set_title(title or f'{col_x} vs {col_y}')
    ax.grid(True, alpha=0.3)
    return ax


def plot_boxplot(df: pd.DataFrame, col_x: str, col_y: str, title: str = None) -> plt.Axes:
    """
    Make Box plot

    Args:
        df (pd.DataFrame): data
        col_x (str): categorical column (x axis)
        col_y (str): numerical column (y axis)
        titre (str): title of the graph

    Returns:
        plt.Axes: graph
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    sns.boxplot(
        data=df,
        hue=col_x,
        x=col_x,
        y=col_y,
        ax=ax,
        palette='Blues',
        legend=False
    )
    ax.set_xlabel(col_x)
    ax.set_ylabel(col_y)
    ax.set_title(title or f'{col_x} vs {col_y}')
    ax.grid(True, alpha=0.3, axis='y')

    return ax