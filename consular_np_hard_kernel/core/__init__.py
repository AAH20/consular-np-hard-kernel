"""Core algorithms and models for the 10 Apex NP-Hard Problems in Consular Logistics and Visa Systems."""
from .models import (
    ApplicantRequest,
    ConsularSlot,
    SlotAllocationResult,
    TravelLeg,
    CountryRule,
    JurisdictionRouteResult,
    BankTransaction,
    AccountStatement,
    SolvencyPackingResult,
    IdentityRecord,
    EntityClusterResult,
    ApplicantTask,
    BiometricStation,
    GroupScheduleResult,
    EvidenceDocument,
    StatutoryBurden,
    DossierPackingResult,
    ConsularEndpoint,
    ProxyNode,
    ProbeScheduleResult,
    HistoricalStay,
    ProposedTrip,
    RollingStayResult,
    ConsularOfficer,
    InterviewCandidate,
    QueueBalanceResult,
    VisaApplicationNode,
    SponsorEdge,
    FraudRingResult,
)

from .slot_allocation import solve_slot_allocation
from .jurisdiction_routing import solve_jurisdiction_routing
from .solvency_packing import solve_solvency_packing
from .identity_resolution import solve_identity_resolution
from .group_scheduling import solve_group_interview_scheduling
from .dossier_packing import solve_dossier_packing
from .probe_scheduling import solve_probe_scheduling
from .rolling_stay import solve_rolling_stay_optimization
from .officer_balancing import solve_interview_line_balancing
from .fraud_detection import solve_fraud_ring_detection

__all__ = [
    # Models
    "ApplicantRequest",
    "ConsularSlot",
    "SlotAllocationResult",
    "TravelLeg",
    "CountryRule",
    "JurisdictionRouteResult",
    "BankTransaction",
    "AccountStatement",
    "SolvencyPackingResult",
    "IdentityRecord",
    "EntityClusterResult",
    "ApplicantTask",
    "BiometricStation",
    "GroupScheduleResult",
    "EvidenceDocument",
    "StatutoryBurden",
    "DossierPackingResult",
    "ConsularEndpoint",
    "ProxyNode",
    "ProbeScheduleResult",
    "HistoricalStay",
    "ProposedTrip",
    "RollingStayResult",
    "ConsularOfficer",
    "InterviewCandidate",
    "QueueBalanceResult",
    "VisaApplicationNode",
    "SponsorEdge",
    "FraudRingResult",
    # Solvers
    "solve_slot_allocation",
    "solve_jurisdiction_routing",
    "solve_solvency_packing",
    "solve_identity_resolution",
    "solve_group_interview_scheduling",
    "solve_dossier_packing",
    "solve_probe_scheduling",
    "solve_rolling_stay_optimization",
    "solve_interview_line_balancing",
    "solve_fraud_ring_detection",
]
