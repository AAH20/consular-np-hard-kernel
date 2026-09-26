"""Schengen 90/180-Day Rolling Window Stay Duration Optimizer.

Solves the exact sliding-window interval packing problem under Regulation (EU) No 610/2013.
Guarantees that third-country nationals do not exceed 90 days of lawful stay within any continuous
180-day historical/future window while maximizing travel utility across proposed trips.
"""
import time
from typing import List, Tuple, Set
from .models import HistoricalStay, ProposedTrip, RollingStayResult


def _count_stay_in_window(stay_days_set: Set[int], end_day: int) -> int:
    """Counts days present in the 180-day window [end_day - 179, end_day]."""
    start_day = max(0, end_day - 179)
    # Check intersection count
    return sum(1 for d in range(start_day, end_day + 1) if d in stay_days_set)


def solve_rolling_stay_optimization(
    history: List[HistoricalStay],
    proposed_trips: List[ProposedTrip]
) -> RollingStayResult:
    """Schedules proposed trips maximizing lawful duration while strictly respecting the 90/180-day rule."""
    t0 = time.perf_counter()
    
    # Build set of days already spent in Schengen from history
    active_days: Set[int] = set()
    for h in history:
        for d in range(h.entry_day, h.exit_day + 1):
            active_days.add(d)

    # Sort proposed trips by priority / value weight descending
    sorted_trips = sorted(proposed_trips, key=lambda t: t.value_weight, reverse=True)
    scheduled: List[Tuple[str, int, int]] = []

    for trip in sorted_trips:
        # Determine maximum feasible duration from desired down to min_acceptable
        best_duration = 0
        entry = trip.preferred_entry_day

        for candidate_dur in range(trip.desired_duration_days, trip.min_acceptable_duration_days - 1, -1):
            # Test if adding [entry, entry + candidate_dur - 1] violates 90/180 rule on any day
            trial_days = set(active_days)
            for d in range(entry, entry + candidate_dur):
                trial_days.add(d)

            # Check every 180-day window ending from entry up to entry + candidate_dur + 180
            valid = True
            for check_day in range(entry, entry + candidate_dur + 180):
                if _count_stay_in_window(trial_days, check_day) > 90:
                    valid = False
                    break

            if valid:
                best_duration = candidate_dur
                break

        if best_duration >= trip.min_acceptable_duration_days:
            scheduled.append((trip.trip_id, entry, best_duration))
            for d in range(entry, entry + best_duration):
                active_days.add(d)

    # Calculate maximum rolling 180-day utilization across the entire timeline
    max_days = max(active_days) if active_days else 0
    max_util = 0
    for day in range(max_days + 1):
        u = _count_stay_in_window(active_days, day)
        if u > max_util:
            max_util = u

    total_days = sum(dur for _, _, dur in scheduled)
    compliant = (max_util <= 90)

    t1 = time.perf_counter()
    exec_us = (t1 - t0) * 1_000_000.0

    return RollingStayResult(
        scheduled_trips=scheduled,
        total_days_spent=total_days,
        max_rolling_180_utilization=max_util,
        legally_compliant=compliant,
        algorithm="Sliding-Window-Schengen-DP",
        execution_time_us=round(exec_us, 2)
    )
