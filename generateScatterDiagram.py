import os
from datetime import datetime
from github import Github
import matplotlib.pyplot as plt

# This code generates a scatter diagram with all the
# commits of the repository, showing the added lines and
# the modified files. It has to be executed manually
# using the "scatterGeneralReportGenerator.yml" workflow

token = os.getenv('GITHUB_TOKEN')

repo_name = "arnaums02/Joint-Project---Grup-B"

g = Github(token)
repo = g.get_repo(repo_name)

days_to_close = []
issue_created_dates = []

def main() -> None:
    get_data()
    generate_diagram()

def get_data() -> None:
     """Gets all the closed issues with their open date and time to close"""
    issues = repo.get_issues(state='closed')

    for issue in issues:
        created_at = issue.created_at
        closed_at = issue.closed_at

        if closed_at is not None:
            time_to_close = (closed_at - created_at).days
            days_to_close.append(time_to_close)
            issue_created_dates.append(created_at)

def generate_diagram() -> None:
    """Generates and saves the scatter diagram with all the data"""
    plt.figure(figsize=(10, 6))

    plt.scatter(days_to_close, issue_created_dates, color='blue', alpha=0.7)

    plt.xlabel('Días para cerrar la issue')
    plt.ylabel('Fecha de creación de la issue')
    plt.title('Tiempo para cerrar las issues')
    plt.grid(True)

    plt.savefig("scatter_diagram_issues.png")

if __name__ == '__main__':
    main()

