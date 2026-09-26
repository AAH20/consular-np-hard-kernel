"""Embassy & Consular Operations Adapter (Mission, VFS/TLS, and Visa Officer Flow).

Provides high-level consular post management workflows: scalper-resistant slot allocation,
multilingual identity resolution against SIS II/VIS watchlists, delegation flow scheduling,
consular officer workload balancing, and organized fraud ring graph detection.
"""
from typing import List, Dict, Tuple, Any
from ..core.models import (
    ApplicantRequest,
    ConsularSlot,
    SlotAllocationResult,
    IdentityRecord,
    EntityClusterResult,
    ApplicantTask,
    BiometricStation,
    GroupScheduleResult,
    ConsularOfficer,
    InterviewCandidate,
    QueueBalanceResult,
    VisaApplicationNode,
    SponsorEdge,
    FraudRingResult,
)
from ..core.slot_allocation import solve_slot_allocation
from ..core.identity_resolution import solve_identity_resolution
from ..core.group_scheduling import solve_group_interview_scheduling
from ..core.officer_balancing import solve_interview_line_balancing
from ..core.fraud_detection import solve_fraud_ring_detection


class EmbassyConsularOpsAdapter:
    """Specialized adapter for diplomatic missions, consular posts, and outsourced VAC centers."""

    @staticmethod
    def allocate_slots_fairly(
        requests: List[ApplicantRequest],
        slots: List[ConsularSlot]
    ) -> SlotAllocationResult:
        """Matches applicants to appointment windows with anti-bot filtering and family contiguity."""
        return solve_slot_allocation(requests, slots)

    @staticmethod
    def screen_watchlist_entities(
        records: List[IdentityRecord]
    ) -> EntityClusterResult:
        """Performs correlation clustering across multilingual records and flags SIS II/Interpol hits."""
        return solve_identity_resolution(records)

    @staticmethod
    def schedule_delegation_intake(
        tasks: List[ApplicantTask],
        stations: List[BiometricStation]
    ) -> GroupScheduleResult:
        """Coordinates biometrics and interview queues without separating family members or teams."""
        return solve_group_interview_scheduling(tasks, stations)

    @staticmethod
    def balance_officer_workloads(
        officers: List[ConsularOfficer],
        candidates: List[InterviewCandidate]
    ) -> QueueBalanceResult:
        """Balances interview queues matching linguistic and security clearance authorizations."""
        return solve_interview_line_balancing(officers, candidates)

    @staticmethod
    def detect_fraud_rings(
        nodes: List[VisaApplicationNode],
        edges: List[SponsorEdge],
        min_clique_size: int = 3
    ) -> FraudRingResult:
        """Discovers coordinated visa syndicates and synthetic employer sponsor networks."""
        return solve_fraud_ring_detection(nodes, edges, min_clique_size)
