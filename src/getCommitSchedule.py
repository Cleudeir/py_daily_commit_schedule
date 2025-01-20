import os
import re
import json
from datetime import datetime, timedelta
from collections import defaultdict
import json

def getCommitSchedule():
    # Read the HTML content from the "index.html" file
    with open("src/input/index.html", "r", encoding="utf-8") as file:
        html = file.read()

    # Regular expression to extract necessary data
    regex = re.compile(
        r'<time.*?title="([^"]*)".*?datetime="([^"]*)".*?>.*?'  # Time data
        r'<a.*?href="([^"]*)".*?>(.*?)<\/a>.*?'  # Branch data
        r'<a.*?title="([^"]*)".*?href="([^"]*)">.*?project-name">(.*?)<\/span><\/a>.*?'  # Repository data
        r'<li.*?commit-sha".*?href="([^"]*)">(.*?)<\/a>.*?·\s*(.*?)\s*</div>',  # Commit data, including description
        re.DOTALL
    )

    # Find all matches
    matches = regex.findall(html)

    # Extract and organize data
    grouped_commits = defaultdict(list)

    for match in matches:
        # Parse the datetime field to extract the date (YYYY-MM-DD)
        commit_date = datetime.strptime(match[1], "%Y-%m-%dT%H:%M:%SZ").date().isoformat()

        # Organize commit data
        commit_data = {
            "time": {
                "title": match[0],
                "datetime": match[1]
            },
            "branch": {
                "href": match[2],
                "name": match[3]
            },
            "repository": {
                "title": match[4],
                "href": match[5],
                "name": match[6]
            },
            "commit": {
                "href": match[7],
                "sha": match[8],
                "description": match[9].strip()
            }
        }

        # Group the commit by its date
        grouped_commits[commit_date].append(commit_data)

    # Convert the defaultdict to a regular dictionary for JSON serialization
    grouped_commits = dict(grouped_commits)

    # Save grouped commits to a JSON file
    with open("src/output/grouped_commits.json", "w", encoding="utf-8") as json_file:
        json.dump(grouped_commits, json_file, indent=4, ensure_ascii=False)

    print(f"Grouped commits by date have been saved to 'grouped_commits.json'")