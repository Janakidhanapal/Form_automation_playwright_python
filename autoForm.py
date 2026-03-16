from playwright.sync_api import sync_playwright
import json
import random
import re

formURL = "https://docs.google.com/forms/d/e/1FAIpQLSfO7oO8H0WKLuTS3UFDOuJQv1noSMi9M2PP5f7fa-1TLrnMoQ/viewform?usp=dialog"

with open("responder.json", "r") as f:
    responder_details = json.load(f)

#page1
age = ["21-30", "31-40"]
org_experience = ["<4", "4-8", "9-12", ">12"]
overall_experience = ["<5", "5-10", "11-15", ">15"]
designation = ["Worker", "Manager", "Senior Manager", "General Manager"]
department = ["Operations", "Supply Chain"]
level_of_management = ["Bottom", "Middle", "Top"]
performance = ['Strongly Agree', 'Agree', 'Neutral', 'Disagree', 'Strongly Disagree']

#page2
questions = [
  # Strategic Purchasing
  'Select suppliers based on clearly defined process',
  'Transparent Selection Process',
  'Includes Quality Management System',
  'Special Instruction for delicate parts',
  'Specification available raw material',
  'Includes environmental management system',
  # Supplier Management Practices
  'Share our details with suppliers',
  'Invest in development of suppliers',
  'Supplier shows great interest in integration',
  'Automated system for evaluation',
  'Share result of supplier evaluation with suppliers',
  'Formal supplier selection process',
  'Suppliers audited',
  # Quality System
  'Installed Continuous Improvement Process',
  'Statistical Process Control',
  'Failure Mode and Effect Analysis',
  'Process for non conforming products',
  'Monitor equipment regularly',
  'Perform first article Inspection',
  'Ensure evidentiary documentation',
  'Supplier scorecard to evaluate quality',
  # Cost Management Practices
  'Conduct cost benchmarking',
  'Cost reduction strategies',
  'Value Engineering',
  'Supplier scorecard for cost',
  # Delivery Performance
  'Track On- time- In- Full delivery metrics on supplier',
  'Accuracy of advance shipping Notification',
  'Average time lead variation',
  'Forecast to improve delivery predictability',
  'Supplier scorecard for Delivery'
]
agreement = ['Strongly Agree', 'Agree', 'Neutral', 'Disagree', 'Strongly Disagree']

#Page 3
factors = ['Quality', 'Price', 'Quantity', 'Service', 'Innovation']
rank = ['Rank 1', 'Rank 2', 'Rank 3', 'Rank 4', 'Rank 5']

def fill_form():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

        try:
            for responder in responder_details:
                page = context.new_page()
                page.goto(formURL)

                #Page 1
                page.locator("input[type='email']").fill(responder['email'])
                page.get_by_label(responder['gender'], exact=True).click()
                page.get_by_label(random.choice(age)).click()
                page.get_by_label(random.choice(org_experience)).click()
                page.get_by_label(random.choice(overall_experience)).click()
                page.get_by_label(random.choice(designation), exact=True).click()
                page.get_by_label(random.choice(department)).click()
                page.get_by_label(random.choice(level_of_management)).click()
                page.get_by_text(re.compile(r"Volgende|Next")).click()

                #Page 2
                for question in questions:
                    page.get_by_label(f"{random.choice(performance)}, antwoord voor {question}", exact=True).click()
                page.get_by_label(random.choice(agreement), exact=True).click()
                page.get_by_text(re.compile(r"Volgende|Next")).click()

                #Page 3
                for factor in factors:
                    page.get_by_label(f"{random.choice(rank)}, antwoord voor {factor} ", exact=True).click()
                page.get_by_text(re.compile(r"Verzenden|Submit")).click()

        except TimeoutError as e:
            print(e)
        finally:
            page.close()
            context.tracing.stop(path="trace.zip")
            context.close()
            browser.close()
            print(f"{responder['email']} - Form filled successfully")

fill_form()
