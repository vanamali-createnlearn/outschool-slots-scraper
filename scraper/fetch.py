import requests
import re

GRAPHQL_ENDPOINT = "https://outschool.com/graphql"

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

HEADERS = {"content-type": "application/json"}

UID_REGEX = r'"activityUid":"([a-f0-9\\-]+)"'

def extract_activity_uid(url):
    page = requests.get(url)
    page.raise_for_status()

    match = re.search(UID_REGEX, page.text)

    if not match:
        raise RuntimeError("Could not find activity UID in page source")

    return match.group(1)

def fetch_course_slots(url):
    activity_uid = extract_activity_uid(url)

    payload = {
        "query": QUERY,
        "variables": {"activityUid": activity_uid}
    }

    response = requests.post(
        GRAPHQL_ENDPOINT,
        headers=HEADERS,
        json=payload
    )

    response.raise_for_status()
    data = response.json()

    sections = data["data"]["activity"]["paginatedFilteredSections"]["data"]

    meetings = []

    for section in sections:
        for meeting in section["meetings"]:
            meetings.append(
                (meeting["start_time"], meeting["end_time"])
            )

    return meetings
