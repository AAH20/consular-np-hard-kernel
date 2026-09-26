"""Consular Officer Skill-Constrained Interview Line Balancer Solver.

Solves the NP-hard Minimax Unrelated Parallel Machine Scheduling problem (R | eligibility | C_max).
Assigns complex visa interview queues across specialized consular officers matching linguistic proficiency,
visa authorization categories, and classified security clearance levels while balancing workloads.
"""
import time
from typing import List, Dict, Tuple
from .models import ConsularOfficer, InterviewCandidate, QueueBalanceResult


def solve_interview_line_balancing(
    officers: List[ConsularOfficer],
    candidates: List[InterviewCandidate]
) -> QueueBalanceResult:
    """Balances daily interview appointments across consular officers satisfying strict skill constraints."""
    t0 = time.perf_counter()
    if not officers or not candidates:
        return QueueBalanceResult(
            assignments={},
            makespan_minutes=0,
            workload_variance=0.0,
            skill_mismatches=0,
            algorithm="Minimax-Skill-Parallel-Scheduler",
            execution_time_us=0.0
        )

    assignments: Dict[str, List[str]] = {o.officer_id: [] for o in officers}
    officer_load: Dict[str, int] = {o.officer_id: 0 for o in officers}
    skill_mismatches = 0

    # Sort candidates by estimated duration descending (LPT heuristic)
    sorted_candidates = sorted(candidates, key=lambda c: c.estimated_duration_min, reverse=True)

    for cand in sorted_candidates:
        # Filter eligible officers
        eligible = []
        for o in officers:
            # Check language
            lang_ok = cand.primary_language in o.languages_spoken
            # Check visa authorization
            type_ok = cand.visa_type in o.authorized_visa_types
            # Check security clearance
            sec_ok = (not cand.requires_security_clearance) or o.has_security_clearance
            
            if lang_ok and type_ok and sec_ok:
                eligible.append(o)

        if eligible:
            # Assign to eligible officer with currently lowest load
            best_officer = min(eligible, key=lambda o: officer_load[o.officer_id])
        else:
            # Skill fallback: assign to least loaded officer overall, count mismatch
            best_officer = min(officers, key=lambda o: officer_load[o.officer_id])
            skill_mismatches += 1

        assignments[best_officer.officer_id].append(cand.candidate_id)
        officer_load[best_officer.officer_id] += cand.estimated_duration_min

    makespan = max(officer_load.values()) if officer_load else 0
    loads = list(officer_load.values())
    mean_load = sum(loads) / float(len(loads)) if loads else 0.0
    variance = (sum((l - mean_load) ** 2 for l in loads) / float(len(loads))) if loads else 0.0

    t1 = time.perf_counter()
    exec_us = (t1 - t0) * 1_000_000.0

    return QueueBalanceResult(
        assignments=assignments,
        makespan_minutes=makespan,
        workload_variance=round(variance, 2),
        skill_mismatches=skill_mismatches,
        algorithm="Minimax-Skill-Parallel-Scheduler",
        execution_time_us=round(exec_us, 2)
    )
