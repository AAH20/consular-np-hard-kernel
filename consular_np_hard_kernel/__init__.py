"""Consular NP-Hard Kernel: Solvers for the 10 Apex NP-Hard Problems in Consular Logistics and Visa Systems."""
from .engine import ConsularNPHardEngine
from .adapters.applicant_concierge import ApplicantConciergeAdapter
from .adapters.embassy_consular_ops import EmbassyConsularOpsAdapter

__version__ = "1.0.0"
__all__ = [
    "ConsularNPHardEngine",
    "ApplicantConciergeAdapter",
    "EmbassyConsularOpsAdapter",
]
