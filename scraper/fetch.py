from playwright.sync_api import sync_playwright


GRAPHQL_KEYWORD = "ClassDetailsSections"


def fetch_course_slots(course):
    url = course["url"]
    meetings = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        def handle_response(response):
            if GRAPHQL_KEYWORD in response.url:
                data = response.json()
                sections = data["data"]["activity"]["paginatedFilteredSections"]["data"]

                for section in sections:
                    for meeting in section["meetings"]:
                        meetings.append(
                            (meeting["start_time"], meeting["end_time"])
                        )

        page.on("response", handle_response)

        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(3000)

        browser.close()

    return meetings
