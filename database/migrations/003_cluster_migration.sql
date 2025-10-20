-- Cluster table migration
-- This migration adds the cluster table to the database

CREATE TABLE IF NOT EXISTS cluster (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    user_id INTEGER NOT NULL,
    project_id INTEGER,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_user_id ON cluster(user_id);
CREATE INDEX IF NOT EXISTS idx_project_id ON cluster(project_id);

-- Update the last_updated_time trigger
CREATE TRIGGER IF NOT EXISTS update_cluster_timestamp 
    AFTER UPDATE ON cluster
    FOR EACH ROW
    BEGIN
        UPDATE cluster SET last_updated_time = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;
