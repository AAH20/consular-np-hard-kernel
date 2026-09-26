"""Data contracts and model definitions for the 10 Apex NP-Hard Problems in Consular Logistics and Visa Systems."""
from dataclasses import dataclass, field
from typing import List, Dict, Set, Tuple, Optional, Any

# --- Problem 1: Consular Appointment Slot Allocation (HR-C Fair Matching) ---
@dataclass
class ApplicantRequest:
    request_id: str
    applicant_name: str
    group_id: str  # Family or delegation bundle
    visa_category: str  # e.g., "Schengen-Tourist", "US-B1/B2", "National-D"
    urgency_score: float  # e.g., medical emergency, conference date
    preferred_dates: List[str]  # YYYY-MM-DD
    max_days_flexibility: int = 7

@dataclass
class ConsularSlot:
    slot_id: str
    consulate_code: str  # e.g., "CAI-DEU", "ALX-FRA"
    date_str: str  # YYYY-MM-DD
    time_window: str  # e.g., "09:00-10:00"
    capacity: int
    allowed_categories: List[str]

@dataclass
class SlotAllocationResult:
    matched_slots: Dict[str, str]  # request_id -> slot_id
    total_matched: int
    family_bundles_preserved_pct: float
    fairness_gini_coefficient: float
    bot_scalper_quarantined_count: int
    algorithm: str
    execution_time_us: float

# --- Problem 2: Multi-Jurisdiction Schengen Itinerary & Consular Authority Router ---
@dataclass
class TravelLeg:
    leg_id: str
    country_code: str  # ISO-2 e.g. "FR", "DE", "IT"
    duration_days: int
    entry_order: int
    is_main_purpose: bool = False

@dataclass
class CountryRule:
    country_code: str
    min_processing_days: int
    visa_fee_eur: float
    historical_refusal_rate_pct: float
    appointment_wait_days: int

@dataclass
class JurisdictionRouteResult:
    competent_consulate_country: str
    legal_basis: str  # "Main Destination (Longest Stay)" or "First Entry"
    estimated_total_lead_time_days: int
    aggregate_risk_score: float
    itinerary_compliant: bool
    algorithm: str
    execution_time_us: float

# --- Problem 3: Multi-Account Bank Statement Solvency & Anti-Fraud Proof Packing ---
@dataclass
class BankTransaction:
    tx_id: str
    date_offset_days: int  # 0 to 180
    amount_eur: float
    is_salary_or_organic: bool
    description: str

@dataclass
class AccountStatement:
    account_id: str
    bank_name: str
    currency: str
    closing_balance_eur: float
    transactions: List[BankTransaction] = field(default_factory=list)

@dataclass
class SolvencyPackingResult:
    selected_accounts: List[str]
    qualified_daily_eur_balance: float
    sudden_deposit_anomaly_ratio: float
    solvency_confidence_score: float  # 0 to 100
    algorithm: str
    execution_time_us: float

# --- Problem 4: Multilingual Consular Identity Resolution & Watchlist Multicut ---
@dataclass
class IdentityRecord:
    record_id: str
    latin_name: str
    arabic_name: str
    passport_num: str
    dob_str: str
    national_id: str
    source_dataset: str  # "VisaApp", "SIS_II", "Interpol", "PriorRefusal"

@dataclass
class EntityClusterResult:
    clusters: Dict[int, List[str]]  # cluster_id -> record_ids
    watchlist_matches: List[Tuple[str, str, float]]  # (app_id, watchlist_id, score)
    false_match_risk_score: float
    algorithm: str
    execution_time_us: float

# --- Problem 5: Delegation & Family Group Interview Co-Dependency Scheduler ---
@dataclass
class ApplicantTask:
    task_id: str
    applicant_id: str
    family_id: str
    station_type_required: str  # "Biometric", "Officer_Interview", "Translator"
    duration_min: int
    depends_on_task: Optional[str] = None  # e.g., biometric must precede interview
    must_sync_with_family: bool = True

@dataclass
class BiometricStation:
    station_id: str
    station_type: str
    operating_minutes: int = 480

@dataclass
class GroupScheduleResult:
    schedule: Dict[str, Tuple[str, int, int]]  # task_id -> (station_id, start_min, end_min)
    makespan_minutes: int
    family_split_count: int
    precedence_certified: bool
    algorithm: str
    execution_time_us: float

# --- Problem 6: Evidentiary Dossier Packing under Statutory Burdens ---
@dataclass
class StatutoryBurden:
    burden_id: str
    name: str  # "Socio-Economic Home Ties", "Financial Means", "Itinerary Coherence", "Accommodation"
    min_evidence_score_required: float

@dataclass
class EvidenceDocument:
    doc_id: str
    name: str
    page_count: int
    file_size_mb: float
    burdens_satisfied: Dict[str, float]  # burden_id -> score contribution

@dataclass
class DossierPackingResult:
    selected_documents: List[str]
    total_pages: int
    total_size_mb: float
    burdens_coverage_pct: float
    all_burdens_met: bool
    algorithm: str
    execution_time_us: float

# --- Problem 7: Dynamic WAF Probe Scheduling & Sentinel Anti-Bot Evasion ---
@dataclass
class ConsularEndpoint:
    endpoint_id: str
    portal_name: str  # "VFS_Cairo", "TLS_Alexandria", "BLS_Cairo"
    rate_limit_rpm: int
    ban_risk_weight: float
    expected_slot_drop_probability: float

@dataclass
class ProxyNode:
    proxy_id: str
    ip_subnet: str
    latency_ms: float
    cooldown_seconds: float = 0.0

@dataclass
class ProbeScheduleResult:
    probe_dispatches: List[Tuple[float, str, str]]  # (timestamp_sec, proxy_id, endpoint_id)
    total_probes_scheduled: int
    expected_slots_discovered: float
    cumulative_ban_risk_pct: float
    algorithm: str
    execution_time_us: float

# --- Problem 8: Schengen 90/180-Day Rolling Window Stay Duration Optimizer ---
@dataclass
class HistoricalStay:
    entry_day: int
    exit_day: int

@dataclass
class ProposedTrip:
    trip_id: str
    preferred_entry_day: int
    desired_duration_days: int
    min_acceptable_duration_days: int
    value_weight: float

@dataclass
class RollingStayResult:
    scheduled_trips: List[Tuple[str, int, int]]  # (trip_id, entry_day, duration)
    total_days_spent: int
    max_rolling_180_utilization: int  # must not exceed 90
    legally_compliant: bool
    algorithm: str
    execution_time_us: float

# --- Problem 9: Consular Officer Skill-Constrained Interview Line Balancer ---
@dataclass
class InterviewCandidate:
    candidate_id: str
    visa_type: str  # "Immigrant", "Non-Immigrant", "Student", "Diplomatic"
    primary_language: str  # "Arabic", "English", "French"
    estimated_duration_min: int
    requires_security_clearance: bool = False

@dataclass
class ConsularOfficer:
    officer_id: str
    languages_spoken: List[str]
    authorized_visa_types: List[str]
    has_security_clearance: bool
    max_shift_minutes: int = 420

@dataclass
class QueueBalanceResult:
    assignments: Dict[str, List[str]]  # officer_id -> [candidate_id]
    makespan_minutes: int
    workload_variance: float
    skill_mismatches: int
    algorithm: str
    execution_time_us: float

# --- Problem 10: Covert Visa Fraud Ring & Shell Sponsor Graph Detection ---
@dataclass
class VisaApplicationNode:
    app_id: str
    applicant_name: str
    employer_tax_id: str
    hotel_booking_ref: str
    bank_branch_code: str
    submission_timestamp: float

@dataclass
class SponsorEdge:
    source_app_id: str
    target_app_id: str
    shared_attribute_type: str  # "TaxID", "HotelRef", "BankTemplate", "IPAddress"
    attribute_value: str

@dataclass
class FraudRingResult:
    detected_fraud_cliques: List[List[str]]  # list of application IDs forming suspicious cliques
    highest_risk_network_size: int
    synthetic_identity_flag_count: int
    algorithm: str
    execution_time_us: float
