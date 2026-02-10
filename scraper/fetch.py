import requests

GRAPHQL_ENDPOINT = "https://outschool.com/graphql"

QUERY = """
query ClassDetailsSections($activityUid: ID!) {
  activity(uid: $activityUid) {
    uid
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

HEADERS = {
    "content-type": "application/json"
}

def extract_uid(url):
    return url.split("-")[-1]

def fetch_course_slots(url):
    uid = extract_uid(url)

    payload = {
        "operationName": "ClassDetailsSections",
        "query": QUERY,
        "variables": {
            "activityUid": uid
        }
    }

    response = requests.post(
        GRAPHQL_ENDPOINT,
        headers=HEADERS,
        json=payload
    )

    response.raise_for_status()
    data = response.json()

    activity = data["data"]["activity"]
    if activity is None:
        raise RuntimeError(f"Activity not found for UID {uid}")

    meetings = []

    for section in activity["paginatedFilteredSections"]["data"]:
        for meeting in section["meetings"]:
            meetings.append(
                (meeting["start_time"], meeting["end_time"])
            )

    return meetings
