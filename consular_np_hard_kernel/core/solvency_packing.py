"""Multi-Account Bank Statement Solvency & Anti-Fraud Proof Packing Solver.

Solves the constrained quadratic subset selection problem over banking assets.
Identifies the optimal combination of bank accounts meeting statutory daily solvency thresholds
while minimizing 'sudden deposit' variance anomalies that trigger consular fraud refusals.
"""
import math
import time
from typing import List, Tuple
from .models import AccountStatement, SolvencyPackingResult


def solve_solvency_packing(
    statements: List[AccountStatement],
    min_required_daily_eur: float = 100.0,
    trip_days: int = 14
) -> SolvencyPackingResult:
    """Selects optimal bank accounts minimizing sudden-deposit fraud suspicion while proving solvency."""
    t0 = time.perf_counter()
    if not statements or trip_days <= 0:
        return SolvencyPackingResult(
            selected_accounts=[],
            qualified_daily_eur_balance=0.0,
            sudden_deposit_anomaly_ratio=0.0,
            solvency_confidence_score=0.0,
            algorithm="Submodular-Solvency-Packer",
            execution_time_us=0.0
        )

    required_total_eur = min_required_daily_eur * trip_days
    evaluated_accounts = []

    for acc in statements:
        # Calculate organic vs sudden non-organic deposits
        organic_inflow = sum(tx.amount_eur for tx in acc.transactions if tx.is_salary_or_organic and tx.amount_eur > 0)
        sudden_inflow = sum(tx.amount_eur for tx in acc.transactions if not tx.is_salary_or_organic and tx.amount_eur > 0)
        
        # Anomaly ratio: sudden inflows relative to closing balance
        anomaly_ratio = (sudden_inflow / max(1.0, acc.closing_balance_eur)) if acc.closing_balance_eur > 0 else 1.0
        
        # Reliability penalty
        net_qualified_balance = max(0.0, acc.closing_balance_eur - sudden_inflow * 0.75)
        
        evaluated_accounts.append({
            "account_id": acc.account_id,
            "closing_balance": acc.closing_balance_eur,
            "qualified_balance": net_qualified_balance,
            "anomaly_ratio": anomaly_ratio,
            "organic_inflow": organic_inflow,
        })

    # Sort accounts by quality: highest qualified balance and lowest anomaly
    sorted_accs = sorted(
        evaluated_accounts,
        key=lambda a: (a["qualified_balance"] / max(0.1, 1.0 + a["anomaly_ratio"] * 2.0)),
        reverse=True
    )

    selected: List[str] = []
    accumulated_qualified = 0.0
    accumulated_sudden_ratio = 0.0

    for a in sorted_accs:
        selected.append(a["account_id"])
        accumulated_qualified += a["qualified_balance"]
        accumulated_sudden_ratio += a["anomaly_ratio"]
        if accumulated_qualified >= required_total_eur * 1.25:  # buffer of 25%
            break

    # If even all accounts cannot reach 1.25x, take all
    if accumulated_qualified < required_total_eur:
        for a in sorted_accs:
            if a["account_id"] not in selected:
                selected.append(a["account_id"])
                accumulated_qualified += a["qualified_balance"]
                accumulated_sudden_ratio += a["anomaly_ratio"]

    daily_eur = accumulated_qualified / float(trip_days)
    avg_anomaly = (accumulated_sudden_ratio / max(1, len(selected)))

    # Solvency confidence score 0 to 100
    solvency_ratio = min(2.0, daily_eur / max(1.0, min_required_daily_eur))
    cleanliness_factor = max(0.0, 1.0 - avg_anomaly)
    confidence_score = round(min(100.0, (solvency_ratio / 2.0 * 60.0) + (cleanliness_factor * 40.0)), 2)

    t1 = time.perf_counter()
    exec_us = (t1 - t0) * 1_000_000.0

    return SolvencyPackingResult(
        selected_accounts=selected,
        qualified_daily_eur_balance=round(daily_eur, 2),
        sudden_deposit_anomaly_ratio=round(avg_anomaly, 3),
        solvency_confidence_score=confidence_score,
        algorithm="Submodular-Solvency-Packer",
        execution_time_us=round(exec_us, 2)
    )
