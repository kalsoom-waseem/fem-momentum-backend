from datetime import date, timedelta


def compute_cycle_day(anchor_date: date, target: date, cycle_length:int)->int:
    delta_days = (target - anchor_date).days
    return (delta_days % cycle_length) + 1


def ovulation_day(cycle_length:int)->int:
    return max(1, cycle_length - 14)

def fertile_windows_days(cycle_length: int)->tuple[int,int]:
    ov_day = ovulation_day(cycle_length)
    start_fertile = max(1, ov_day - 5)
    end_fertile = min(cycle_length, ov_day + 1)
    return (start_fertile, end_fertile)

def phase_for_cycle_day(cycle_day: int, period_length: int, cycle_length: int) -> str:
    ovulation= ovulation_day(cycle_length)
    if cycle_day <= period_length:
        return "menstrual"
    if cycle_day < ovulation - 1:
        return "follicular"
    if (ovulation - 1) <= cycle_day <= (ovulation + 1):
        return "ovulation"
    return "luteal"

def day_info(anchor_date: date, target: date, period_length: int, cycle_length: int):
    cycle_day = compute_cycle_day(anchor_date, target, cycle_length)
    phase = phase_for_cycle_day(cycle_day, period_length, cycle_length)
    fertile_start, fertile_end = fertile_windows_days(cycle_length)
    return {
        "date": target,
        "cycle_day": cycle_day,
        "phase": phase,
        "is_period_day": cycle_day <= period_length,
        "is_fertile_window": fertile_start <= cycle_day <= fertile_end,
        "is_ovulation_day": cycle_day == ovulation_day(cycle_length)
    }