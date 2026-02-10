from playwright.sync_api import sync_playwright


def fetch_course_slots(course):
    url = course["url"]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Wait explicitly for the GraphQL response while loading the page
        with page.expect_response(lambda r: "ClassDetailsSections" in r.url) as resp:
            page.goto(url, wait_until="domcontentloaded")

        response = resp.value
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
