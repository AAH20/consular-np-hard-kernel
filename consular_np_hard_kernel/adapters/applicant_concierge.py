"""Applicant Concierge Adapter (Veeza AI / Travel Agent & Consumer Flow).

Provides high-level applicant-side agentic workflows: bank statement solvency auditing,
Schengen Article 5 competent consulate routing, evidentiary dossier packing,
rolling 90/180-day stay compliance, and WAF rate-compliant appointment slot probing.
"""
from typing import List, Dict, Tuple, Any
from ..core.models import (
    AccountStatement,
    SolvencyPackingResult,
    TravelLeg,
    CountryRule,
    JurisdictionRouteResult,
    EvidenceDocument,
    StatutoryBurden,
    DossierPackingResult,
    HistoricalStay,
    ProposedTrip,
    RollingStayResult,
    ConsularEndpoint,
    ProxyNode,
    ProbeScheduleResult,
)
from ..core.solvency_packing import solve_solvency_packing
from ..core.jurisdiction_routing import solve_jurisdiction_routing
from ..core.dossier_packing import solve_dossier_packing
from ..core.rolling_stay import solve_rolling_stay_optimization
from ..core.probe_scheduling import solve_probe_scheduling


class ApplicantConciergeAdapter:
    """Specialized adapter for applicants, visa concierges (Veeza AI), and corporate travel desks."""

    @staticmethod
    def audit_bank_solvency(
        statements: List[AccountStatement],
        min_required_daily_eur: float = 100.0,
        trip_days: int = 14
    ) -> SolvencyPackingResult:
        """Audits bank accounts to eliminate sudden-deposit fraud suspicion while proving solvency."""
        return solve_solvency_packing(statements, min_required_daily_eur, trip_days)

    @staticmethod
    def route_schengen_jurisdiction(
        itinerary_legs: List[TravelLeg],
        country_rules: List[CountryRule]
    ) -> JurisdictionRouteResult:
        """Determines competent consular authority under Schengen Article 5 (longest stay / first entry)."""
        return solve_jurisdiction_routing(itinerary_legs, country_rules)

    @staticmethod
    def assemble_evidentiary_dossier(
        documents: List[EvidenceDocument],
        burdens: List[StatutoryBurden],
        max_pages: int = 25,
        max_mb: float = 10.0
    ) -> DossierPackingResult:
        """Selects minimal authoritative document subset satisfying statutory home ties and solvency."""
        return solve_dossier_packing(documents, burdens, max_pages, max_mb)

    @staticmethod
    def optimize_rolling_stays(
        history: List[HistoricalStay],
        proposed_trips: List[ProposedTrip]
    ) -> RollingStayResult:
        """Schedules future travel while guaranteeing 100% compliance with Schengen 90/180-day limits."""
        return solve_rolling_stay_optimization(history, proposed_trips)

    @staticmethod
    def schedule_appointment_sentinel_probes(
        endpoints: List[ConsularEndpoint],
        proxies: List[ProxyNode],
        time_horizon_sec: float = 300.0
    ) -> ProbeScheduleResult:
        """Schedules proxy polling across VFS/TLS/BLS portals under WAF rate limits without getting banned."""
        return solve_probe_scheduling(endpoints, proxies, time_horizon_sec)
