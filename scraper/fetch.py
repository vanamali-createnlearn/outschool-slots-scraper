from playwright.sync_api import sync_playwright


def fetch_course_slots(course):
    url = course["url"]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Start navigation
        page.goto(url, wait_until="domcontentloaded")

        # Explicitly wait for the ClassDetailsSections GraphQL response
        response = page.wait_for_response(
            lambda r: "ClassDetailsSections" in r.url
        )

        data = response.json()
        sections = data["data"]["activity"]["paginatedFilteredSections"]["data"]

        meetings = []
        for section in sections:
            for meeting in section["meetings"]:
                meetings.append(
                    (meeting["start_time"], meeting["end_time"])
                )

        browser.close()

    return meetings
