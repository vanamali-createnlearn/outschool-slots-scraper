import json
from fetch import fetch_course_slots
from normalize import normalize_slots
from compare import compare_slots
from sheets import write_competitor_matrices, write_comparisons


def load_courses():
    with open("courses.json", "r") as f:
        return json.load(f)["courses"]


def main():
    courses = load_courses()

    competitor_data = {}
    inhouse_data = {}

    for course in courses:
        # 🔑 IMPORTANT: pass full course object
        raw_slots = fetch_course_slots(course)
        weekly_slots = normalize_slots(raw_slots)

        if course["nature"] == "competitor":
            competitor_data[course["id"]] = {
                "name": course["name"],
                "slots": weekly_slots
            }

        elif course["nature"] == "inhouse":
            inhouse_data[course["id"]] = {
                "name": course["name"],
                "slots": weekly_slots
            }

    # Write competitor matrices once
    write_competitor_matrices(competitor_data)

    # Compare per in-house course
    for inhouse in inhouse_data.values():
        comparisons = compare_slots(
            inhouse["slots"],
            competitor_data
        )
        write_comparisons(inhouse["name"], comparisons)


if __name__ == "__main__":
    main()
