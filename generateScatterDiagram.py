import os
from datetime import datetime
from github import Github
import matplotlib.pyplot as plt

# Token de autenticación de GitHub
token = os.getenv('GITHUB_TOKEN')

# Nombre del repositorio en formato "username/repository"
repo_name = "arnaums02/Joint-Project---Grup-B"

# Inicialización de la instancia de Github
g = Github(token)

# Obtener el repositorio
repo = g.get_repo(repo_name)

# Listas para almacenar los datos de las issues
days_to_close = []
issue_created_dates = []


def main() -> None:
    get_data()
    generate_diagram()


def get_data() -> None:
    """Obtener los datos de las issues"""
    issues = repo.get_issues(state='closed')  # Obtener todas las issues cerradas

    for issue in issues:
        print(issue.raw_data)
        created_at = issue.created_at
        closed_at = issue.closed_at

        # Calcular los días que se tardaron en cerrar la issue
        if closed_at is not None:
            time_to_close = (closed_at - created_at).days
            days_to_close.append(time_to_close)
            issue_created_dates.append(created_at)


def generate_diagram() -> None:
    """Generar y guardar el scatter diagram"""
    plt.figure(figsize=(10, 6))

    plt.scatter(issue_created_dates, days_to_close, color='blue', alpha=0.7)

    plt.xlabel('Fecha de creación de la issue')
    plt.ylabel('Días para cerrar la issue')
    plt.title('Tiempo para cerrar las issues')
    plt.grid(True)

    plt.savefig("scatter_diagram_issues.png")


if __name__ == '__main__':
    main()
