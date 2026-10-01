"""Data loading and leak guard for FlakeFlagger dataset."""

import json
import pandas as pd
from pathlib import Path


# Columns that leak the label directly (computed from pass/fail history)
# These must be dropped before any model training
LEAKAGE_COLUMNS_LABEL_DERIVED = [
    'flakiness_score',
    'failure_rate',
    'pass_rate',
    'pass_rate_last_10_runs',
    'failure_rate_last_10_runs',
    'standard_deviation_of_pass_rate',
    'coefficient_of_variance',
    'times_flipped',
    'num_passing_tests',
    'num_failing_tests',
]

# Columns that assume future information (not available at decision time)
# These must be dropped before any model training
LEAKAGE_COLUMNS_FUTURE_INFO = [
    'future_passes_in_next_100_runs',
    'future_flakiness',
    'future_outcome',
]

# All leakage columns combined
ALL_LEAKAGE_COLUMNS = LEAKAGE_COLUMNS_LABEL_DERIVED + LEAKAGE_COLUMNS_FUTURE_INFO


def load_data(metadata_path: str, runs_path: str, join_key: str = 'test_id') -> pd.DataFrame:
    """
    Load FlakeFlagger dataset and apply leak guard.
    
    Args:
        metadata_path: Path to test metadata CSV
        runs_path: Path to test runs CSV
        join_key: Column name to join on (default: 'test_id')
    
    Returns:
        DataFrame with features + label, with leak guard applied
    """
    # Load CSVs
    metadata = pd.read_csv(metadata_path)
    runs = pd.read_csv(runs_path)
    
    # Join on test_id
    df = runs.merge(metadata, on=join_key, how='left')
    
    # Apply leak guard (drop leakage columns if they exist)
    leakage_found = [col for col in ALL_LEAKAGE_COLUMNS if col in df.columns]
    if leakage_found:
        print(f"WARNING: Dropping leakage columns: {leakage_found}")
        df = df.drop(columns=leakage_found)
    
    return df


def get_features_and_labels(df: pd.DataFrame, label_col: str = 'outcome') -> tuple:
    """
    Split DataFrame into features and labels.
    
    Args:
        df: DataFrame from load_data()
        label_col: Name of label column (default: 'outcome')
    
    Returns:
        (X, y) where X is feature DataFrame and y is label Series
    """
    # Separate label and features
    # Metadata columns (not features): test_id, project_id, timestamp, etc.
    metadata_cols = ['test_id', 'project_id', 'build_id', 'commit_sha', 'timestamp', 
                     'run_id', 'project', 'class', 'method']
    
    # Remove metadata and label from features
    feature_cols = [col for col in df.columns 
                   if col != label_col and col not in metadata_cols]
    
    X = df[feature_cols]
    y = df[label_col]
    
    return X, y


def exploratory_analysis(df: pd.DataFrame) -> dict:
    """
    Compute EDA statistics and return as dictionary.
    
    Args:
        df: DataFrame from load_data()
    
    Returns:
        Dictionary with shape, n_projects, label distribution, etc.
    """
    eda = {
        'n_rows': len(df),
        'n_columns': len(df.columns),
        'columns': df.columns.tolist(),
        'n_projects': df['project_id'].nunique() if 'project_id' in df.columns else 0,
        'n_tests': df['test_id'].nunique() if 'test_id' in df.columns else 0,
        'label_distribution': df['outcome'].value_counts().to_dict() if 'outcome' in df.columns else {},
    }
    
    # Compute positive rate (assume 'True' or 1 means flaky)
    if 'outcome' in df.columns:
        label_col = df['outcome']
        if label_col.dtype == bool:
            eda['positive_rate'] = label_col.sum() / len(label_col)
        elif label_col.dtype in [int, float]:
            eda['positive_rate'] = (label_col == 1).sum() / len(label_col)
        else:
            # String labels
            eda['positive_rate'] = (label_col == 'flaky').sum() / len(label_col)
    
    return eda
