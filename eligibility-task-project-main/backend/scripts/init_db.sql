CREATE INDEX idx_user_department ON users(department);
CREATE INDEX idx_user_experience ON users(experience);
CREATE INDEX idx_task_status ON tasks(status);
CREATE INDEX idx_task_assigned_to ON tasks(assigned_to);
CREATE INDEX idx_taskassignment_task_user ON task_assignments(task_id, user_id);
CREATE INDEX idx_taskassignment_eligible ON task_assignments(eligible);
CREATE INDEX idx_user_active_tasks ON users(active_tasks);
