-- Criando a tabela user
CREATE TABLE novena.user (
    user_id SERIAL PRIMARY KEY,
    user_name VARCHAR(255) NOT NULL
);

-- Criando a tabela project
CREATE TABLE novena.project (
    project_id SERIAL PRIMARY KEY,
    project_name VARCHAR(255) NOT null,
    project_status VARCHAR(20) not null
);

-- Criando a tabela squad
CREATE TABLE novena.squad (
    squad_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES novena.user(user_id),
    squad_name VARCHAR(255) NOT NULL
);

-- Criando a tabela sprint
CREATE TABLE novena.sprint (
    sprint_id SERIAL PRIMARY KEY,
    project_id INT REFERENCES novena.project(project_id),
    sprint_name VARCHAR(255) NOT NULL,
    sprint_date_begin TIMESTAMP,
    sprint_date_end TIMESTAMP
);

-- Criando a tabela task
CREATE TABLE novena.task (
    task_id SERIAL PRIMARY KEY,
    sprint_id INT REFERENCES novena.sprint(sprint_id),
    user_id INT REFERENCES novena.user(user_id),
    task_name VARCHAR(255) NOT null,
    task_status VARCHAR(20) not NULL
);
