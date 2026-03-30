-- Migration 004 - Add performance indexes

-- Create indexes for better query performance
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_tasks_created_at ON tasks(created_at);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_created_at ON users(created_at);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_task_assignments_created ON task_assignments(assigned_at);

-- Add partial index for active tasks
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_tasks_active ON tasks(status) WHERE status != 'Done';

-- Add composite index for common queries
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_tasks_status_priority ON tasks(status, priority);

-- Analyze tables to update statistics
ANALYZE tasks;
ANALYZE users;
ANALYZE task_assignments;

-- Record migration
INSERT INTO migrations (migration_name) VALUES ('004_add_indexes.sql');
