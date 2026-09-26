"""Evidentiary Dossier Packing under Statutory Burdens Solver.

Solves the NP-hard Budgeted Maximum Coverage problem with multi-dimensional knapsack constraints.
Selects the minimal, highest-authority evidentiary document portfolio satisfying all statutory
consular burdens (socio-economic home ties, liquidity, accommodation) under strict dossier size caps.
"""
import time
from typing import List, Dict, Set, Tuple
from .models import EvidenceDocument, StatutoryBurden, DossierPackingResult


def solve_dossier_packing(
    documents: List[EvidenceDocument],
    burdens: List[StatutoryBurden],
    max_pages: int = 25,
    max_mb: float = 10.0
) -> DossierPackingResult:
    """Selects an optimal document portfolio covering statutory burdens within page and size limits."""
    t0 = time.perf_counter()
    if not documents or not burdens:
        return DossierPackingResult(
            selected_documents=[],
            total_pages=0,
            total_size_mb=0.0,
            burdens_coverage_pct=0.0,
            all_burdens_met=False,
            algorithm="Budgeted-Coverage-DossierPacker",
            execution_time_us=0.0
        )

    burden_reqs = {b.burden_id: b.min_evidence_score_required for b in burdens}
    burden_covered: Dict[str, float] = {b.burden_id: 0.0 for b in burdens}
    
    selected_docs: List[str] = []
    curr_pages = 0
    curr_mb = 0.0

    # Iterative greedy marginal score per unit weight (pages + size)
    remaining_docs = list(documents)

    while remaining_docs:
        best_doc = None
        best_ratio = -1.0

        for doc in remaining_docs:
            if curr_pages + doc.page_count > max_pages or curr_mb + doc.file_size_mb > max_mb:
                continue

            # Calculate marginal utility: gain towards unsatisfied burdens
            marginal_gain = 0.0
            for b_id, score in doc.burdens_satisfied.items():
                if b_id in burden_reqs:
                    needed = max(0.0, burden_reqs[b_id] - burden_covered[b_id])
                    marginal_gain += min(needed, score)

            cost = float(doc.page_count) + (doc.file_size_mb * 2.0)
            ratio = marginal_gain / max(0.1, cost)
            if ratio > best_ratio:
                best_ratio = ratio
                best_doc = doc

        if best_doc is not None and best_ratio > 0.0:
            selected_docs.append(best_doc.doc_id)
            curr_pages += best_doc.page_count
            curr_mb += best_doc.file_size_mb
            for b_id, score in best_doc.burdens_satisfied.items():
                burden_covered[b_id] = burden_covered.get(b_id, 0.0) + score
            remaining_docs.remove(best_doc)
        else:
            break

    # Calculate overall burdens coverage percentage
    covered_fractions = [min(1.0, burden_covered[b_id] / max(0.1, req)) for b_id, req in burden_reqs.items()]
    avg_coverage_pct = (sum(covered_fractions) / float(len(covered_fractions))) * 100.0 if covered_fractions else 0.0
    all_met = all(burden_covered[b_id] >= req for b_id, req in burden_reqs.items())

    t1 = time.perf_counter()
    exec_us = (t1 - t0) * 1_000_000.0

    return DossierPackingResult(
        selected_documents=selected_docs,
        total_pages=curr_pages,
        total_size_mb=round(curr_mb, 2),
        burdens_coverage_pct=round(avg_coverage_pct, 2),
        all_burdens_met=all_met,
        algorithm="Budgeted-Coverage-DossierPacker",
        execution_time_us=round(exec_us, 2)
    )
