CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status ENUM(
        'pending',
        'in_progress',
        'done'
    ) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO tasks (title, description, status)
VALUES
    (
        'Deploy application',
        'Deploy application using Docker Compose',
        'pending'
    ),
    (
        'Configure monitoring',
        'Install Prometheus and Grafana',
        'in_progress'
    ),
    (
        'Create database',
        'Configure MariaDB',
        'done'
    );