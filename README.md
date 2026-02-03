# 📆 Notion Schedule Script

This script automates the process of transferring course schedules (assignments, exams, readings) from a raw syllabus into your Notion database. It utilizes ChatGPT to parse unstructured text into JSON, and then uses the Notion API to populate your workspace.

## Requirements

* Python 3.7+
* A Notion Integration Token (created at [notion.so/my-integrations](https://www.notion.so/my-integrations))

## Setup

### 1. Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/yourusername/notion-schedule-automator.git
cd notion-schedule-automator
pip install notion-client python-dotenv
```

### 2. Notion Database Configuration

Your Notion setup must match the script's expectations. You need two databases:

**A. Classes Database**

* **Property:** `Name` (Title)

**B. Schedule Database**

* **Property:** `title` (Title)
* **Property:** `Type` (Select) - *Options: Assignment, Reading, Notes, Essay, Group Work, Project, Presentation, Video Lecture, Study, Quiz, Exam, Lab.*
* **Property:** `Due date` (Date)
* **Property:** `Notes` (Text)
* **Property:** `automatic?` (Checkbox)
* **Property:** `Course` (Relation) - *Linked to the Classes Database.*

### 3. Environment Variables

Create a `.env` file in the root directory and add your Notion credentials:

```ini
NOTION_API_TOKEN=secret_your_token_here
SCHEDULE_DATABASE_ID=your_schedule_database_id
CLASSES_DATABASE_ID=your_classes_database_id
```

> You can find the Database ID in the URL of your Notion database page: `https://notion.so/workspace/{DATABASE_ID}?v=...`

## Usage

### Step 1: Parse Syllabus

The script relies on a strictly formatted JSON file. Copy the prompt below, fill in the `{brackets}`, and paste it into an LLM along with your syllabus text.

<details>
<summary><strong>Click to view the Prompt</strong></summary>

````text
This is for course: {course name}
The year is: {year}

This is format A:
```py
    [
        {
            "title": _____, # title of the item, try it to keep it short yet descriptive, otherwise overfill to "Note"
            "Course": ___ ___, # Course name in format '{one word} {3 numbers}'"
            "Type": _____, # can be one of ONLY "Assignment", "Video Lecture", "Reading", "Notes", "Essay", "Group Work", "Project", "Presentation", "Study", "Quiz", or "Exam"
            "Due date": _____, # Due date of the item in "%Y-%m-%d" format
            "Note": _____, # usually blank, only fill in if necessary
        }
    ]

```

I want to convert the following schedule into format A:

```
{paste schedule here}

```

Only include items that have a valid "Type" that can be assigned. This means don't include activities occurring during that day in lab, lectures, etc.
If week of an item is provided along with the day of the week it is due, it should adjust the due date accordingly. For example, if an item is due on "Wednesday" and the week is "Week of 9/6/2023", then the due date should be "9/8/2023".
If many due dates fall on the same day, try to distribute them before the due date for a more even workload.
The distributed/adjusted due date should never be after the original due date.
Please do so and send it back to me, making sure it conforms to format A.
Include all the valid types, including all valid homework assignments. Do not stop until you have included all valid types.
Do not add comments. I want a clean JSON output.

````
</details>

### Step 2: Save the Data
Copy the JSON response from LLM and save it into a file named `schedule.json` in the project root.

### Step 3: Run the Script
Execute the Python script to upload the items to Notion:

```bash
python main.py

```

## Troubleshooting

* **"Could not find class X in Notion database!"**: Ensure the "Course" value in your `schedule.json` matches the text in the "Name" property of your Classes database *exactly*.
* **404 / API Errors**: Double-check that your Internal Integration has been given access to *both* databases (click the `...` menu on the database page -> Connections -> Add your integration).
