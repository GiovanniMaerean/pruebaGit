import os
from github import Github
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Obtener el token de acceso a GitHub
token = os.getenv('GITHUB_TOKEN')

# Nombre del repositorio
repo_name = "arnaums02/Joint-Project---Grup-B"

# Crear una instancia de la clase Github
g = Github(token)

# Obtener el repositorio
repo = g.get_repo(repo_name)

# Definir rango de fechas desde el 12 de marzo de 2024 hasta el 4 de abril de 2024
start_date = datetime(2024, 3, 12)  # Convertido a objeto datetime
end_date = datetime(2024, 4, 4)  # Convertido a objeto datetime

# Obtener todas las issues cerradas del repositorio en ese rango de fechas
closed_issues = repo.get_issues(state='closed', since=start_date, sort='updated', direction='asc')

# Obtener la fecha de cierre de cada issue y contarlas por día
issues_data = {}
for issue in closed_issues:
    closed_at = issue.closed_at.date()
    if start_date.date() <= closed_at <= end_date.date():
        issues_data[closed_at] = issues_data.get(closed_at, 0) + 1

# Crear una lista ordenada de las fechas
dates = sorted(issues_data.keys())

# Crear una lista con el número acumulado de issues cerradas por día
cumulative_closed = [issues_data[dates[0]]]
for date in dates[1:]:
    cumulative_closed.append(cumulative_closed[-1] + issues_data[date])

# Obtener el número total de issues cerradas
total_closed_issues = sum(issues_data.values())

# Crear una lista con el número total de issues inicial
total_issues = [total_closed_issues] * len(dates)

# Calcular los días transcurridos desde el inicio del proyecto
days_elapsed = [(date - start_date).days for date in dates]

# Crear el diagrama burn down
plt.plot(dates, total_issues, label='Total de issues')
plt.plot(dates, cumulative_closed, label='Issues cerradas')

plt.xlabel('Fechas')
plt.ylabel('Número de issues')
plt.title('Diagrama Burn Down del Repositorio GitHub')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)  # Rotar etiquetas del eje x para mejor visualización
plt.tight_layout()  # Ajustar el diseño del gráfico para que se muestren todas las etiquetas
plt.savefig("burn_down_chart.png")

plt.show()
