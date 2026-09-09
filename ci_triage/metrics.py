"""Evaluation metrics for CI triage system."""

import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_recall_fscore_support,
    brier_score_loss
)


# Phase 01 cost matrix: (predicted, actual) -> cost
COST_MATRIX = {
    ('flaky', 'flaky'): 0,
    ('genuine', 'genuine'): 0,
    ('infrastructure', 'infrastructure'): 0,
    ('genuine', 'flaky'): 600,  # predict genuine, actual flaky
    ('infrastructure', 'flaky'): 400,
    ('flaky', 'genuine'): 5000,  # predict flaky, actual genuine (catastrophic)
    ('infrastructure', 'genuine'): 400,
    ('flaky', 'infrastructure'): 400,
    ('genuine', 'infrastructure'): 600,
    ('abstain', 'flaky'): 700,
    ('abstain', 'genuine'): 700,
    ('abstain', 'infrastructure'): 700,
}


def cost_weighted_risk(y_true, y_pred, cost_matrix=COST_MATRIX):
    """Expected cost of predictions given cost matrix from phase 01."""
    # Convert to lists to ensure string-based dictionary lookup works
    y_true = [str(t) for t in y_true]
    y_pred = [str(p) for p in y_pred]
    
    costs = []
    for true_label, pred_label in zip(y_true, y_pred):
        # Look up cost; default to 0 if not found (shouldn't happen)
        cost = cost_matrix.get((pred_label, true_label), 0)
        costs.append(cost)
    return np.mean(costs)


def expected_calibration_error(y_true, y_prob, n_bins=10, binning='equal_width'):
    """ECE with selectable binning: equal_width or equal_frequency."""
    y_true = np.array(y_true, dtype=int)
    y_prob = np.array(y_prob)
    
    if binning == 'equal_width':
        bins = np.linspace(0, 1, n_bins + 1)
    elif binning == 'equal_frequency':
        bins = np.percentile(y_prob, np.linspace(0, 100, n_bins + 1))
    else:
        raise ValueError(f"Unknown binning: {binning}")
    
    ece = 0
    for i in range(len(bins) - 1):
        mask = (y_prob >= bins[i]) & (y_prob < bins[i + 1])
        if mask.sum() == 0:
            continue
        conf = y_prob[mask].mean()
        acc = y_true[mask].mean()
        ece += np.abs(conf - acc) * mask.sum() / len(y_true)
    
    return ece


def coverage_and_abstention(y_pred):
    """Fraction of cases that system decided vs. abstained."""
    y_pred = [str(p) for p in y_pred]
    n_abstain = sum(1 for p in y_pred if p == 'abstain')
    coverage = 1.0 - (n_abstain / len(y_pred))
    return coverage, n_abstain / len(y_pred)


def evaluate(y_true, y_pred, y_prob=None):
    """Compute full metric ladder."""
    # Ensure we're working with lists of strings
    y_true = [str(t) for t in y_true]
    y_pred = [str(p) for p in y_pred]
    
    results = {
        'cost_weighted_risk': cost_weighted_risk(y_true, y_pred),
    }
    
    # For accuracy and class metrics, filter out 'abstain' predictions
    y_true_filtered = [t for t, p in zip(y_true, y_pred) if p != 'abstain']
    y_pred_filtered = [p for p in y_pred if p != 'abstain']
    
    if y_pred_filtered:
        results['accuracy'] = accuracy_score(y_true_filtered, y_pred_filtered)
    else:
        results['accuracy'] = 0.0
    
    if y_prob is not None:
        y_prob = np.array(y_prob)
        # Binary: genuineon vs. rest
        y_true_binary = np.array([1 if t == 'genuine' else 0 for t in y_true])
        results['brier_score'] = brier_score_loss(y_true_binary, y_prob)
        results['ece_equal_width'] = expected_calibration_error(y_true_binary, y_prob, binning='equal_width')
        results['ece_equal_frequency'] = expected_calibration_error(y_true_binary, y_prob, binning='equal_frequency')
    
    # Class-level metrics (for classes present in y_true)
    classes = list(set(y_true))
    for cls in classes:
        y_true_binary = [1 if t == cls else 0 for t in y_true_filtered]
        y_pred_binary = [1 if p == cls else 0 for p in y_pred_filtered]
        if sum(y_true_binary) == 0:  # No samples of this class
            results[f'precision_{cls}'] = 0.0
            results[f'recall_{cls}'] = 0.0
            results[f'f1_{cls}'] = 0.0
        else:
            p, r, f1, _ = precision_recall_fscore_support(y_true_binary, y_pred_binary, average='binary', zero_division=0)
            results[f'precision_{cls}'] = float(p)
            results[f'recall_{cls}'] = float(r)
            results[f'f1_{cls}'] = float(f1)
    
    coverage, abstention = coverage_and_abstention(y_pred)
    results['coverage'] = coverage
    results['abstention_rate'] = abstention
    
    return results
