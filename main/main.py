import os
import random
from faker import Faker
import psycopg2
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

db_config = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
}

conn = psycopg2.connect(**db_config)
cursor = conn.cursor()

cursor.execute("SET search_path TO novena;")

fake = Faker()

status_options = ['Pending', 'In Progress', 'Completed', 'On Hold']


project_ids = []
for _ in range(5):  # Exemplo: 5 projetos
    project_name = fake.company()
    status = random.choice(status_options)
    cursor.execute(
        "INSERT INTO project (project_name, project_status) VALUES (%s, %s) RETURNING project_id",
        (project_name, status)
    )
    project_id = cursor.fetchone()[0]
    project_ids.append(project_id)

user_ids = []
for _ in range(15):  # Exemplo: 10 usuários
    user_name = fake.name()
    cursor.execute("INSERT INTO novena.user (user_name) VALUES (%s) RETURNING user_id", (user_name,))
    user_id = cursor.fetchone()[0]
    user_ids.append(user_id)

squad_ids = []
for _ in range(3):
    squad_name = fake.catch_phrase()
    user_id = random.choice(user_ids)
    cursor.execute("INSERT INTO novena.squad (squad_name, user_id) VALUES (%s, %s) RETURNING squad_id", (squad_name, user_id))
    squad_id = cursor.fetchone()[0]
    squad_ids.append(squad_id)  

sprint_ids = []
for _ in range(8):  # Exemplo: 8 sprints
    sprint_name = f"Sprint {fake.word()}"
    project_id = random.choice(project_ids)
    sprint_date_begin = fake.date_time_this_year()
    sprint_date_end = fake.date_time_between_dates(sprint_date_begin, sprint_date_begin + timedelta(days=14))
    cursor.execute(
        "INSERT INTO novena.sprint (sprint_name, project_id, sprint_date_begin, sprint_date_end) VALUES (%s, %s, %s, %s) RETURNING sprint_id",
        (sprint_name, project_id, sprint_date_begin, sprint_date_end)
    )
    sprint_id = cursor.fetchone()[0]
    sprint_ids.append(sprint_id)

for _ in range(20):  # Exemplo: 20 tarefas
    task_name = fake.bs()
    sprint_id = random.choice(sprint_ids)
    user_id = random.choice(user_ids)
    status = random.choice(status_options)
    cursor.execute(
        "INSERT INTO task (task_name, sprint_id, user_id, task_status) VALUES (%s, %s, %s, %s)",
        (task_name, sprint_id, user_id, status)
    )

conn.commit()
cursor.close()
conn.close()