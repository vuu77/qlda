IF DB_ID('ITProjectManagementDB') IS NULL
    CREATE DATABASE ITProjectManagementDB;
GO

USE ITProjectManagementDB;
GO

IF OBJECT_ID('task_schedules', 'U') IS NOT NULL DROP TABLE task_schedules;
IF OBJECT_ID('project_schedules', 'U') IS NOT NULL DROP TABLE project_schedules;
IF OBJECT_ID('tasks', 'U') IS NOT NULL DROP TABLE tasks;
IF OBJECT_ID('projects', 'U') IS NOT NULL DROP TABLE projects;
IF OBJECT_ID('users', 'U') IS NOT NULL DROP TABLE users;
GO

CREATE TABLE users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    full_name NVARCHAR(255) NOT NULL,
    email NVARCHAR(255) NOT NULL UNIQUE,
    password NVARCHAR(255) NOT NULL,
    role NVARCHAR(50) DEFAULT 'member',
    created_at DATETIME DEFAULT GETDATE()
);

CREATE TABLE projects (
    id INT IDENTITY(1,1) PRIMARY KEY,
    project_code NVARCHAR(50) NOT NULL UNIQUE,
    project_name NVARCHAR(255) NOT NULL,
    description NVARCHAR(MAX),
    manager_id INT NOT NULL,
    team_name NVARCHAR(255),
    start_date DATE,
    end_date DATE,
    created_at DATETIME DEFAULT GETDATE(),
    CONSTRAINT FK_projects_users FOREIGN KEY (manager_id) REFERENCES users(id)
);

CREATE TABLE tasks (
    id INT IDENTITY(1,1) PRIMARY KEY,
    project_id INT NOT NULL,
    task_name NVARCHAR(255) NOT NULL,
    description NVARCHAR(MAX),
    assigned_to NVARCHAR(255),
    estimated_expert_hours FLOAT DEFAULT 0,
    actual_hours FLOAT DEFAULT 0,
    hourly_rate FLOAT DEFAULT 0,
    estimated_cost FLOAT DEFAULT 0,
    status NVARCHAR(50) DEFAULT 'pending',
    start_date DATE,
    end_date DATE,
    created_at DATETIME DEFAULT GETDATE(),
    CONSTRAINT FK_tasks_projects FOREIGN KEY (project_id) REFERENCES projects(id)
);

CREATE TABLE project_schedules (
    id INT IDENTITY(1,1) PRIMARY KEY,
    project_id INT NOT NULL,
    milestone_name NVARCHAR(255) NOT NULL,
    start_date DATE,
    end_date DATE,
    note NVARCHAR(MAX),
    CONSTRAINT FK_project_schedules_projects FOREIGN KEY (project_id) REFERENCES projects(id)
);

CREATE TABLE task_schedules (
    id INT IDENTITY(1,1) PRIMARY KEY,
    task_id INT NOT NULL,
    work_date DATE,
    note NVARCHAR(MAX),
    CONSTRAINT FK_task_schedules_tasks FOREIGN KEY (task_id) REFERENCES tasks(id)
);

INSERT INTO users (full_name, email, password, role)
VALUES (N'Admin Project', 'admin@project.local', '123456', 'manager');
GO
