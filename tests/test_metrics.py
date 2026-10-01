"""Tests for CI triage metrics."""

import numpy as np
from ci_triage.metrics import evaluate, expected_calibration_error


def test_constant_predictor_trap():
    """
    The trap: a constant predictor "always not flaky" scores 94% accuracy
    on 3% genuine base rate, but catches zero genuine defects.
    This test asserts both high accuracy AND zero recall on genuine.
    """
    # Create toy data: 100 samples, ~3% are genuine, rest flaky/infra
    y_true = np.array(['flaky'] * 97 + ['genuine'] * 3)
    
    # Constant predictor: always predict 'flaky'
    y_pred = np.array(['flaky'] * 100)
    
    results = evaluate(y_true, y_pred)
    
    # High accuracy
    assert results['accuracy'] == 0.97, f"Expected 97% accuracy, got {results['accuracy']}"
    
    # Zero recall on genuine (we caught 0 genuine defects)
    assert results['recall_genuine'] == 0.0, f"Expected 0 recall on genuine, got {results['recall_genuine']}"
    
    # Cost-weighted risk should reflect the cost of missing genuine
    # 3% of genuine missed = 3% * 5000 = 150 per case (in expectation)
    assert results['cost_weighted_risk'] > 100, f"Expected high cost-weighted risk, got {results['cost_weighted_risk']}"


def test_ece_binning_difference():
    """
    On imbalanced data (3% positive), equal-width binning can produce
    misleading ECE (empty bins). Equal-frequency binning is more robust.
    """
    # Create imbalanced data: 97% negative, 3% positive
    y_true = np.array([0] * 97 + [1] * 3)
    
    # Probabilities: mostly low confidence, some high
    y_prob = np.array([0.1] * 50 + [0.5] * 47 + [0.9] * 3)
    
    ece_width = expected_calibration_error(y_true, y_prob, n_bins=10, binning='equal_width')
    ece_freq = expected_calibration_error(y_true, y_prob, n_bins=10, binning='equal_frequency')
    
    # Both should be floats
    assert isinstance(ece_width, (float, np.floating))
    assert isinstance(ece_freq, (float, np.floating))
    
    # On imbalanced data, equal-frequency should be more robust
    # (this is diagnostic; equal-width might have empty bins)
    print(f"ECE equal-width: {ece_width}")
    print(f"ECE equal-frequency: {ece_freq}")


def test_cost_matrix_applied():
    """
    Verify that cost matrix is correctly applied.
    Genuine prediction when actually flaky costs 600.
    Flaky prediction when actually genuine costs 5000.
    """
    y_true = np.array(['flaky', 'genuine', 'genuine', 'flaky'])
    y_pred = np.array(['genuine', 'genuine', 'flaky', 'flaky'])
    
    # Cost per sample: [600, 0, 5000, 0]
    # Mean cost: (600 + 0 + 5000 + 0) / 4 = 1400
    results = evaluate(y_true, y_pred)
    expected_cost = (600 + 0 + 5000 + 0) / 4
    assert results['cost_weighted_risk'] == expected_cost, \
        f"Expected {expected_cost}, got {results['cost_weighted_risk']}"


def test_abstention_cost():
    """
    Abstaining costs 700 per sample (engineer manual investigation).
    """
    y_true = np.array(['flaky', 'genuine', 'infrastructure'])
    y_pred = np.array(['abstain', 'abstain', 'abstain'])
    
    # Cost per sample: [700, 700, 700]
    # Mean cost: 700
    results = evaluate(y_true, y_pred)
    assert results['cost_weighted_risk'] == 700, \
        f"Expected 700, got {results['cost_weighted_risk']}"


def test_metric_returns_float():
    """
    Metrics should return floats, not raise exceptions.
    """
    y_true = np.array(['flaky', 'genuine', 'infrastructure'])
    y_pred = np.array(['flaky', 'genuine', 'infrastructure'])
    y_prob = np.array([0.1, 0.8, 0.05])
    
    results = evaluate(y_true, y_pred, y_prob)
    
    assert isinstance(results['cost_weighted_risk'], (float, np.floating))
    assert isinstance(results['accuracy'], (float, np.floating))
    assert isinstance(results['ece_equal_width'], (float, np.floating))
    assert isinstance(results['ece_equal_frequency'], (float, np.floating))


if __name__ == '__main__':
    test_constant_predictor_trap()
    print("✓ test_constant_predictor_trap passed")
    
    test_ece_binning_difference()
    print("✓ test_ece_binning_difference passed")
    
    test_cost_matrix_applied()
    print("✓ test_cost_matrix_applied passed")
    
    test_abstention_cost()
    print("✓ test_abstention_cost passed")
    
    test_metric_returns_float()
    print("✓ test_metric_returns_float passed")
    
    print("\nAll tests passed!")
