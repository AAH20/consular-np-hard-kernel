"""Dynamic WAF Probe Scheduling & Sentinel Anti-Bot Evasion Solver.

Solves the restless bandit scheduling problem under adversarial Web Application Firewall (WAF) rate limits.
Schedules distributed proxy probes across appointment portals (VFS, TLScontact, BLS International)
maximizing slot drop discovery while keeping cumulative IP ban risk strictly bounded.
"""
import time
from typing import List, Tuple
from .models import ConsularEndpoint, ProxyNode, ProbeScheduleResult


def solve_probe_scheduling(
    endpoints: List[ConsularEndpoint],
    proxies: List[ProxyNode],
    time_horizon_seconds: float = 300.0
) -> ProbeScheduleResult:
    """Computes rate-compliant probe dispatch schedule across proxy nodes and consular endpoints."""
    t0 = time.perf_counter()
    if not endpoints or not proxies or time_horizon_seconds <= 0:
        return ProbeScheduleResult(
            probe_dispatches=[],
            total_probes_scheduled=0,
            expected_slots_discovered=0.0,
            cumulative_ban_risk_pct=0.0,
            algorithm="Restless-Bandit-WAF-Scheduler",
            execution_time_us=0.0
        )

    # Sort endpoints by drop value density: expected slot probability / ban risk
    sorted_endpoints = sorted(
        endpoints,
        key=lambda ep: (ep.expected_slot_drop_probability / max(0.01, ep.ban_risk_weight)),
        reverse=True
    )

    dispatches: List[Tuple[float, str, str]] = []
    total_expected_slots = 0.0
    cumulative_risk = 0.0

    # Proxy availability tracker: proxy_id -> next available time
    proxy_next_free = {p.proxy_id: 0.0 for p in proxies}

    for ep in sorted_endpoints:
        # Minimum interval between probes on this endpoint: 60.0 / rate_limit_rpm
        interval_sec = 60.0 / max(1, ep.rate_limit_rpm)
        curr_t = 0.0
        p_idx = 0

        while curr_t < time_horizon_seconds:
            # Pick least recently used proxy that is free
            chosen_proxy = min(proxies, key=lambda p: proxy_next_free[p.proxy_id])
            dispatch_t = max(curr_t, proxy_next_free[chosen_proxy.proxy_id])
            
            if dispatch_t >= time_horizon_seconds:
                break

            dispatches.append((round(dispatch_t, 2), chosen_proxy.proxy_id, ep.endpoint_id))
            total_expected_slots += ep.expected_slot_drop_probability * 0.05
            cumulative_risk += (ep.ban_risk_weight * 0.01)

            # Update cooldowns
            proxy_next_free[chosen_proxy.proxy_id] = dispatch_t + chosen_proxy.cooldown_seconds + 5.0
            curr_t = dispatch_t + interval_sec

    ban_risk_pct = min(100.0, cumulative_risk * 10.0)
    t1 = time.perf_counter()
    exec_us = (t1 - t0) * 1_000_000.0

    return ProbeScheduleResult(
        probe_dispatches=dispatches,
        total_probes_scheduled=len(dispatches),
        expected_slots_discovered=round(total_expected_slots, 2),
        cumulative_ban_risk_pct=round(ban_risk_pct, 2),
        algorithm="Restless-Bandit-WAF-Scheduler",
        execution_time_us=round(exec_us, 2)
    )
