-- Migration script to add TaskQueue table for task scheduling and concurrency control
-- This script creates the task_queue table and related indexes

-- Start transaction
BEGIN;

-- Create TaskQueue table
CREATE TABLE IF NOT EXISTS task_queue (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'queued',
    priority INTEGER NOT NULL DEFAULT 5,
    task_config JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    started_at TIMESTAMP WITH TIME ZONE NULL,
    completed_at TIMESTAMP WITH TIME ZONE NULL,
    retry_count INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,
    error_message TEXT NULL,
    external_task_id VARCHAR(100) NULL,

    -- Foreign key constraint
    CONSTRAINT fk_task_queue_project
        FOREIGN KEY (project_id)
        REFERENCES projects(id)
        ON DELETE CASCADE,

    -- Check constraints
    CONSTRAINT chk_status
        CHECK (status IN ('queued', 'running', 'completed', 'failed', 'cancelled')),

    CONSTRAINT chk_priority
        CHECK (priority >= 1 AND priority <= 10),

    CONSTRAINT chk_retry_count
        CHECK (retry_count >= 0 AND retry_count <= max_retries)
);

-- Create indexes for optimized querying
CREATE INDEX IF NOT EXISTS idx_queue_order
    ON task_queue (status, priority, created_at);

CREATE INDEX IF NOT EXISTS idx_project_queue
    ON task_queue (project_id, status);

CREATE INDEX IF NOT EXISTS idx_task_status
    ON task_queue (status);

CREATE INDEX IF NOT EXISTS idx_external_task
    ON task_queue (external_task_id)
    WHERE external_task_id IS NOT NULL;

-- Add comments for documentation
COMMENT ON TABLE task_queue IS 'Task queue for managing training task scheduling and concurrency control';
COMMENT ON COLUMN task_queue.status IS 'Task status: queued, running, completed, failed, cancelled';
COMMENT ON COLUMN task_queue.priority IS 'Task priority (1-10, lower number = higher priority)';
COMMENT ON COLUMN task_queue.task_config IS 'Task configuration stored as JSON';
COMMENT ON COLUMN task_queue.retry_count IS 'Current number of retries';
COMMENT ON COLUMN task_queue.max_retries IS 'Maximum allowed retries';
COMMENT ON COLUMN task_queue.external_task_id IS 'External task ID from training API';

-- Create function to automatically set started_at when status changes to running
CREATE OR REPLACE FUNCTION set_task_started_at()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'running' AND OLD.status != 'running' AND NEW.started_at IS NULL THEN
        NEW.started_at = NOW();
    END IF;

    IF NEW.status IN ('completed', 'failed', 'cancelled') AND OLD.status NOT IN ('completed', 'failed', 'cancelled') AND NEW.completed_at IS NULL THEN
        NEW.completed_at = NOW();
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to automatically set timestamps
DROP TRIGGER IF EXISTS trigger_set_task_timestamps ON task_queue;
CREATE TRIGGER trigger_set_task_timestamps
    BEFORE UPDATE ON task_queue
    FOR EACH ROW
    EXECUTE FUNCTION set_task_started_at();

-- Create function to prevent multiple running tasks for the same project
CREATE OR REPLACE FUNCTION check_project_concurrency()
RETURNS TRIGGER AS $$
BEGIN
    -- Only check when inserting or updating to 'running' status
    IF (TG_OP = 'INSERT' AND NEW.status = 'running') OR
       (TG_OP = 'UPDATE' AND NEW.status = 'running' AND OLD.status != 'running') THEN

        -- Check if project already has a running task
        IF EXISTS (
            SELECT 1 FROM task_queue
            WHERE project_id = NEW.project_id
              AND status = 'running'
              AND id != NEW.id
        ) THEN
            RAISE EXCEPTION 'Project % already has a running task', NEW.project_id;
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to enforce project concurrency
DROP TRIGGER IF EXISTS trigger_check_project_concurrency ON task_queue;
CREATE TRIGGER trigger_check_project_concurrency
    BEFORE INSERT OR UPDATE ON task_queue
    FOR EACH ROW
    EXECUTE FUNCTION check_project_concurrency();

-- Insert some sample data for testing (optional)
-- This section can be removed in production
DO $$
BEGIN
    -- Only insert sample data if the projects table has data
    IF EXISTS (SELECT 1 FROM projects LIMIT 1) THEN
        -- Insert a sample queued task
        INSERT INTO task_queue (project_id, status, priority, task_config)
        SELECT
            id,
            'queued',
            5,
            '{"sample": true, "description": "Sample task for testing"}'::jsonb
        FROM projects
        LIMIT 1
        ON CONFLICT DO NOTHING;

        RAISE NOTICE 'Sample task queue data inserted for testing';
    END IF;
END
$$;

-- Create view for queue statistics
CREATE OR REPLACE VIEW task_queue_stats AS
SELECT
    status,
    COUNT(*) as count,
    AVG(priority) as avg_priority,
    MIN(created_at) as oldest_task,
    MAX(created_at) as newest_task
FROM task_queue
GROUP BY status
ORDER BY status;

COMMENT ON VIEW task_queue_stats IS 'Statistics view for task queue status breakdown';

-- Commit transaction
COMMIT;

-- Verify the migration
SELECT
    'Task Queue Migration Verification' as verification_step,
    'SUCCESS' as status,
    COUNT(*) as task_count
FROM task_queue;

-- Display table structure
SELECT
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = 'task_queue'
  AND table_schema = 'public'
ORDER BY ordinal_position;