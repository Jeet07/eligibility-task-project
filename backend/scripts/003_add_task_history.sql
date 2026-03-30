-- Migration 003 - Task history tracking
CREATE TABLE IF NOT EXISTS task_history (
    id SERIAL PRIMARY KEY,
    task_id INTEGER REFERENCES tasks(id),
    changed_by INTEGER REFERENCES users(id),
    old_status VARCHAR(50),
    new_status VARCHAR(50),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_task_history_task ON task_history(task_id);
