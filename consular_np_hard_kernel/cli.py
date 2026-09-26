"""Command Line Interface for Consular NP-Hard Kernel."""
import argparse
import sys
from .engine import ConsularNPHardEngine


def run_benchmark_all():
    engine = ConsularNPHardEngine()
    print("=" * 80)
    print("  CONSULAR NP-HARD KERNEL: 10 APEX EMBASSY & VISA SOLVERS BENCHMARK")
    print("=" * 80)

    results = engine.benchmark_all_10()
    solvers = results["solvers"]

    print(f"\n{'Solver ID & Name':<35} | {'Key Metric':<25} | {'Latency':<12}")
    print("-" * 80)
    for s_name, data in solvers.items():
        time_str = f"{data['time_us']:.1f} µs"
        primary_metric = [f"{k}={v}" for k, v in data.items() if k != 'time_us'][0]
        print(f"{s_name:<35} | {primary_metric:<25} | {time_str:<12}")

    print("-" * 80)
    print(f"Total Combined Pipeline Benchmark Execution: {results['total_benchmark_time_us']:.1f} µs")
    print("=" * 80)
    return results


def run_concierge_demo():
    engine = ConsularNPHardEngine()
    print("=" * 80)
    print("  APPLICANT CONCIERGE (VEEZA AI / TRAVEL DESK) HARNESS")
    print("=" * 80)
    suite = engine.generate_synthetic_benchmark_suite()

    # 1. Solvency
    res_solv = engine.concierge_adapter.audit_bank_solvency(*suite["p3_solvency"])
    print(f"[1] Bank Solvency Audit: daily_eur={res_solv.qualified_daily_eur_balance}€, "
          f"anomaly_ratio={res_solv.sudden_deposit_anomaly_ratio}, confidence={res_solv.solvency_confidence_score}/100 ({res_solv.execution_time_us} µs)")

    # 2. Jurisdiction Routing
    res_juris = engine.concierge_adapter.route_schengen_jurisdiction(*suite["p2_jurisdiction"])
    print(f"[2] Schengen Authority Router: competent_country={res_juris.competent_consulate_country}, "
          f"basis='{res_juris.legal_basis}', lead_time={res_juris.estimated_total_lead_time_days} days ({res_juris.execution_time_us} µs)")

    # 3. Dossier Packing
    res_dossier = engine.concierge_adapter.assemble_evidentiary_dossier(*suite["p6_dossier"])
    print(f"[3] Evidentiary Dossier Packing: docs={len(res_dossier.selected_documents)}, "
          f"pages={res_dossier.total_pages}, coverage={res_dossier.burdens_coverage_pct}%, all_met={res_dossier.all_burdens_met} ({res_dossier.execution_time_us} µs)")

    # 4. Rolling Stay
    res_stay = engine.concierge_adapter.optimize_rolling_stays(*suite["p8_stay"])
    print(f"[4] Schengen 90/180-Day Compliance: days={res_stay.total_days_spent}, "
          f"max_180_util={res_stay.max_rolling_180_utilization}/90, compliant={res_stay.legally_compliant} ({res_stay.execution_time_us} µs)")

    # 5. Sentinel Probe Scheduling
    res_probe = engine.concierge_adapter.schedule_appointment_sentinel_probes(*suite["p7_probe"])
    print(f"[5] Sentinel WAF Probes: scheduled={res_probe.total_probes_scheduled}, "
          f"expected_slots={res_probe.expected_slots_discovered}, ban_risk={res_probe.cumulative_ban_risk_pct}% ({res_probe.execution_time_us} µs)")
    print("=" * 80)


def run_consulate_demo():
    engine = ConsularNPHardEngine()
    print("=" * 80)
    print("  EMBASSY & CONSULAR OPERATIONS (MISSION & VAC DESK) HARNESS")
    print("=" * 80)
    suite = engine.generate_synthetic_benchmark_suite()

    # 1. Slot Allocation
    res_slot = engine.consular_adapter.allocate_slots_fairly(*suite["p1_slot"])
    print(f"[1] Anti-Scalper Slot Allocation: matched={res_slot.total_matched}, "
          f"family_intact={res_slot.family_bundles_preserved_pct}%, bots_quarantined={res_slot.bot_scalper_quarantined_count} ({res_slot.execution_time_us} µs)")

    # 2. Identity Resolution
    res_id = engine.consular_adapter.screen_watchlist_entities(suite["p4_identity"])
    print(f"[2] Identity Resolution & Watchlist Screen: clusters={len(res_id.clusters)}, "
          f"watchlist_hits={len(res_id.watchlist_matches)} ({res_id.execution_time_us} µs)")

    # 3. Delegation Scheduling
    res_group = engine.consular_adapter.schedule_delegation_intake(*suite["p5_group"])
    print(f"[3] Delegation & Family Flow: makespan={res_group.makespan_minutes}m, "
          f"family_splits={res_group.family_split_count}, precedence_ok={res_group.precedence_certified} ({res_group.execution_time_us} µs)")

    # 4. Officer Workload Balancing
    res_officer = engine.consular_adapter.balance_officer_workloads(*suite["p9_officer"])
    print(f"[4] Officer Interview Line Balancer: makespan={res_officer.makespan_minutes}m, "
          f"variance={res_officer.workload_variance}, mismatches={res_officer.skill_mismatches} ({res_officer.execution_time_us} µs)")

    # 5. Fraud Ring Detection
    res_fraud = engine.consular_adapter.detect_fraud_rings(*suite["p10_fraud"])
    print(f"[5] Covert Fraud Ring Detection: cliques={len(res_fraud.detected_fraud_cliques)}, "
          f"max_network={res_fraud.highest_risk_network_size}, flags={res_fraud.synthetic_identity_flag_count} ({res_fraud.execution_time_us} µs)")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(description="Consular NP-Hard Kernel CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("benchmark-all", help="Benchmark all 10 NP-hard Consular & Visa solvers")
    subparsers.add_parser("concierge-demo", help="Run Applicant Concierge (Veeza AI Consumer Flow) demo")
    subparsers.add_parser("consulate-demo", help="Run Embassy & Consular Operations (Mission Flow) demo")

    args = parser.parse_args()
    if args.command == "benchmark-all" or args.command is None:
        run_benchmark_all()
    elif args.command == "concierge-demo":
        run_concierge_demo()
    elif args.command == "consulate-demo":
        run_consulate_demo()


if __name__ == "__main__":
    main()
