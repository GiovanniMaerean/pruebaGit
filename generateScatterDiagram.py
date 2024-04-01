import os
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


def get_data() -> None:
    commits = repo.get_commits()

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
    plt.title('Scatter Diagram of Lines added and Files modified')
    plt.grid(True)

    plt.savefig("scatter_diagram_commits.png")


if __name__ == '__main__':
    main()
