import requests
import json
from bs4 import BeautifulSoup

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

HEADERS = {
    "content-type": "application/json"
}

def extract_activity_uid(url: str) -> str:
    r = requests.get(url)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    script = soup.find("script", id="__NEXT_DATA__")

    if not script:
        raise RuntimeError("__NEXT_DATA__ script not found")

    data = json.loads(script.string)

    try:
        return data["props"]["pageProps"]["activity"]["uid"]
    except KeyError:
        raise RuntimeError("Activity UID not found inside __NEXT_DATA__")

def fetch_course_slots(course: dict):
    activity_uid = extract_activity_uid(course["url"])

    payload = {
        "query": QUERY,
        "variables": {
            "activityUid": activity_uid
        }
    }

    r = requests.post(GRAPHQL_ENDPOINT, headers=HEADERS, json=payload)
    r.raise_for_status()

    sections = r.json()["data"]["activity"]["paginatedFilteredSections"]["data"]

    slots = []
    for section in sections:
        for meeting in section["meetings"]:
            slots.append((meeting["start_time"], meeting["end_time"]))

    return slots
