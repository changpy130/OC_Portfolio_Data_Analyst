import plotly.express as px
import pandas as pd
import numpy as np
from components.calculation import corr_list

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src import is_numeric

# region Basic

def plot_line_plotly(df: pd.DataFrame, col_x: str, col_y: str, title: str = None):
    fig = px.line(
        df,
        x=col_x,
        y=col_y,
        title=title
    )
    return fig


def plot_bar_plotly(df: pd.DataFrame, col_x: str, col_y: str, xlabel: str=None, ylabel: str=None, legendLabel: str=None, title: str = None, color = None, barmode = "group", bar_width=40):
    # Calculate dynamic width based on number of bars
    n_bars = df[col_x].nunique()
    chart_width = max(600, n_bars * bar_width)  # minimum 600px
    
    fig = px.bar(
        df,
        x=col_x,
        y=col_y,
        color=color,
        barmode=barmode
    )
    fig.update_layout(
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        legend_title_text=legendLabel
    )
    return fig


def plot_donut_plotly(values, labels, title=None, hole=0.4):
    """
    Make donut with Plotly Express

    Args:
        values (list): a list of values
        labels (list): a list of names of categories
        title (_type_, optional): Title of the graph. Defaults to None.
        hole (float, optional): Size of the hole of donut. Defaults to 0.4

    Returns:
        fig: go.Figure
    """
    fig = px.pie(
        values=values,
        names=labels,
        hole=hole,
        title=title
    )
    return fig


# region Stats

def plot_stats(df: pd.DataFrame, col1: str, col2: str):
    name_mapping = corr_list()
    name1 = next(k for k, v in name_mapping.items() if v == col1)
    name2 = next(k for k, v in name_mapping.items() if v == col2)
    title = f'{name1} vs {name2}'

    is_numeric1 = is_numeric(df[col1])
    is_numeric2 = is_numeric(df[col2])

    if is_numeric1 and is_numeric2:
        return plot_scatter_plotly(
            df,
            col1,
            col2, 
            title=title
        )
    elif is_numeric1 or is_numeric2:
        num_col = col1 if is_numeric1 else col2
        cat_col = col2 if is_numeric1 else col1

        return plot_boxplot_plotly(
            df,
            cat_col,
            num_col,
            title=title
        )
    else:
        table = pd.crosstab(df[col1], df[col2], normalize='index') * 100
        return plot_heatmap_plotly(
            table,
            title=title
        )

def plot_scatter_plotly(df: pd.DataFrame, col_x: str, col_y: str, title: str = None):
    """
    Make scatter plot with Plotly Express

    Args:
        df (pd.DataFrame)
        col_x (str): the name of the column of x axis
        col_y (str): the name of the column of y axis
        title (str, optional): Title of the graph. Defaults to None.

    Returns:
        fig: go.Figure
    """
    # Remove extreme outliers for display (keep 99th percentile)
    q_low = df[col_y].quantile(0.01)
    q_high = df[col_y].quantile(0.99)
    
    fig = px.scatter(
        df,
        x=col_x,
        y=col_y,
        title=title or f'{col_x} vs {col_y}',
        color_discrete_sequence=['cadetblue'],
        trendline='ols',
        trendline_color_override='tomato',
        opacity=0.3
    )
    
    # 👇 cap the y axis without removing the data
    fig.update_layout(
        yaxis=dict(range=[q_low, q_high])
    )
    return fig


def plot_boxplot_plotly(df: pd.DataFrame, col_x: str, col_y: str, title: str = None, color=None):
    """
    Make boxplot with Plotly Express

    Args:
        df (pd.DataFrame)
        col_x (str): the name of the column of x axis
        col_y (str): the name of the column of y axis
        title (str, optional): Title of the graph. Defaults to None.
        color (str): the name of column for legend

    Returns:
        fig: go.Figure
    """
    q_low = df[col_y].quantile(0.01)
    q_high = df[col_y].quantile(0.99)

    fig = px.box(
        df,
        x=col_x,
        y=col_y,
        color=color or col_x,
        title=title or f"{col_x} vs {col_y}"
    )
    fig.update_layout(
        yaxis=dict(range=[q_low, q_high])
    )
    return fig


def plot_heatmap_plotly(crosstab, title=None, color='blues'):
    """
    Make heatmap with Plotly Express

    Args:
        crosstab (pd.DataFrame): Cross table in percentage (ex: pd.crosstab(df_b2c['sex'], df_b2c['categ'], normalize='index') * 100)
        title (str, optional): Title of the graph. Defaults to None.
        color (str, optional): Color palette of scale. Default to Blue

    Returns:
        fig: go.Figure
    """
    fig = px.imshow(
        crosstab,
        text_auto='.1f',
        color_continuous_scale=color,
        title=title,
        aspect='auto',    
    )
    fig.update_layout(
        xaxis_title=crosstab.columns.name, 
        yaxis_title=crosstab.index.name,
        coloraxis_colorbar=dict(title='%') 
    )
    return fig


# region Lorenz

def plot_lorenz_plotly(df: pd.DataFrame, targetCol: str, amountCol: str, title="") -> tuple:
    values = df.groupby(targetCol)[amountCol].sum().sort_values()
    cumsum = values.cumsum() / values.sum()
    equal_cumsum = np.arange(1, len(cumsum) + 1) / len(cumsum)
    gini = 1 - 2 * np.trapezoid(cumsum, equal_cumsum)

    # DataFrame for plotting
    plot_df = pd.DataFrame({
        "Population share": equal_cumsum,
        "Courbe de Lorenz": cumsum,
        "Equality line": equal_cumsum
    })

    fig = px.line(
        plot_df,
        x="Population share",
        y=["Courbe de Lorenz", "Equality line"]
    )

    # Colour the area in between
    import plotly.graph_objects as go
    fig = go.Figure()

    # Equality line
    fig.add_trace(go.Scatter(
        x=equal_cumsum,
        y=equal_cumsum,
        mode='lines',
        name='Égalité parfaite',
        line=dict(color='gray', width=1, dash='dash')
    ))

    # Lorenz curve with fill
    fig.add_trace(go.Scatter(
        x=equal_cumsum,
        y=cumsum,
        mode='lines',
        name='Courbe de Lorenz',
        fill='tonexty'  # fills area between curves
    ))

    fig.update_layout(
        title=title,
        xaxis_title="Proportion cumulée des clients",
        yaxis_title="Proportion cumulée du CA"
    )

    return (fig, gini)


# region Product positioning

def plot_product_positioning(df: pd.DataFrame, top_n=10):
    df_products = pd.DataFrame({
        'ca': df.groupby('id_prod')['price'].sum(),
        'quantity': df.groupby('id_prod').size()
    })

    # Categorise
    top_ca = set(df_products.nlargest(top_n, 'ca').index)
    top_quantity = set(df_products.nlargest(top_n, 'quantity').index)

    stars = top_ca & top_quantity
    cher_rare = top_ca - top_quantity
    populaire_pas_cher = top_quantity - top_ca

    def categorise(prod):
        if prod in stars:
            return 'Star'
        elif prod in cher_rare:
            return 'Cher & Rare'
        elif prod in populaire_pas_cher:
            return 'Populaire & Pas cher'
        else:
            return 'Autres'

    df_products['categorie'] = df_products.index.map(categorise)
    df_products['id_prod'] = df_products.index  # for hover

    color_map = {
        'Star': 'gold',
        'Cher & Rare': 'tomato',
        'Populaire & Pas cher': 'cadetblue',
        'Autres': 'lightgray'
    }

    # Size — highlight non-Autres
    df_products['size'] = df_products['categorie'].apply(
        lambda x: 15 if x != 'Autres' else 6
    )

    fig = px.scatter(
        df_products,
        x='quantity',
        y='ca',
        color='categorie',
        color_discrete_map=color_map,
        size='size',
        size_max=20,
        hover_name='id_prod',          # 👈 product name on hover
        hover_data={'quantity': True, 'ca': ':.2f', 'size': False, 'categorie': False},
        text=df_products.index.where(df_products['categorie'] != 'Autres', other=''),  # 👈 labels only for top products
        labels={'quantity': 'Quantité vendue', 'ca': 'CA (€)', 'categorie': 'Catégorie'},
        opacity=0.7,
        height=600
    )

    fig.update_traces(textposition='top center', textfont_size=10)
    fig.update_layout(legend_title_text='Catégorie')

    return fig