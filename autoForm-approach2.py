from playwright.sync_api import sync_playwright
import random
import re
from data import entries

formURL = "https://forms.gle/3AzqAmfZoA5GR6eZ7"

age = ["21-30", "31-40"]
org_experience = ["<4", "4-8", "9-12", ">12"]
overall_experience = ["<5", "5-10", "11-15", ">15"]
designation = ["Worker", "Manager", "Senior Manager", "General Manager"]
department = ["Operations", "Supply Chain"]
level_of_management = ["Bottom", "Middle", "Top"]

with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

        try:
            for entry in entries:
                page = context.new_page()
                page.goto(formURL)

                #Page 1
                page.locator("input[type='email']").fill(entry['email'])
                page.get_by_label(entry['gender'], exact=True).click()
                page.get_by_label(random.choice(age)).click()
                page.get_by_label(random.choice(org_experience)).click()
                page.get_by_label(random.choice(overall_experience)).click()
                page.get_by_label(random.choice(designation), exact=True).click()
                page.get_by_label(random.choice(department)).click()
                page.get_by_label(random.choice(level_of_management)).click()
                page.get_by_text(re.compile(r"Volgende|Next")).click()

                #Page 2
                for radio_group in page.get_by_role('radiogroup').all():
                    radio_group.get_by_role('radio').nth(random.randint(0, 4)).click()
                page.get_by_text(re.compile(r"Volgende|Next")).click()

                #Page 3
                for radio_group in page.get_by_role('radiogroup').all():
                    radio_group.get_by_role('radio').nth(random.randint(0, 4)).click()
                # page.get_by_text(re.compile(r"Verzenden|Submit")).click()
        except TimeoutError as e:
            print(e)
        finally:
            page.close()
            context.tracing.stop(path="trace.zip")
            context.close()
            browser.close()
