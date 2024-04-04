import os
from github import Github
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Token de autenticación de GitHub
token = os.getenv('GITHUB_TOKEN')

# Nombre del repositorio en formato "username/repository"
repo_name = "arnaums02/Joint-Project---Grup-B"

# Inicialización de la instancia de Github
g = Github(token)

# Obtener el repositorio
repo = g.get_repo(repo_name)

# Listas para almacenar los datos de las issues
open_issue_created_dates = []
closed_issue_closed_dates = []
open_issue_count = []
closed_issue_count = []


def main() -> None:
    get_data()
    generate_burndown_chart()
    generate_burnup_chart()


def get_data() -> None:
    """Obtener los datos de las issues"""
    open_issues = list(repo.get_issues(state='open'))
    for issue in open_issues:
        open_issue_created_dates.append(issue.created_at.date())
    open_issue_count.append(len(open_issues))

    # Obtener todas las issues cerradas
    closed_issues = list(repo.get_issues(state='closed'))
    for issue in closed_issues:
        closed_issue_closed_dates.append(issue.closed_at.date())
    closed_issue_count.append(len(closed_issues))


def generate_burndown_chart() -> None:
    """Generar y guardar el diagrama de Burn-down"""
    plt.figure(figsize=(10, 6))
    dates = sorted(open_issue_created_dates + closed_issue_closed_dates)
    remaining_issues = [sum(1 for d in dates if d <= date) for date in dates]
    plt.plot(dates, remaining_issues, color='red', label='Remaining Issues')
    plt.xlabel('Fecha')
    plt.ylabel('Número de Issues Restantes')
    plt.title('Diagrama de Burn-down')
    plt.legend()
    plt.grid(True)
    plt.savefig("burn_down_chart.png")


def generate_burnup_chart() -> None:
    """Generar y guardar el diagrama de Burn-up"""
    plt.figure(figsize=(10, 6))
    dates = sorted(open_issue_created_dates + closed_issue_closed_dates)
    plt.plot(dates, open_issue_count, color='blue', label='Issues Abiertas')
    plt.plot(dates, closed_issue_count, color='green', label='Issues Cerradas')
    plt.xlabel('Fecha')
    plt.ylabel('Número de Issues')
    plt.title('Diagrama de Burn-up')
    plt.legend()
    plt.grid(True)
    plt.savefig("burn_up_chart.png")


if __name__ == '__main__':
    main()
