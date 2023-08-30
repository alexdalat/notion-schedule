import json
import os
from dotenv import load_dotenv

from notion_client import Client

# Step 1: Tell ChatGPT 4 this (subtitute {} with the correct values):
"""
This is format A:
```py
    [
        {
            "title": _____, # title of the item, try it to keep it \
                              short yet descriptive, otherwise overfill to "Note"
            "Course": ___ ___, # Course name in format '{3-4 letters} {3 numbers}'"
            "Type": _____, # can be one of ONLY "Assignment", "Reading", "Notes", \
                                    "Essay", "Group Work", "Project", "Presentation", \
                                    "Study", "Quiz", or "Exam"
            "Due date": _____, # Due date of the item in "%Y-%m-%d" format
            "Note": _____, # usually blank, only fill in if necessary
        },
        {
            "title": _____,
            ...
        }
    ]
```
I want to convert the following schedule into format A:
```
{paste schedule here}
```
This is for course: {course name}
Only include items that have a valid "Type" that can be assigned. This means don't \ 
include activities occurring during that day, etc.
If week of an item is provided along with the day of the week it is due, it should \
adjust the due date accordingly. For example, if an item is due on "Wednesday" and the \
week is "Week of 9/6/2023", then the due date should be "9/8/2023".
If many due dates fall on the same day, try to distribute them before the due date \
for a more even workload.
The distributed/adjusted due date should never be after the original due date.
Please do so and send it back to me, making sure it conforms to format A.
Include all the valid types, including all valid homework assignments. Do not stop \
until you have included all valid types.
"""

# Step 2: Copy the output into the file schedule.json, making sure it is valid JSON

# Step 3: Fill out the variables in .env

# Step 4: Run this file which will add your schedule items to Notion


# ---------------------------------- #

# Load environment variables from .env
load_dotenv()
NOTION_API_TOKEN = os.getenv("NOTION_API_TOKEN")
SCHEDULE_DATABASE_ID = os.getenv("SCHEDULE_DATABASE_ID")
CLASSES_DATABASE_ID = os.getenv("CLASSES_DATABASE_ID")

# Initialize Notion client
notion = Client(
    auth=NOTION_API_TOKEN,
    # log_level=logging.DEBUG
)

with open("schedule.json", "r") as f:
    schedule_data = json.load(f)


# Function to find and return the class row that matches the course name
def find_class_row(course_name):
    results = notion.databases.query(
        database_id=CLASSES_DATABASE_ID,
        filter={"property": "Name", "rich_text": {"equals": course_name}},
    )
    if results["results"]:
        return results["results"][0]["id"]
    return None


# Function to set the icon based on the type
def get_icon_for_type(type_name):
    icons = {
        "Assignment": "📝",
        "Reading": "📚",
        "Notes": "📒",
        "Essay": "📄",
        "Group Work": "👥",
        "Project": "📁",
        "Presentation": "📊",
        "Study": "☁️",
        "Quiz": "📓",
        "Exam": "🏁",
    }
    return icons.get(type_name, "📋")


for entry in schedule_data:
    # Link to the correct class
    course_name = entry["Course"]
    class_row_id = find_class_row(course_name)

    # # make sure everything is ready
    # print(f"Title: {entry['title']}")
    # print(f"Course: {course_name}")
    # print(f"Type: {entry['Type']}")
    # print(f"Due date: {entry['Due date']}")
    # print(f"Note: {entry['Note']}")
    # print(f"Class row id: {class_row_id}")
    # exit()

    # Get the icon for the type
    icon = get_icon_for_type(entry["Type"])

    # Create the new row
    notion.pages.create(
        parent={"database_id": SCHEDULE_DATABASE_ID},
        properties={
            "title": {"title": [{"text": {"content": entry["title"]}}]},
            "Type": {"select": {"name": entry["Type"]}},
            "Due date": {"date": {"start": entry["Due date"]}},
            "Note": {"rich_text": [{"text": {"content": entry["Note"]}}]},
            "automatic?": {"checkbox": True},
            "Course": {"relation": [{"id": class_row_id}]},
        },
        icon={"type": "emoji", "emoji": icon},
    )
    print(f"Added {icon} {entry['title']} to Notion database successfully!")

print("Schedule added to Notion database successfully!")
