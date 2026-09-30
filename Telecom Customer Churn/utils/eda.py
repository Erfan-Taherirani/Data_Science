"""
Utility functions for EDA.

functions:
    - describe_stats: Generate a compact statistical summary for a numeric feature.
"""
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def describe_stats(
    df: pd.DataFrame,
    feature: str,
    *,
    decimals: int = 3,
) -> pd.DataFrame:
    """
    Generate a compact statistical summary for a numeric feature.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataset.
    feature : str
        Name of the numeric feature to summarize.
    decimals : int, default=3
        Number of decimal places for numeric results.

    Returns
    -------
    pd.DataFrame
        Formatted statistical summary.
    """

    # Validate input
    if feature not in df.columns:
        raise KeyError(f"Feature '{feature}' not found in DataFrame.")

    if not pd.api.types.is_numeric_dtype(df[feature]):
        raise TypeError(
            f"Feature '{feature}' must be numeric. "
            f"Found dtype: {df[feature].dtype}"
        )

    # Extract feature
    s = df[feature]

    # Calculate statistics
    q1 = s.quantile(0.25)
    q3 = s.quantile(0.75)

    stats = {
        "Count": s.count(),
        "Missing": s.isna().sum(),
        "Unique": s.nunique(),

        "Mean": s.mean(),
        "Median": s.median(),
        "Std. Dev.": s.std(),
        "Variance": s.var(),

        "Min": s.min(),
        "Q1 (25%)": q1,
        "Q3 (75%)": q3,
        "Max": s.max(),

        "Range": s.max() - s.min(),
        "IQR": q3 - q1,

        "Skewness": s.skew(),
        "Kurtosis": s.kurt(),
    }

    # Convert to table
    result = pd.DataFrame(
        {
            "Statistic": stats.keys(),
            "Value": stats.values(),
        }
    )

    # Format output
    result["Value"] = result["Value"].apply(
        lambda x: (
            f"{x:,.{decimals}f}"
            if isinstance(x, (float, int))
            else x
        )
    )

    return result.set_index("Statistic")
