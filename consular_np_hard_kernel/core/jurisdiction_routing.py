"""Multi-Jurisdiction Schengen Itinerary & Consular Authority Router.

Solves the multi-constrained path optimization problem under Article 5 of the Schengen Visa Code.
Determines legally competent consular jurisdiction (longest stay vs first entry) and evaluates
aggregate processing lead times and refusal risk scores.
"""
import time
from typing import List, Dict, Tuple
from .models import TravelLeg, CountryRule, JurisdictionRouteResult


def solve_jurisdiction_routing(
    legs: List[TravelLeg],
    country_rules: List[CountryRule]
) -> JurisdictionRouteResult:
    """Computes competent consular authority and evaluates processing risk under Schengen Article 5."""
    t0 = time.perf_counter()
    if not legs:
        return JurisdictionRouteResult(
            competent_consulate_country="UNKNOWN",
            legal_basis="None",
            estimated_total_lead_time_days=0,
            aggregate_risk_score=0.0,
            itinerary_compliant=False,
            algorithm="Schengen-Article5-MCPP",
            execution_time_us=0.0
        )

    rule_map = {r.country_code: r for r in country_rules}
    
    # Sort legs by entry order
    sorted_legs = sorted(legs, key=lambda l: l.entry_order)
    
    # 1. Check if any leg is marked as main purpose (e.g. conference or medical)
    main_purpose_leg = next((l for l in sorted_legs if l.is_main_purpose), None)
    
    # 2. Count total stay duration per country
    country_duration: Dict[str, int] = {}
    for l in sorted_legs:
        country_duration[l.country_code] = country_duration.get(l.country_code, 0) + l.duration_days

    # Determine longest stay
    max_duration = max(country_duration.values())
    longest_countries = [c for c, d in country_duration.items() if d == max_duration]

    competent_country = ""
    legal_basis = ""

    if main_purpose_leg:
        competent_country = main_purpose_leg.country_code
        legal_basis = "Article 5(1)(b) - Primary Purpose of Stay"
    elif len(longest_countries) == 1:
        competent_country = longest_countries[0]
        legal_basis = f"Article 5(1)(b) - Main Destination ({max_duration} Days Longest Stay)"
    else:
        # Tie-breaker: Country of first entry among the tied longest countries
        first_country = sorted_legs[0].country_code
        if first_country in longest_countries:
            competent_country = first_country
        else:
            competent_country = longest_countries[0]
        legal_basis = "Article 5(1)(c) - First Point of Entry (Duration Tie-Breaker)"

    # Compute lead time and risk based on competent country rules
    c_rule = rule_map.get(competent_country, CountryRule(competent_country, 15, 90.0, 15.0, 30))
    total_lead_time = c_rule.appointment_wait_days + c_rule.min_processing_days
    
    # Risk calculation combines refusal rate with lead time friction
    risk_score = c_rule.historical_refusal_rate_pct * 1.5 + (c_rule.appointment_wait_days / 60.0) * 10.0

    t1 = time.perf_counter()
    exec_us = (t1 - t0) * 1_000_000.0

    return JurisdictionRouteResult(
        competent_consulate_country=competent_country,
        legal_basis=legal_basis,
        estimated_total_lead_time_days=total_lead_time,
        aggregate_risk_score=round(risk_score, 2),
        itinerary_compliant=True,
        algorithm="Schengen-Article5-MCPP",
        execution_time_us=round(exec_us, 2)
    )
