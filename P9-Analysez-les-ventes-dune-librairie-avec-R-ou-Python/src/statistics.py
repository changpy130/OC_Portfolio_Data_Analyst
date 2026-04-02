import pandas as pd
from scipy.stats import shapiro, pearsonr, spearmanr, chi2_contingency, f_oneway

# region Entry point

def test_statistic(df: pd.DataFrame, col1: str, col2: str, alpha=0.05):
    """
    Entry point of statistic tests, currently including: Shapiro-Wilk, Pearson, Spearman, Chi-2, ANOVA

    Args:
        df (pd.DataFrame)
        col1 (str): the first column name 
        col2 (str): the second column name 
        alpha (float, optional): threshold, defaults to 0.05
    """
    is_number1 = is_numeric(df[col1])
    is_number2 = is_numeric(df[col2])
    result = ""

    if is_number1 and is_number2:
        result = test_numerical(df=df, col1=col1, col2=col2, alpha=alpha)
    elif not is_number1 and not is_number2:
        result = test_categorical(series1=df[col1], series2=df[col2], alpha=alpha)
    elif is_number1:
        result = test_mixed(df=df, col_category=col2, col_value=col1, alpha=alpha)
    elif is_number2:
        result = test_mixed(df=df, col_category=col1, col_value=col2, alpha=alpha)

    return result

# region Numerical (Quantity-Quantity)

def test_numerical(df: pd.DataFrame, col1: str, col2: str, alpha=0.05):
    """
    Test for 2 quantitative variables

    Args:
        df (pd.DataFrame)
        col1 (str): the first column name
        col2 (str): the second column name
        alpha (float, optional): threshold, defaults to 0.05
    """
    is_normal1 = test_normality(df, col1, alpha)
    is_normal2 = test_normality(df, col2, alpha)

    type = ""
    result = ()

    if is_normal1[0] and is_normal2[0]:
        type = "Pearson"
        result = test_pearson(df[col1], df[col2])
    else:
        type = "Spearman"
        result = test_spearman(df[col1], df[col2])

    return (
        f"{is_normal1[1]}\n"
        f"{is_normal2[1]}\n"
        f"🎮 Coefficient de corrélation de {type}: {result[0]: .4f}\n"
        f"{interpret_pvalue_corr(result[1])}\n"
    )


def test_normality(df: pd.DataFrame, col: str, alpha=0.05) -> tuple:
    """
    Test the normality of data (Shapiro-Wilk)

    Args:
        df (pd.DataFrame)
        col (str): target column
        alpha (float, optional): threshold, defaults to 0.05

    Returns:
        bool: True means normal distribution.
    """
    values = df[col].dropna()  # have to add dropna() or there will be errors
    warning = ""
    if len(values) > 5000:
        values = values.sample(5000, random_state=42)
        warning = f"⚠️ Échantillonnage à 5000 observations (n original = {len(df[col].dropna())})"
    
    stat, p_value = shapiro(values)

    return (
        p_value > alpha,
        (
            f"🌈 Test de Shapiro-Wilk - {col} : stat = {stat: .4f}\n"
            f"{warning}\n"
            f"{interpret_pvalue_shapiro(p_value=p_value, alpha=alpha)}\n"
        )
    )


def test_pearson(series1: pd.Series, series2: pd.Series) -> tuple:
    """
    Pearson test (for normal distribution data)

    Args:
        series1 (pd.Series): the first data series
        series2 (pd.Series): the second data series

    Returns:
        tuple: (correlation, p_value)
    """
    return pearsonr(
        series1.dropna(), 
        series2.dropna()
    )  # have to add dropna() or there will be errors


def test_spearman(series1: pd.Series, series2: pd.Series) -> tuple:
    """
    Spearman test (for not normal distribution data)

    Args:
        series1 (pd.Series): the first data series
        series2 (pd.Series): the second data series

    Returns:
        tuple: (correlation, p_value)
    """
    return spearmanr(
        series1.dropna(),
        series2.dropna()
    )


# region Categorical (Quality-Quality)

def test_categorical(series1: pd.Series, series2: pd.Series, alpha=0.05):
    # could add more tests in the future
    chi2_stat, p_value, dof, expected  = test_chi2(series1, series2)

    return (
        f"{interpret_chi2(chi2_stat, dof, expected)}\n"
        f"{interpret_pvalue_corr(p_value=p_value, alpha=alpha)}\n"
    )


def test_chi2(series1: pd.Series, series2: pd.Series) -> tuple:
    """
    Chi-2 test

    Args:
        series1 (pd.Series): the first data series
        series2 (pd.Series): the second data series

    Returns:
        tuple: chi2_stat, p_value, dof, expected 
    """
    contingency_table = pd.crosstab(series1, series2)
    return chi2_contingency(contingency_table)


# region Mixed (Quantity-Quality)

def test_mixed(df: pd.DataFrame, col_category: str, col_value: str, alpha=0.05):
    # could add more tests in the future
    ((f_stat, p_value), eta) = test_anova(df=df, col_category=col_category, col_value=col_value)

    return (
        f"{interpret_anova(f_stat, p_value, alpha)}\n"
        f"{interpret_eta_squared(eta)}\n"
    )


def test_anova(df: pd.DataFrame, col_category: str, col_value: str) -> tuple:
    """
    ANOVA test

    Args:
        df (pd.DataFrame)
        col_category (str): the column name of target "category" (quality)
        col_value (str): the column name of target "value" (quantity)

    Returns:
        tuple: ((f_stat, p_value), eta_squared)
    """
    groups = [
        df.loc[df[col_category] == group][col_value].dropna() for group in df[col_category].unique()
    ]
    return (f_oneway(*groups), eta_squared_anova(*groups))


def eta_squared_anova(*groups):
    import numpy as np
    
    all_data = np.concatenate(groups)
    grand_mean = np.mean(all_data)
    
    # SS = sum of squares
    SS_total = np.sum((all_data - grand_mean) ** 2)
    
    SS_between = sum(
        len(g) * (np.mean(g) - grand_mean) ** 2
        for g in groups
    )
    
    return SS_between / SS_total


# region Interpretation

def interpret_normality(col: str, stat: float, p_value: float, alpha: float, warning: str = ""):
    return (
            f"🌈 Test de Shapiro-Wilk - {col} : stat = {stat: .4f}\n"
            f"{warning}\n"
            f"{interpret_pvalue_shapiro(p_value=p_value, alpha=alpha)}\n"
        )

def interpret_pvalue_shapiro(p_value, alpha=0.05):
    if p_value < alpha:
        return f"❌ Les données ne suivent pas une distribution normale : on rejette H0 (p={p_value:.2e} < {alpha})"
    else:
        return f"✅ Les données suivent une distribution normale : on ne rejette pas H0 (p={p_value:.2e} > {alpha})"


def interpret_pvalue_corr(p_value, alpha=0.05):
    """
    Interpret the p value for tests of correlation (Pearson, Spearman, Chi-2)

    Args:
        p_value (float): p value
        alpha (float, optional): threshold, defaults to 0.05

    Returns :
        str : interpretation
    """
    if p_value < alpha:
        return f"✅ Corrélation significative : on rejette H0 (p={p_value:.2e} < {alpha})\n"
    else:
        return f"❌ Pas de corrélation significative : on ne rejette pas H0 (p={p_value:.2e} > {alpha})\n"


def interpret_anova(f_stat, p_value, alpha=0.05):
    """
    Interpret the p value for ANOVA test

    Args:
        p_value (float): p value
        alpha (float, optional): threshold, defaults to 0.05

    Returns :
        str : interpretation
    """
    if p_value < alpha:
        result = f"✅ Différence significative entre les groupes : on rejette H0 (p={p_value:.2e} < {alpha})"
    else:
        result = f"❌ Pas de différence significative entre les groupes : on ne rejette pas H0 (p={p_value:.2e} > {alpha})"

    return (
        "🎹 Test de ANOVA\n"
        f"💭 Statistique de test F: {f_stat:.4f}\n"
        f"{result}\n"
    )

def interpret_chi2(chi2_stat, dof, expected):
    """
    Interpret the Chi-2 test

    Args:
        chi2_stat
        dof : degree of freedom
        expected : expected frequency

    Returns :
        str : interpretation
    """
    
    return (
        f"🧩 Statistique Chi-2: {chi2_stat: .4f}\n"
        f"🗽 Degrés de liberté: {dof}\n"
        "🌊 Fréquences attendues:\n"
        f"{expected}\n"
    )


def interpret_eta_squared(eta):
    """
    Interpret η² (eta squared)
    
    Args :
        eta (float) : valeur de η² (entre 0 et 1)
        
    Returns :
        str : interpretation
    """
    
    if eta < 0 or eta > 1:
        return "Valeur de η² invalide (doit être entre 0 et 1)"
    
    if eta < 0.01:
        return f"η²={eta:.4f} : Effet négligeable (pratiquement aucun impact)"
    elif eta < 0.06:
            return f"η²={eta:.4f} : Petit effet"
    elif eta < 0.14:
        return f"η²={eta:.4f} : Effet moyen"
    else:
        return f"η²={eta:.4f} : Grand effet (impact pratique fort)"


# region Checking

def is_numeric(series: pd.Series) -> bool:
    """
    Check if a series is numeric

    Args:
        series (pd.Series): target series

    Returns:
        bool: is_numeric
    """
    return pd.api.types.is_numeric_dtype(series)