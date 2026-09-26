"""Covert Visa Fraud Ring & Shell Sponsor Graph Detection Solver.

Solves the NP-hard Attributed Subgraph Isomorphism and Maximal Clique Enumeration problem.
Identifies coordinated visa fraud syndicates, synthetic identity farms, and shell employer sponsor rings
by detecting dense attribute-sharing subgraphs across thousands of visa filings.
"""
import time
from typing import List, Dict, Set, Tuple
from .models import VisaApplicationNode, SponsorEdge, FraudRingResult


def solve_fraud_ring_detection(
    nodes: List[VisaApplicationNode],
    edges: List[SponsorEdge],
    min_clique_size: int = 3
) -> FraudRingResult:
    """Discovers dense fraud rings and shell sponsor networks via Bron-Kerbosch maximal clique enumeration."""
    t0 = time.perf_counter()
    if not nodes:
        return FraudRingResult(
            detected_fraud_cliques=[],
            highest_risk_network_size=0,
            synthetic_identity_flag_count=0,
            algorithm="Bron-Kerbosch-Fraud-Clique",
            execution_time_us=0.0
        )

    # Build adjacency graph
    adj: Dict[str, Set[str]] = {n.app_id: set() for n in nodes}
    for e in edges:
        if e.source_app_id in adj and e.target_app_id in adj:
            adj[e.source_app_id].add(e.target_app_id)
            adj[e.target_app_id].add(e.source_app_id)

    # Also infer implicit edges from identical suspicious attributes
    tax_groups: Dict[str, List[str]] = {}
    hotel_groups: Dict[str, List[str]] = {}
    for n in nodes:
        if n.employer_tax_id:
            tax_groups.setdefault(n.employer_tax_id, []).append(n.app_id)
        if n.hotel_booking_ref:
            hotel_groups.setdefault(n.hotel_booking_ref, []).append(n.app_id)

    for group in tax_groups.values():
        if len(group) > 1:
            for i in range(len(group)):
                for j in range(i + 1, len(group)):
                    adj[group[i]].add(group[j])
                    adj[group[j]].add(group[i])

    for group in hotel_groups.values():
        if len(group) > 1:
            for i in range(len(group)):
                for j in range(i + 1, len(group)):
                    adj[group[i]].add(group[j])
                    adj[group[j]].add(group[i])

    # Bron-Kerbosch algorithm for maximal cliques
    cliques: List[List[str]] = []

    def bron_kerbosch(r: Set[str], p: Set[str], x: Set[str]):
        if not p and not x:
            if len(r) >= min_clique_size:
                cliques.append(sorted(list(r)))
            return
        
        # Choose pivot u in P union X maximizing |P intersection N(u)|
        u = next(iter(p.union(x)))
        for v in list(p - adj.get(u, set())):
            bron_kerbosch(r.union({v}), p.intersection(adj.get(v, set())), x.intersection(adj.get(v, set())))
            p.remove(v)
            x.add(v)

    all_nodes = set(adj.keys())
    bron_kerbosch(set(), all_nodes, set())

    # Sort cliques by size descending
    cliques.sort(key=len, reverse=True)
    max_network_size = len(cliques[0]) if cliques else 0
    flag_count = sum(len(c) for c in cliques)

    t1 = time.perf_counter()
    exec_us = (t1 - t0) * 1_000_000.0

    return FraudRingResult(
        detected_fraud_cliques=cliques,
        highest_risk_network_size=max_network_size,
        synthetic_identity_flag_count=flag_count,
        algorithm="Bron-Kerbosch-Fraud-Clique",
        execution_time_us=round(exec_us, 2)
    )
