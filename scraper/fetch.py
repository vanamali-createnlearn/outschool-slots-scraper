import requests

GRAPHQL_ENDPOINT = "https://outschool.com/graphql"

QUERY = """
query ClassDetailsSections($activityUid: ID!) {
  activity(uid: $activityUid) {
    paginatedFilteredSections {
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

def extract_uid(url):
    return url.split("-")[-1]

def fetch_course_slots(url):
    uid = extract_uid(url)

    payload = {
        "query": QUERY,
        "variables": {"activityUid": uid}
    }

    r = requests.post(GRAPHQL_ENDPOINT, json=payload)
    r.raise_for_status()

    data = r.json()

    meetings = []

    for section in data["data"]["activity"]["paginatedFilteredSections"]["data"]:
        for meeting in section["meetings"]:
            meetings.append((
                meeting["start_time"],
                meeting["end_time"]
            ))

    return meetings
