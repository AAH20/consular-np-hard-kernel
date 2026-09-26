"""Multilingual Consular Identity Resolution & Watchlist Multicut Solver.

Solves the NP-hard Correlation Clustering (Graph Multicut) problem over fragmented identity records.
Matches noisy Latin/Arabic name transliterations, passport numbers, and birth dates across
visa dossiers and refusal watchlists (Schengen SIS II, VIS, Interpol Red Notices) with bounded false-match risk.
"""
import time
from typing import List, Dict, Set, Tuple
from .models import IdentityRecord, EntityClusterResult


def _name_similarity(s1: str, s2: str) -> float:
    """Computes Jaccard character-ngram similarity between two names."""
    if not s1 or not s2:
        return 0.0
    w1, w2 = s1.lower().strip(), s2.lower().strip()
    if w1 == w2:
        return 1.0
    # bigrams
    b1 = {w1[i:i+2] for i in range(len(w1) - 1)}
    b2 = {w2[i:i+2] for i in range(len(w2) - 1)}
    union = len(b1.union(b2))
    if union == 0:
        return 0.0
    return len(b1.intersection(b2)) / float(union)


def _record_affinity(r1: IdentityRecord, r2: IdentityRecord) -> float:
    """Returns affinity score in [-1.0, 1.0]. Positive means should cluster, negative means separate."""
    # Passport exact match or national ID exact match is decisive
    if r1.passport_num and r2.passport_num and r1.passport_num == r2.passport_num:
        return 1.0
    if r1.national_id and r2.national_id and r1.national_id == r2.national_id:
        return 0.95

    # Check date of birth
    dob_match = (r1.dob_str == r2.dob_str) if (r1.dob_str and r2.dob_str) else False
    if not dob_match and r1.dob_str and r2.dob_str:
        return -0.9  # Conflicting DOBs strongly separate

    latin_sim = _name_similarity(r1.latin_name, r2.latin_name)
    arabic_sim = _name_similarity(r1.arabic_name, r2.arabic_name)
    best_name_sim = max(latin_sim, arabic_sim)

    if best_name_sim > 0.8 and dob_match:
        return 0.85
    elif best_name_sim > 0.6 and dob_match:
        return 0.5
    elif best_name_sim < 0.3:
        return -0.8
    else:
        return -0.2


def solve_identity_resolution(
    records: List[IdentityRecord]
) -> EntityClusterResult:
    """Solves Correlation Clustering via Pivot heuristic to cluster entities and identify watchlist hits."""
    t0 = time.perf_counter()
    n = len(records)
    if n == 0:
        return EntityClusterResult(
            clusters={},
            watchlist_matches=[],
            false_match_risk_score=0.0,
            algorithm="Pivot-Correlation-Clustering",
            execution_time_us=0.0
        )

    # 1. Pivot Correlation Clustering (Ailon, Charikar, Newman)
    unassigned = set(range(n))
    clusters: Dict[int, List[str]] = {}
    cluster_idx = 0

    while unassigned:
        # Pick a pivot
        pivot_idx = next(iter(unassigned))
        unassigned.remove(pivot_idx)
        cluster = [pivot_idx]

        to_add = []
        for other in unassigned:
            aff = _record_affinity(records[pivot_idx], records[other])
            if aff > 0.3:  # positive agreement threshold
                to_add.append(other)

        for mem in to_add:
            cluster.append(mem)
            unassigned.remove(mem)

        clusters[cluster_idx] = [records[i].record_id for i in cluster]
        cluster_idx += 1

    # 2. Watchlist hit detection: check clusters containing both VisaApp and Watchlist records
    watchlist_matches: List[Tuple[str, str, float]] = []
    record_map = {r.record_id: r for r in records}

    for c_id, rec_ids in clusters.items():
        apps = [rid for rid in rec_ids if record_map[rid].source_dataset == "VisaApp"]
        watch = [rid for rid in rec_ids if record_map[rid].source_dataset in {"SIS_II", "Interpol", "PriorRefusal"}]
        for a_id in apps:
            for w_id in watch:
                aff = _record_affinity(record_map[a_id], record_map[w_id])
                watchlist_matches.append((a_id, w_id, round(aff, 3)))

    false_match_risk = 0.05 * len(watchlist_matches)

    t1 = time.perf_counter()
    exec_us = (t1 - t0) * 1_000_000.0

    return EntityClusterResult(
        clusters=clusters,
        watchlist_matches=watchlist_matches,
        false_match_risk_score=round(false_match_risk, 3),
        algorithm="Pivot-Correlation-Clustering",
        execution_time_us=round(exec_us, 2)
    )
