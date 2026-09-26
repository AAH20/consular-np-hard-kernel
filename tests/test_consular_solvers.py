"""Comprehensive Test Suite for all 10 Apex Consular & Visa NP-Hard Solvers."""
import unittest
from consular_np_hard_kernel.core.models import (
    ApplicantRequest, ConsularSlot, TravelLeg, CountryRule,
    AccountStatement, BankTransaction, IdentityRecord,
    ApplicantTask, BiometricStation, EvidenceDocument, StatutoryBurden,
    ConsularEndpoint, ProxyNode, HistoricalStay, ProposedTrip,
    ConsularOfficer, InterviewCandidate, VisaApplicationNode, SponsorEdge
)
from consular_np_hard_kernel.core.slot_allocation import solve_slot_allocation
from consular_np_hard_kernel.core.jurisdiction_routing import solve_jurisdiction_routing
from consular_np_hard_kernel.core.solvency_packing import solve_solvency_packing
from consular_np_hard_kernel.core.identity_resolution import solve_identity_resolution
from consular_np_hard_kernel.core.group_scheduling import solve_group_interview_scheduling
from consular_np_hard_kernel.core.dossier_packing import solve_dossier_packing
from consular_np_hard_kernel.core.probe_scheduling import solve_probe_scheduling
from consular_np_hard_kernel.core.rolling_stay import solve_rolling_stay_optimization
from consular_np_hard_kernel.core.officer_balancing import solve_interview_line_balancing
from consular_np_hard_kernel.core.fraud_detection import solve_fraud_ring_detection
from consular_np_hard_kernel.engine import ConsularNPHardEngine


class TestConsularNPHardKernel(unittest.TestCase):

    def test_p1_slot_allocation(self):
        reqs = [
            ApplicantRequest("r1", "Parent", "fam_1", "Schengen-Tourist", 90.0, ["2026-10-15"]),
            ApplicantRequest("r2", "Child", "fam_1", "Schengen-Tourist", 90.0, ["2026-10-15"]),
            ApplicantRequest("r_bot", "Bot 1", "solo", "Schengen-Tourist", 10000.0, ["2026-10-15"]),
        ]
        slots = [
            ConsularSlot("s1", "CAI-DEU", "2026-10-15", "09:00", 2, ["Schengen-Tourist"]),
        ]
        res = solve_slot_allocation(reqs, slots)
        self.assertEqual(res.total_matched, 2)
        self.assertEqual(res.bot_scalper_quarantined_count, 1)
        self.assertEqual(res.matched_slots["r1"], "s1")
        self.assertEqual(res.matched_slots["r2"], "s1")

    def test_p2_jurisdiction_routing(self):
        legs = [
            TravelLeg("l1", "FR", duration_days=4, entry_order=1),
            TravelLeg("l2", "IT", duration_days=6, entry_order=2),
        ]
        rules = [
            CountryRule("FR", 15, 90.0, 16.0, 30),
            CountryRule("IT", 10, 90.0, 12.0, 20),
        ]
        res = solve_jurisdiction_routing(legs, rules)
        self.assertEqual(res.competent_consulate_country, "IT")
        self.assertTrue(res.itinerary_compliant)
        self.assertGreater(res.estimated_total_lead_time_days, 0)

    def test_p3_solvency_packing(self):
        accs = [
            AccountStatement("acc1", "Bank A", "EGP", 5000.0, [
                BankTransaction("t1", 30, 2000.0, True, "Salary"),
            ]),
            AccountStatement("acc2", "Bank B", "USD", 10000.0, [
                BankTransaction("t2", 5, 8000.0, False, "Suspicious Transfer"),
            ]),
        ]
        res = solve_solvency_packing(accs, min_required_daily_eur=100.0, trip_days=10)
        self.assertIn("acc1", res.selected_accounts)
        self.assertGreater(res.solvency_confidence_score, 0.0)

    def test_p4_identity_resolution(self):
        recs = [
            IdentityRecord("id1", "Omar Farouk", "عمر فاروق", "P12345", "1990-01-01", "N1", "VisaApp"),
            IdentityRecord("id2", "Omer Faruk", "عمر فاروق", "P12345", "1990-01-01", "N1", "VisaApp"),
            IdentityRecord("id3", "Omar Farouk", "عمر فاروق", "P12345", "1990-01-01", "N1", "SIS_II"),
        ]
        res = solve_identity_resolution(recs)
        self.assertEqual(len(res.clusters), 1)
        self.assertEqual(len(res.watchlist_matches), 2)

    def test_p5_group_scheduling(self):
        tasks = [
            ApplicantTask("t1", "a1", "f1", "Biometric", 10),
            ApplicantTask("t2", "a1", "f1", "Interview", 15, depends_on_task="t1"),
        ]
        stations = [
            BiometricStation("st1", "Biometric"),
            BiometricStation("st2", "Interview"),
        ]
        res = solve_group_interview_scheduling(tasks, stations)
        self.assertTrue(res.precedence_certified)
        self.assertGreater(res.makespan_minutes, 0)

    def test_p6_dossier_packing(self):
        burdens = [
            StatutoryBurden("b1", "Ties", 50.0),
            StatutoryBurden("b2", "Solvency", 50.0),
        ]
        docs = [
            EvidenceDocument("d1", "Doc 1", page_count=5, file_size_mb=2.0, burdens_satisfied={"b1": 60.0}),
            EvidenceDocument("d2", "Doc 2", page_count=4, file_size_mb=1.5, burdens_satisfied={"b2": 60.0}),
        ]
        res = solve_dossier_packing(docs, burdens, max_pages=15, max_mb=5.0)
        self.assertTrue(res.all_burdens_met)
        self.assertEqual(len(res.selected_documents), 2)

    def test_p7_probe_scheduling(self):
        endpoints = [ConsularEndpoint("ep1", "VFS", rate_limit_rpm=6, ban_risk_weight=1.0, expected_slot_drop_probability=0.9)]
        proxies = [ProxyNode("prx1", "10.0.0.1", 30.0)]
        res = solve_probe_scheduling(endpoints, proxies, time_horizon_seconds=60.0)
        self.assertGreater(res.total_probes_scheduled, 0)
        self.assertLess(res.cumulative_ban_risk_pct, 100.0)

    def test_p8_rolling_stay(self):
        history = [HistoricalStay(10, 40)]  # 31 days
        proposed = [ProposedTrip("t1", 50, 40, 20, 100.0)]
        res = solve_rolling_stay_optimization(history, proposed)
        self.assertTrue(res.legally_compliant)
        self.assertLessEqual(res.max_rolling_180_utilization, 90)

    def test_p9_officer_balancing(self):
        officers = [
            ConsularOfficer("off1", ["Arabic"], ["Tourist"], False),
            ConsularOfficer("off2", ["English"], ["Tourist"], False),
        ]
        candidates = [
            InterviewCandidate("c1", "Tourist", "Arabic", 15),
            InterviewCandidate("c2", "Tourist", "English", 15),
        ]
        res = solve_interview_line_balancing(officers, candidates)
        self.assertEqual(res.skill_mismatches, 0)
        self.assertEqual(len(res.assignments["off1"]), 1)
        self.assertEqual(len(res.assignments["off2"]), 1)

    def test_p10_fraud_detection(self):
        nodes = [
            VisaApplicationNode("a1", "U1", "TAX_A", "H_B", "B1", 1.0),
            VisaApplicationNode("a2", "U2", "TAX_A", "H_B", "B1", 2.0),
            VisaApplicationNode("a3", "U3", "TAX_A", "H_B", "B1", 3.0),
        ]
        edges = [
            SponsorEdge("a1", "a2", "Tax", "TAX_A"),
            SponsorEdge("a2", "a3", "Tax", "TAX_A"),
            SponsorEdge("a1", "a3", "Tax", "TAX_A"),
        ]
        res = solve_fraud_ring_detection(nodes, edges, min_clique_size=3)
        self.assertEqual(len(res.detected_fraud_cliques), 1)
        self.assertEqual(res.highest_risk_network_size, 3)

    def test_engine_full_benchmark(self):
        engine = ConsularNPHardEngine()
        bench = engine.benchmark_all_10()
        self.assertEqual(len(bench["solvers"]), 10)
        self.assertGreater(bench["total_benchmark_time_us"], 0.0)

    def test_adapters(self):
        engine = ConsularNPHardEngine()
        suite = engine.generate_synthetic_benchmark_suite()
        # Test concierge adapter
        res_solv = engine.concierge_adapter.audit_bank_solvency(*suite["p3_solvency"])
        self.assertGreater(res_solv.qualified_daily_eur_balance, 0.0)
        # Test consular ops adapter
        res_slot = engine.consular_adapter.allocate_slots_fairly(*suite["p1_slot"])
        self.assertGreater(res_slot.total_matched, 0)


if __name__ == "__main__":
    unittest.main()
