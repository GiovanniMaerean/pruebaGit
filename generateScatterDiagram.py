import os
from github import Github
import matplotlib.pyplot as plt

token = os.getenv('GITHUB_TOKEN')
repo_name = "GiovanniMaerean/pruebaGit"

g = Github(token)
repo = g.get_repo(repo_name)


def main() -> None:
    commits = repo.get_commits()

    lines_added_per_commit = []
    files_modified_per_commit = []

    for commit in commits:
        print(commit.raw_data)
        files = commit.files
        lines_added = 0
        files_modified = 0

        for file in files:
            files_modified += 1
            lines = file.raw_data.get('additions', 0)

            lines_added += lines

        lines_added_per_commit.append(lines_added)
        files_modified_per_commit.append(files_modified)



    plt.figure(figsize=(10, 6))
    plt.scatter(lines_added_per_commit, files_modified_per_commit)

    plt.xlabel('Lines added')
    plt.ylabel('Files modified')
    plt.title('Scatter Diagram of Lines added and Files modified')
    plt.grid(True)

    plt.savefig("scatter_diagram_commits.png")


if __name__ == '__main__':
    main()
