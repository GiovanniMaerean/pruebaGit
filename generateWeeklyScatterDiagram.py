import os
import os
from datetime import datetime, timezone, timedelta

from github import Github
import matplotlib.pyplot as plt

token = os.getenv('GITHUB_TOKEN')
repo_name = "GiovanniMaerean/pruebaGit"

g = Github(token)
repo = g.get_repo(repo_name)

lines_added_per_commit = []
files_modified_per_commit = []


def main() -> None:
    get_data()
    generate_diagram()


def get_date_range_of_current_week() -> tuple:
    """Gets the date range of the current week from Monday to Sunday as datetime objects, making them timezone aware."""
    current_date = datetime.now(timezone.utc)
    start_of_week = current_date - timedelta(days=current_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    start_of_week = datetime.combine(start_of_week.date(), datetime.min.time(), tzinfo=timezone.utc)
    end_of_week = datetime.combine(end_of_week.date(), datetime.max.time(), tzinfo=timezone.utc)
    return start_of_week, end_of_week


def get_data() -> None:
    start_of_week, end_of_week = get_date_range_of_current_week()
    commits = repo.get_commits(since=start_of_week)

    for commit in commits:
        lines_added = commit.stats.additions
        files_modified = len(commit.files)

        lines_added_per_commit.append(lines_added)
        files_modified_per_commit.append(files_modified)


def generate_diagram() -> None:
    plt.figure(figsize=(10, 6))
    plt.scatter(lines_added_per_commit, files_modified_per_commit)

    plt.xlabel('Lines added')
    plt.ylabel('Files modified')
    plt.title(f'Scatter Diagram of Lines added and Files modified - {get_date()}')
    plt.grid(True)

    plt.savefig("scatter_diagram_commits_weekly.png")


def get_date() -> str:
    """The format is: MX-WY-Report -> where X is the month number and Y is the week number"""
    now = datetime.now()
    month = now.strftime("%m")
    week_of_year = int(now.strftime("%U"))
    first_day_of_month = now.replace(day=1)
    week_of_first_day = int(first_day_of_month.strftime("%U"))
    week_of_month = week_of_year - week_of_first_day + 1
    return f"M{month}-W{week_of_month}-Report"


if __name__ == '__main__':
    main()
