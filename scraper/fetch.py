import requests

GRAPHQL_ENDPOINT = "https://outschool.com/graphql"
HEADERS = {"content-type": "application/json"}

RESOLVE_UID_QUERY = """
query ActivityBySlug($slug: String!) {
  activityBySlug(slug: $slug) {
    uid
  }
}
"""

SECTIONS_QUERY = """
query ClassDetailsSections($activityUid: ID!) {
  activity(uid: $activityUid) {
    paginatedFilteredSections(first: 50) {
      data {
        meetings {
          start_time
          end_time
        }
      }
    }
  }
}
"""

def extract_slug(url):
    return url.rstrip("/").split("/classes/")[-1]

def resolve_activity_uid(slug):
    payload = {
        "query": RESOLVE_UID_QUERY,
        "variables": {"slug": slug}
    }

    r = requests.post(GRAPHQL_ENDPOINT, headers=HEADERS, json=payload)
    r.raise_for_status()

    data = r.json()
    activity = data["data"]["activityBySlug"]

    if not activity:
        raise RuntimeError(f"Could not resolve UID for slug: {slug}")

    return activity["uid"]

def fetch_course_slots(course):
    slug = extract_slug(course["url"])
    activity_uid = resolve_activity_uid(slug)

    payload = {
        "query": SECTIONS_QUERY,
        "variables": {"activityUid": activity_uid}
    }

    r = requests.post(GRAPHQL_ENDPOINT, headers=HEADERS, json=payload)
    r.raise_for_status()

    data = r.json()
    sections = data["data"]["activity"]["paginatedFilteredSections"]["data"]

    meetings = []
    for section in sections:
        for meeting in section["meetings"]:
            meetings.append(
                (meeting["start_time"], meeting["end_time"])
            )

    return meetings
