import requests
import re

GRAPHQL_ENDPOINT = "https://outschool.com/graphql"
HEADERS = {"content-type": "application/json"}

QUERY = """
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

UID_PATTERN = r'"Activity:([a-f0-9\\-]+)"'

def extract_activity_uid(url):
    r = requests.get(url)
    r.raise_for_status()

    match = re.search(UID_PATTERN, r.text)

    if not match:
        raise RuntimeError("Could not locate activity UID in page Apollo state")

    return match.group(1)

def fetch_course_slots(course):
    activity_uid = extract_activity_uid(course["url"])

    payload = {
        "query": QUERY,
        "variables": {
            "activityUid": activity_uid
        }
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
