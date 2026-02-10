from playwright.sync_api import sync_playwright


GRAPHQL_KEYWORD = "ClassDetailsSections"


def fetch_course_slots(course):
    url = course["url"]
    meetings = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox"
            ],
        )

        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
            viewport={"width": 1400, "height": 900}
        )

        page = context.new_page()

        def handle_response(response):
            try:
                if GRAPHQL_KEYWORD in response.url:
                    data = response.json()
                    sections = data["data"]["activity"]["paginatedFilteredSections"]["data"]

                    for section in sections:
                        for meeting in section["meetings"]:
                            meetings.append(
                                (meeting["start_time"], meeting["end_time"])
                            )
            except:
                pass

        page.on("response", handle_response)

        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(5000)

        browser.close()

    if not meetings:
        raise RuntimeError("Blocked by anti-bot protection")

    return meetings
