import os
from datetime import datetime, timezone, timedelta
from github import Github
import matplotlib.pyplot as plt

# Token de autenticación de GitHub
token = os.getenv('GITHUB_TOKEN')

# Nombre del repositorio en formato "username/repository"
repo_name = "GiovanniMaerean/pruebaGit"

# Inicialización de la instancia de Github
g = Github(token)

# Obtener el repositorio
repo = g.get_repo(repo_name)

days_to_close = []
issue_created_dates = []

def main() -> None:
    get_data()
    generate_diagram()

def get_date_range_of_current_week() -> tuple:
    """Obtener el rango de fechas de la semana actual desde el lunes hasta el domingo como objetos datetime, haciéndolos conscientes de la zona horaria."""
    current_date = datetime.now(timezone.utc)
    start_of_week = current_date - timedelta(days=current_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    start_of_week = datetime.combine(start_of_week.date(), datetime.min.time(), tzinfo=timezone.utc)
    end_of_week = datetime.combine(end_of_week.date(), datetime.max.time(), tzinfo=timezone.utc)
    return start_of_week, end_of_week

def get_data() -> None:
    """Obtener los datos de las issues"""
    issues = repo.get_issues(state='closed', since=start_of_week)

    for issue in issues:
        closed_at = issue.closed_at

        # Verificar si la issue se cerró durante la semana actual
        if closed_at is not None and start_of_week <= closed_at <= end_of_week:
            created_at = issue.created_at
            time_to_close = (closed_at - created_at).days
            days_to_close.append(time_to_close)
            issue_created_dates.append(created_at)


def generate_diagram() -> None:
    """Generar y guardar el scatter diagram con todos los datos"""
    plt.figure(figsize=(10, 6))

    plt.scatter(days_to_close, issue_created_dates, color='blue', alpha=0.7)

    plt.xlabel('Días para cerrar la issue')
    plt.ylabel('Fecha de creación de la issue')
    plt.title(f'Scatter Diagram of closed issues - {get_date()}')
    plt.grid(True)

    plt.savefig("scatter_diagram_issues_weekly.png")
    plt.show()

def get_date() -> str:
    """El formato es: MX-WY-Report -> donde X es el número de mes y Y es el número de semana"""
    now = datetime.now()
    month = now.strftime("%m")
    week_of_year = int(now.strftime("%U"))
    first_day_of_month = now.replace(day=1)
    week_of_first_day = int(first_day_of_month.strftime("%U"))
    week_of_month = week_of_year - week_of_first_day + 1
    return f"M{month}-W{week_of_month}-Report"

if __name__ == '__main__':
    main()
