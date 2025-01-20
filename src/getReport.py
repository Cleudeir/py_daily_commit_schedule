import json
from datetime import datetime, timedelta

def getReport():
    # Load the grouped commits from the JSON file
    with open("src/output/grouped_commits.json", "r", encoding="utf-8") as json_file:
        grouped_commits = json.load(json_file)

    # Define the work schedule
    work_start = datetime.strptime("09:00 AM", "%I:%M %p")
    lunch_start = datetime.strptime("13:00", "%H:%M")
    lunch_end = datetime.strptime("14:00", "%H:%M")
    work_end = datetime.strptime("18:00", "%H:%M")

    def parse_commit_time(commit_time):
        """Parse commit time, handling the 'Z' as UTC timezone."""
        if commit_time.endswith('Z'):
            # Replace 'Z' with '+00:00' to make it compatible with fromisoformat
            commit_time = commit_time[:-1] + '+00:00'
        return datetime.fromisoformat(commit_time)

    def create_daily_schedule(dayCommit, commits):
        """
        Creates a daily schedule string for all commits on a given date.

        Args:
            dayCommit: The date for the schedule (string in "YYYY-MM-DD" format).
            commits: A list of all commits on the given date.

        Returns:
            A string containing the daily schedule for all commits.
        """

        schedule = {}  # Use a dictionary to group commits by project
        commits = sorted(commits, key=lambda commit: parse_commit_time(commit['time']['datetime']))

        for i in range(len(commits)):
            previous_commit = None
            commit = commits[i]
            if i > 0:
                previous_commit = commits[i - 1]

            start_active = "**"
            if previous_commit is not None:
                start_active = parse_commit_time(previous_commit['time']['datetime']).strftime('%H:%M')

            end_active = parse_commit_time(commit['time']['datetime']).strftime('%H:%M')
            description = commit['commit']['description']
            project = "/".join(commit['commit']['href'].split("/")[2:3])  # Fix: Assuming this is how you get the project name

            if project not in schedule:
                schedule[project] = []
            schedule[project].append(
                f"{start_active} - {end_active} : \"{description}\""
            )

        return schedule

    # Generate the daily schedule for each date
    report_lines = []
    for date, commits in grouped_commits.items():
        # Convert date format to dd/mm/yyyy
        formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y")
        dayCommit = grouped_commits[date]
        report_lines.append(f"Date: {formatted_date}")
        daily_schedule = create_daily_schedule(dayCommit, commits)
        for project, activities in daily_schedule.items():
            for activity in activities:
                report_lines.append(f"    {project}: {activity}")
        report_lines.append("")  # Add a blank line between dates

    # Save the report to a file
    report_content = "\n".join(report_lines)
    with open("src/output/daily_commit_schedule.txt", "w", encoding="utf-8") as report_file:
        report_file.write(report_content)

    print("Daily commit schedule has been saved to 'daily_commit_schedule.txt'")