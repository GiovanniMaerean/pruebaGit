import os
import matplotlib.pyplot as plt
from github import Github

token = os.getenv('GITHUB_TOKEN')

repo_name = "arnaums02/Joint-Project---Grup-B"

g = Github(token)
repo = g.get_repo(repo_name)

dates = []
completed_count = []


def main() -> None:
    get_data()
    generate_burndown()


def get_data() -> None:
    """Gets the count of completed issues on each day"""
    issues = repo.get_issues(state='closed')
    current_date = None
    count = 0

    for issue in issues:
        closed_at = issue.closed_at.date()

        # If it's a new date, add the previous date and count to the lists
        if closed_at != current_date:
            if current_date is not None:
                dates.append(current_date)
                completed_count.append(count)
            current_date = closed_at
            count = 0

        count += 1

    # Add the last date and count
    if current_date is not None:
        dates.append(current_date)
        completed_count.append(count)


def generate_burndown() -> None:
    """Generates and saves the burndown chart"""
    plt.figure(figsize=(10, 6))

    total_issues = sum(completed_count)
    remaining_issues = total_issues

    for i in range(len(dates)):
        remaining_issues -= completed_count[i]
        plt.plot(dates[i:], [remaining_issues] * len(dates[i:]), label='Ideal Progress', linestyle='--')

    plt.plot(dates, [total_issues - x for x in completed_count], marker='o', color='blue', label='Actual Progress')

    plt.xlabel('Date')
    plt.ylabel('Remaining Issues')
    plt.title('Burndown Chart')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig("burndown_chart.png")


if __name__ == '__main__':
    main()
