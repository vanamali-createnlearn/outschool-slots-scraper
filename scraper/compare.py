def compare_slots(inhouse_slots, competitor_data):
    competitor_union = set()

    for course in competitor_data.values():
        competitor_union |= course["slots"]

    missing = competitor_union - inhouse_slots
    extra = inhouse_slots - competitor_union

    return {
        "missing": missing,
        "extra": extra
    }
