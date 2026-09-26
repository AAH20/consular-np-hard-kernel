"""Adapters bridging NP-hard consular solvers to Applicant Concierge and Embassy Operations domains."""
from .applicant_concierge import ApplicantConciergeAdapter
from .embassy_consular_ops import EmbassyConsularOpsAdapter

__all__ = [
    "ApplicantConciergeAdapter",
    "EmbassyConsularOpsAdapter",
]
