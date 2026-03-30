#!/usr/bin/env python3
import sys
import os
sys.path.append('/app')

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migrations():
    try:
        conn = psycopg2.connect(
            host="15.206.178.183",
            user="taskdb",
            password="bdksat7",
            database="taskdb"
        )
        conn.autocommit = False
        cursor = conn.cursor()
        
        # Create migrations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS migrations (
                id SERIAL PRIMARY KEY,
                migration_name VARCHAR(255) UNIQUE NOT NULL,
                run_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        
        migrations = [
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                role VARCHAR(50) DEFAULT 'User',
                department VARCHAR(100),
                experience INTEGER DEFAULT 0,
                location VARCHAR(255),
                active_tasks INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                status VARCHAR(50) DEFAULT 'Todo',
                priority VARCHAR(50),
                due_date TIMESTAMP,
                rules JSONB,
                assigned_to INTEGER REFERENCES users(id),
                created_by INTEGER REFERENCES users(id),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS task_assignments (
                id SERIAL PRIMARY KEY,
                task_id INTEGER REFERENCES tasks(id) ON DELETE CASCADE,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                eligible BOOLEAN DEFAULT FALSE,
                assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)",
            "CREATE INDEX IF NOT EXISTS idx_users_department ON users(department)",
            "CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)",
            "CREATE INDEX IF NOT EXISTS idx_tasks_assigned_to ON tasks(assigned_to)",
            "CREATE INDEX IF NOT EXISTS idx_task_assignments_task_user ON task_assignments(task_id, user_id)",
        ]
        
        for migration in migrations:
            cursor.execute(migration)
            logger.info("✅ Ran migration")
        
        conn.commit()
        cursor.close()
        conn.close()
        
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    run_migrations()
