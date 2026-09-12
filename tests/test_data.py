"""Tests for data loading and leak guard."""

import pandas as pd
import pytest
from ci_triage.data import (
    load_data, get_features_and_labels, exploratory_analysis,
    ALL_LEAKAGE_COLUMNS
)


def test_leak_guard_catches_label_derived_columns():
    """
    Critical test: If a leakage column (computed from label) appears in the data,
    the loader must remove it. This test fails when the guard is missing or bypassed.
    
    This test should outlive every model and every version of the loader.
    """
    # Create a toy DataFrame with a leakage column
    df_with_leak = pd.DataFrame({
        'test_id': [1, 2, 3],
        'project_id': ['proj_a', 'proj_a', 'proj_b'],
        'outcome': [True, False, True],  # Ground truth
        'failure_rate': [0.8, 0.1, 0.9],  # LEAKAGE: computed from outcome
        'duration': [100, 150, 120],  # Safe feature
    })
    
    # Save to temp CSV
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        df_with_leak.to_csv(f.name, index=False)
        temp_path = f.name
    
    # Create metadata CSV (minimal)
    metadata_df = pd.DataFrame({
        'test_id': [1, 2, 3],
        'project_id': ['proj_a', 'proj_a', 'proj_b'],
    })
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        metadata_df.to_csv(f.name, index=False)
        metadata_path = f.name
    
    # Load with leak guard
    df_loaded = load_data(temp_path, metadata_path, join_key='test_id')
    
    # Assert: failure_rate must be removed by the leak guard
    assert 'failure_rate' not in df_loaded.columns, \
        "Leak guard failed: 'failure_rate' (leakage column) was not removed!"
    
    # Cleanup
    import os
    os.unlink(temp_path)
    os.unlink(metadata_path)


def test_leak_guard_preserves_safe_columns():
    """
    Leak guard should remove leakage columns but preserve safe features.
    """
    df_with_mixed = pd.DataFrame({
        'test_id': [1, 2, 3],
        'project_id': ['proj_a', 'proj_a', 'proj_b'],
        'outcome': [True, False, True],
        'failure_rate': [0.8, 0.1, 0.9],  # LEAKAGE
        'duration': [100, 150, 120],  # SAFE
        'test_class': ['A', 'B', 'A'],  # SAFE
    })
    
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        df_with_mixed.to_csv(f.name, index=False)
        temp_path = f.name
    
    metadata_df = pd.DataFrame({
        'test_id': [1, 2, 3],
        'project_id': ['proj_a', 'proj_a', 'proj_b'],
    })
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        metadata_df.to_csv(f.name, index=False)
        metadata_path = f.name
    
    df_loaded = load_data(temp_path, metadata_path, join_key='test_id')
    
    # Leakage columns removed
    assert 'failure_rate' not in df_loaded.columns
    
    # Safe columns preserved
    assert 'duration' in df_loaded.columns
    assert 'test_class' in df_loaded.columns
    
    import os
    os.unlink(temp_path)
    os.unlink(metadata_path)


def test_get_features_and_labels():
    """
    Features and labels can be split correctly.
    """
    df = pd.DataFrame({
        'test_id': [1, 2, 3],
        'project_id': ['proj_a', 'proj_a', 'proj_b'],
        'outcome': [True, False, True],
        'duration': [100, 150, 120],
        'test_class': ['A', 'B', 'A'],
    })
    
    X, y = get_features_and_labels(df, label_col='outcome')
    
    # y should be the label
    assert len(y) == 3
    assert y.tolist() == [True, False, True]
    
    # X should have features but not label or metadata
    assert 'outcome' not in X.columns
    assert 'test_id' not in X.columns
    assert 'project_id' not in X.columns
    assert 'duration' in X.columns
    assert 'test_class' in X.columns


def test_exploratory_analysis():
    """
    EDA should compute shape, label distribution, and positive rate.
    """
    df = pd.DataFrame({
        'test_id': [1, 2, 3, 4],
        'project_id': ['proj_a', 'proj_a', 'proj_b', 'proj_b'],
        'outcome': [True, False, True, True],
        'duration': [100, 150, 120, 110],
    })
    
    eda = exploratory_analysis(df)
    
    assert eda['n_rows'] == 4
    assert eda['n_projects'] == 2
    assert eda['n_tests'] == 4
    assert eda['positive_rate'] == 0.75  # 3 out of 4 are True (flaky)
    assert eda['label_distribution'] == {True: 3, False: 1}


def test_leakage_columns_list_not_empty():
    """
    Sanity check: the leakage columns list should not be empty.
    If it is, we're not checking for anything.
    """
    assert len(ALL_LEAKAGE_COLUMNS) > 0, \
        "Leakage columns list is empty; leak guard cannot work!"


if __name__ == '__main__':
    test_leak_guard_catches_label_derived_columns()
    print("✓ test_leak_guard_catches_label_derived_columns passed")
    
    test_leak_guard_preserves_safe_columns()
    print("✓ test_leak_guard_preserves_safe_columns passed")
    
    test_get_features_and_labels()
    print("✓ test_get_features_and_labels passed")
    
    test_exploratory_analysis()
    print("✓ test_exploratory_analysis passed")
    
    test_leakage_columns_list_not_empty()
    print("✓ test_leakage_columns_list_not_empty passed")
    
    print("\nAll data tests passed!")
