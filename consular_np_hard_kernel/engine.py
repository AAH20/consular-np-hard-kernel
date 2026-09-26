"""Unified Engine for the 10 Apex NP-Hard Problems in Consular Logistics and Visa Systems."""
import time
from typing import Dict, Any, List, Tuple

from .core.models import (
    ApplicantRequest,
    ConsularSlot,
    TravelLeg,
    CountryRule,
    AccountStatement,
    BankTransaction,
    IdentityRecord,
    ApplicantTask,
    BiometricStation,
    EvidenceDocument,
    StatutoryBurden,
    ConsularEndpoint,
    ProxyNode,
    HistoricalStay,
    ProposedTrip,
    ConsularOfficer,
    InterviewCandidate,
    VisaApplicationNode,
    SponsorEdge,
)
from .core.slot_allocation import solve_slot_allocation
from .core.jurisdiction_routing import solve_jurisdiction_routing
from .core.solvency_packing import solve_solvency_packing
from .core.identity_resolution import solve_identity_resolution
from .core.group_scheduling import solve_group_interview_scheduling
from .core.dossier_packing import solve_dossier_packing
from .core.probe_scheduling import solve_probe_scheduling
from .core.rolling_stay import solve_rolling_stay_optimization
from .core.officer_balancing import solve_interview_line_balancing
from .core.fraud_detection import solve_fraud_ring_detection

from .adapters.applicant_concierge import ApplicantConciergeAdapter
from .adapters.embassy_consular_ops import EmbassyConsularOpsAdapter


class ConsularNPHardEngine:
    """Unified engine coordinating NP-hard solvers across Consular Logistics, Embassies, and Visas."""

    def __init__(self):
        self.concierge_adapter = ApplicantConciergeAdapter()
        self.consular_adapter = EmbassyConsularOpsAdapter()

    # --- Core Direct Solvers ---
    solve_slot_allocation = staticmethod(solve_slot_allocation)
    solve_jurisdiction_routing = staticmethod(solve_jurisdiction_routing)
    solve_solvency_packing = staticmethod(solve_solvency_packing)
    solve_identity_resolution = staticmethod(solve_identity_resolution)
    solve_group_scheduling = staticmethod(solve_group_interview_scheduling)
    solve_dossier_packing = staticmethod(solve_dossier_packing)
    solve_probe_scheduling = staticmethod(solve_probe_scheduling)
    solve_rolling_stay = staticmethod(solve_rolling_stay_optimization)
    solve_officer_balancing = staticmethod(solve_interview_line_balancing)
    solve_fraud_detection = staticmethod(solve_fraud_ring_detection)

    @staticmethod
    def generate_synthetic_benchmark_suite() -> Dict[str, Any]:
        """Generates realistic synthetic benchmark problem instances for all 10 NP-hard challenges."""
        # 1. Slot Allocation: 20 applicants including family groups and bot anomalies
        requests = [
            ApplicantRequest("req_1", "Ahmed Hassan", "fam_1", "Schengen-Tourist", 85.0, ["2026-10-15", "2026-10-16"]),
            ApplicantRequest("req_2", "Fatima Hassan", "fam_1", "Schengen-Tourist", 85.0, ["2026-10-15", "2026-10-16"]),
            ApplicantRequest("req_3", "Omar Hassan", "fam_1", "Schengen-Tourist", 85.0, ["2026-10-15", "2026-10-16"]),
            ApplicantRequest("req_4", "Youssef Ali", "solo", "US-B1/B2", 90.0, ["2026-10-15"]),
            ApplicantRequest("req_5", "Mona Ibrahim", "solo", "Schengen-Tourist", 70.0, ["2026-10-17"]),
            ApplicantRequest("req_bot_1", "Bot Alpha", "solo", "Schengen-Tourist", 9999.0, ["2026-10-15"]),
        ]
        slots = [
            ConsularSlot("slot_1", "CAI-DEU", "2026-10-15", "09:00-10:00", 4, ["Schengen-Tourist", "US-B1/B2"]),
            ConsularSlot("slot_2", "CAI-DEU", "2026-10-16", "10:00-11:00", 2, ["Schengen-Tourist"]),
            ConsularSlot("slot_3", "ALX-FRA", "2026-10-17", "09:00-10:00", 3, ["Schengen-Tourist"]),
        ]

        # 2. Jurisdiction Routing: Multi-city European itinerary
        legs = [
            TravelLeg("leg_1", "FR", duration_days=3, entry_order=1),
            TravelLeg("leg_2", "DE", duration_days=7, entry_order=2),
            TravelLeg("leg_3", "IT", duration_days=4, entry_order=3),
        ]
        rules = [
            CountryRule("FR", min_processing_days=15, visa_fee_eur=90.0, historical_refusal_rate_pct=16.5, appointment_wait_days=45),
            CountryRule("DE", min_processing_days=10, visa_fee_eur=90.0, historical_refusal_rate_pct=12.0, appointment_wait_days=20),
            CountryRule("IT", min_processing_days=20, visa_fee_eur=90.0, historical_refusal_rate_pct=18.0, appointment_wait_days=60),
        ]

        # 3. Solvency Packing: 3 accounts with varying organic cash flows
        accs = [
            AccountStatement("acc_cib", "CIB Egypt", "EGP", closing_balance_eur=4500.0, transactions=[
                BankTransaction("tx_1", 30, 1500.0, True, "Salary Deposit"),
                BankTransaction("tx_2", 60, 1500.0, True, "Salary Deposit"),
                BankTransaction("tx_3", 5, 200.0, False, "ATM Deposit"),
            ]),
            AccountStatement("acc_hsbc", "HSBC Premier", "USD", closing_balance_eur=8000.0, transactions=[
                BankTransaction("tx_4", 10, 5000.0, False, "Sudden Broker Transfer"),  # Anomaly!
            ]),
        ]

        # 4. Identity Resolution: records across visa app and watchlists
        identities = [
            IdentityRecord("rec_1", "Mohamed El-Sayed", "محمد السيد", "A12345678", "1988-04-12", "28804120101", "VisaApp"),
            IdentityRecord("rec_2", "Mohammed Elsayed", "محمد السيد", "A12345678", "1988-04-12", "28804120101", "VisaApp"),
            IdentityRecord("rec_3", "Mohamed Al-Sayed", "محمد السيد", "B99999999", "1988-04-12", "28804120101", "SIS_II"),
            IdentityRecord("rec_4", "Tarek Mansour", "طارق منصور", "C55555555", "1992-09-01", "29209010202", "VisaApp"),
        ]

        # 5. Group Scheduling: Family of 3 doing biometrics and interview
        tasks = [
            ApplicantTask("task_bio_1", "p1", "fam_1", "Biometric", duration_min=10),
            ApplicantTask("task_bio_2", "p2", "fam_1", "Biometric", duration_min=10),
            ApplicantTask("task_int_1", "p1", "fam_1", "Interview", duration_min=15, depends_on_task="task_bio_1"),
            ApplicantTask("task_int_2", "p2", "fam_1", "Interview", duration_min=15, depends_on_task="task_bio_2"),
        ]
        stations = [
            BiometricStation("st_bio_1", "Biometric"),
            BiometricStation("st_bio_2", "Biometric"),
            BiometricStation("st_int_1", "Interview"),
        ]

        # 6. Dossier Packing: Evidence documents and statutory burdens
        burdens = [
            StatutoryBurden("b_ties", "Socio-Economic Home Ties", min_evidence_score_required=70.0),
            StatutoryBurden("b_solv", "Financial Solvency", min_evidence_score_required=60.0),
            StatutoryBurden("b_itin", "Itinerary Coherence", min_evidence_score_required=50.0),
        ]
        docs = [
            EvidenceDocument("doc_hr", "HR Employment Letter", page_count=2, file_size_mb=0.8, burdens_satisfied={"b_ties": 50.0}),
            EvidenceDocument("doc_bank", "6-Month Certified Bank Statement", page_count=6, file_size_mb=2.5, burdens_satisfied={"b_solv": 80.0, "b_ties": 20.0}),
            EvidenceDocument("doc_deed", "Real Estate Ownership Title", page_count=3, file_size_mb=1.2, burdens_satisfied={"b_ties": 40.0}),
            EvidenceDocument("doc_itin", "Detailed Travel Plan & Flight Ticket", page_count=4, file_size_mb=1.5, burdens_satisfied={"b_itin": 60.0}),
        ]

        # 7. Probe Scheduling: 2 portals and 3 proxies
        endpoints = [
            ConsularEndpoint("ep_vfs_deu", "VFS_Cairo_Germany", rate_limit_rpm=6, ban_risk_weight=2.0, expected_slot_drop_probability=0.8),
            ConsularEndpoint("ep_tls_fra", "TLS_Alexandria_France", rate_limit_rpm=4, ban_risk_weight=3.0, expected_slot_drop_probability=0.6),
        ]
        proxies = [
            ProxyNode("prx_1", "197.38.10.x", latency_ms=45.0, cooldown_seconds=2.0),
            ProxyNode("prx_2", "197.38.20.x", latency_ms=52.0, cooldown_seconds=2.0),
            ProxyNode("prx_3", "197.38.30.x", latency_ms=48.0, cooldown_seconds=2.0),
        ]

        # 8. Rolling Stay: Historical stays and proposed trips
        history = [
            HistoricalStay(entry_day=10, exit_day=35),  # 26 days
            HistoricalStay(entry_day=80, exit_day=110), # 31 days
        ]
        proposed = [
            ProposedTrip("trip_summer", preferred_entry_day=150, desired_duration_days=25, min_acceptable_duration_days=15, value_weight=100.0),
            ProposedTrip("trip_autumn", preferred_entry_day=220, desired_duration_days=30, min_acceptable_duration_days=20, value_weight=80.0),
        ]

        # 9. Officer Balancing: 3 officers with varying skills and 5 candidates
        officers = [
            ConsularOfficer("off_1", ["Arabic", "English"], ["Schengen-Tourist", "US-B1/B2"], has_security_clearance=False),
            ConsularOfficer("off_2", ["Arabic", "French", "English"], ["Schengen-Tourist", "Immigrant"], has_security_clearance=True),
        ]
        candidates = [
            InterviewCandidate("cand_1", "Schengen-Tourist", "Arabic", 15),
            InterviewCandidate("cand_2", "Immigrant", "Arabic", 30, requires_security_clearance=True),
            InterviewCandidate("cand_3", "Schengen-Tourist", "English", 15),
            InterviewCandidate("cand_4", "Schengen-Tourist", "French", 20),
        ]

        # 10. Fraud Ring Detection: 5 applications with suspicious shared attributes
        apps = [
            VisaApplicationNode("app_1", "Applicant 1", "TAX_SHELL_99", "HOTEL_FAKE_123", "B_CAIRO_01", 1700000000.0),
            VisaApplicationNode("app_2", "Applicant 2", "TAX_SHELL_99", "HOTEL_FAKE_123", "B_CAIRO_01", 1700000100.0),
            VisaApplicationNode("app_3", "Applicant 3", "TAX_SHELL_99", "HOTEL_FAKE_123", "B_CAIRO_02", 1700000200.0),
            VisaApplicationNode("app_4", "Applicant 4", "TAX_LEGIT_11", "HOTEL_REAL_456", "B_ALEX_05", 1700000300.0),
        ]
        edges = [
            SponsorEdge("app_1", "app_2", "TaxID", "TAX_SHELL_99"),
            SponsorEdge("app_2", "app_3", "TaxID", "TAX_SHELL_99"),
            SponsorEdge("app_1", "app_3", "HotelRef", "HOTEL_FAKE_123"),
        ]

        return {
            "p1_slot": (requests, slots),
            "p2_jurisdiction": (legs, rules),
            "p3_solvency": (accs, 100.0, 14),
            "p4_identity": identities,
            "p5_group": (tasks, stations),
            "p6_dossier": (docs, burdens, 20, 8.0),
            "p7_probe": (endpoints, proxies, 120.0),
            "p8_stay": (history, proposed),
            "p9_officer": (officers, candidates),
            "p10_fraud": (apps, edges, 3),
        }

    def benchmark_all_10(self) -> Dict[str, Any]:
        """Executes and benchmarks all 10 NP-hard Consular & Visa solvers in a single run."""
        suite = self.generate_synthetic_benchmark_suite()
        t_start_total = time.perf_counter()

        res_p1 = self.solve_slot_allocation(*suite["p1_slot"])
        res_p2 = self.solve_jurisdiction_routing(*suite["p2_jurisdiction"])
        res_p3 = self.solve_solvency_packing(*suite["p3_solvency"])
        res_p4 = self.solve_identity_resolution(suite["p4_identity"])
        res_p5 = self.solve_group_scheduling(*suite["p5_group"])
        res_p6 = self.solve_dossier_packing(*suite["p6_dossier"])
        res_p7 = self.solve_probe_scheduling(*suite["p7_probe"])
        res_p8 = self.solve_rolling_stay(*suite["p8_stay"])
        res_p9 = self.solve_officer_balancing(*suite["p9_officer"])
        res_p10 = self.solve_fraud_detection(*suite["p10_fraud"])

        t_end_total = time.perf_counter()
        total_time_us = (t_end_total - t_start_total) * 1_000_000.0

        return {
            "total_benchmark_time_us": round(total_time_us, 2),
            "solvers": {
                "P1_Slot_Allocation_HR_C": {
                    "matched_count": res_p1.total_matched,
                    "family_bundles_pct": res_p1.family_bundles_preserved_pct,
                    "time_us": res_p1.execution_time_us,
                },
                "P2_Jurisdiction_Routing_Art5": {
                    "competent_country": res_p2.competent_consulate_country,
                    "lead_time_days": res_p2.estimated_total_lead_time_days,
                    "time_us": res_p2.execution_time_us,
                },
                "P3_Solvency_Proof_Packing": {
                    "daily_eur": res_p3.qualified_daily_eur_balance,
                    "confidence_score": res_p3.solvency_confidence_score,
                    "time_us": res_p3.execution_time_us,
                },
                "P4_Identity_Resolution_Multicut": {
                    "clusters": len(res_p4.clusters),
                    "watchlist_matches": len(res_p4.watchlist_matches),
                    "time_us": res_p4.execution_time_us,
                },
                "P5_Group_Interview_Scheduler": {
                    "makespan_min": res_p5.makespan_minutes,
                    "precedence_ok": res_p5.precedence_certified,
                    "time_us": res_p5.execution_time_us,
                },
                "P6_Dossier_Packing_Coverage": {
                    "pages": res_p6.total_pages,
                    "all_burdens_met": res_p6.all_burdens_met,
                    "time_us": res_p6.execution_time_us,
                },
                "P7_Probe_Scheduler_Anti_WAF": {
                    "probes_scheduled": res_p7.total_probes_scheduled,
                    "ban_risk_pct": res_p7.cumulative_ban_risk_pct,
                    "time_us": res_p7.execution_time_us,
                },
                "P8_Rolling_Stay_90_180": {
                    "total_days": res_p8.total_days_spent,
                    "compliant": res_p8.legally_compliant,
                    "time_us": res_p8.execution_time_us,
                },
                "P9_Officer_Workload_Balancer": {
                    "makespan_min": res_p9.makespan_minutes,
                    "skill_mismatches": res_p9.skill_mismatches,
                    "time_us": res_p9.execution_time_us,
                },
                "P10_Fraud_Ring_Clique_Detector": {
                    "fraud_cliques_found": len(res_p10.detected_fraud_cliques),
                    "max_ring_size": res_p10.highest_risk_network_size,
                    "time_us": res_p10.execution_time_us,
                },
            }
        }
