import os
from datetime import datetime
from collections import defaultdict
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

# Diccionario para almacenar el número de issues cerradas por día
issues_closed_per_day = defaultdict(int)


def main() -> None:
    get_data()
    generate_diagram()


def get_data() -> None:
    """Obtener los datos de las issues cerradas por día"""
    issues = repo.get_issues(state='closed')  # Obtener todas las issues cerradas

    for issue in issues:
        created_at = issue.created_at
        closed_at = issue.closed_at

        # Verificar si la issue está cerrada
        if closed_at is not None:
            # Usar la fecha de cierre como clave para el diccionario y aumentar el contador
            issues_closed_per_day[closed_at.date()] += 1


def generate_diagram() -> None:
    """Generar y guardar el diagrama de barras"""
    # Ordenar el diccionario por fecha
    sorted_issues_closed_per_day = dict(sorted(issues_closed_per_day.items()))

    dates = list(sorted_issues_closed_per_day.keys())
    issues_closed = list(sorted_issues_closed_per_day.values())

    plt.figure(figsize=(10, 6))
    plt.bar(dates, issues_closed, color='blue')

    plt.xlabel('Fecha de cierre de la issue')
    plt.ylabel('Número de issues cerradas')
    plt.title('Número de issues cerradas por día')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    plt.savefig("bar_chart_issues_closed_per_day.png")
    plt.show()


if __name__ == '__main__':
    main()
