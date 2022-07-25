import pandas as pd

def _mean(X:pd.Series) -> float:
    """
    Get mean value for XImputer class
    
    """
    return pd.Series(X).mean()

def _median(X:pd.Series) -> float:
    """
    Get median value for XImputer class
    
    """
    return pd.Series(X).median()

def _mode(X:pd.Series) -> float:
    """
    Get mode value for XImputer class
    
    """    
    return pd.Series(X).mode().values[0]

def _min(X:pd.Series) -> float:
    """
    Get min value for XImputer class
    
    """    
    return pd.Series(X).min()

def _max(X:pd.Series) -> float:
    """
    Get max value for XImputer class
    
    """    
    return pd.Series(X).max()