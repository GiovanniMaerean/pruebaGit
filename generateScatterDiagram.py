import os
from github import Github
import matplotlib.pyplot as plt

token = os.getenv('GITHUB_TOKEN')
repo_name = "GiovanniMaerean/pruebaGit"

g = Github(token)
repo = g.get_repo(repo_name)


def main() -> None:
    issues = repo.get_issues()
    priorities = []
    estimations = []

    for issue in issues:

        if 'priority' in issue.raw_data['fields']:
            priority = issue.raw_data['fields']['priority']
            priorities.append(priority)
        if 'estimate' in issue.raw_data['fields']:
            estimate = issue.raw_data['fields']['estimate']
            estimations.append(estimate)

    plt.figure(figsize=(10, 6))
    plt.scatter(estimations, priorities, color='blue', alpha=0.5)

    plt.xlabel('Estimation')
    plt.ylabel('Priority')
    plt.title('Scatter Diagram of Estimations and Priorities')
    plt.grid(True)

    plt.savefig("scatter_diagram_issues.png")


if __name__ == '__main__':
    main()
