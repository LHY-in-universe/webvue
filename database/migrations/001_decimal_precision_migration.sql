-- Migration script to convert Float fields to DECIMAL(precision,2) for better numeric precision
-- This script should be run against the EdgeAI database

-- Start transaction
BEGIN;

-- Backup existing data first (optional but recommended)
CREATE TABLE IF NOT EXISTS projects_backup AS SELECT * FROM projects;
CREATE TABLE IF NOT EXISTS models_backup AS SELECT * FROM models;
CREATE TABLE IF NOT EXISTS nodes_backup AS SELECT * FROM nodes;

-- Update Projects table
-- Convert progress from Float to DECIMAL(5,2)
ALTER TABLE projects
    ALTER COLUMN progress TYPE DECIMAL(5,2) USING ROUND(progress::numeric, 2);

-- Update Models table
-- Convert size from Float to DECIMAL(10,2) (for larger file sizes)
ALTER TABLE models
    ALTER COLUMN size TYPE DECIMAL(10,2) USING ROUND(size::numeric, 2);

-- Convert progress from Float to DECIMAL(5,2)
ALTER TABLE models
    ALTER COLUMN progress TYPE DECIMAL(5,2) USING ROUND(progress::numeric, 2);

-- Convert loss from Float to DECIMAL(8,2) (for loss values that might be larger)
ALTER TABLE models
    ALTER COLUMN loss TYPE DECIMAL(8,2) USING ROUND(loss::numeric, 2);

-- Convert accuracy from Float to DECIMAL(5,2)
ALTER TABLE models
    ALTER COLUMN accuracy TYPE DECIMAL(5,2) USING ROUND(accuracy::numeric, 2);

-- Update Nodes table
-- Convert progress from Float to DECIMAL(5,2)
ALTER TABLE nodes
    ALTER COLUMN progress TYPE DECIMAL(5,2) USING ROUND(progress::numeric, 2);

-- Convert cpu_usage from Float to DECIMAL(5,2)
ALTER TABLE nodes
    ALTER COLUMN cpu_usage TYPE DECIMAL(5,2) USING ROUND(cpu_usage::numeric, 2);

-- Convert memory_usage from Float to DECIMAL(5,2)
ALTER TABLE nodes
    ALTER COLUMN memory_usage TYPE DECIMAL(5,2) USING ROUND(memory_usage::numeric, 2);

-- Convert disk_usage from Float to DECIMAL(5,2)
ALTER TABLE nodes
    ALTER COLUMN disk_usage TYPE DECIMAL(5,2) USING ROUND(disk_usage::numeric, 2);

-- Convert sent from Float to DECIMAL(10,2) (for data transfer amounts)
ALTER TABLE nodes
    ALTER COLUMN sent TYPE DECIMAL(10,2) USING ROUND(sent::numeric, 2);

-- Convert received from Float to DECIMAL(10,2) (for data transfer amounts)
ALTER TABLE nodes
    ALTER COLUMN received TYPE DECIMAL(10,2) USING ROUND(received::numeric, 2);

-- Update default values to match new DECIMAL types
ALTER TABLE projects ALTER COLUMN progress SET DEFAULT 0.00;
ALTER TABLE models ALTER COLUMN size SET DEFAULT 0.00;
ALTER TABLE models ALTER COLUMN progress SET DEFAULT 0.00;
ALTER TABLE models ALTER COLUMN loss SET DEFAULT 0.00;
ALTER TABLE models ALTER COLUMN accuracy SET DEFAULT 0.00;
ALTER TABLE nodes ALTER COLUMN progress SET DEFAULT 0.00;
ALTER TABLE nodes ALTER COLUMN cpu_usage SET DEFAULT 0.00;
ALTER TABLE nodes ALTER COLUMN memory_usage SET DEFAULT 0.00;
ALTER TABLE nodes ALTER COLUMN disk_usage SET DEFAULT 0.00;
ALTER TABLE nodes ALTER COLUMN sent SET DEFAULT 0.00;
ALTER TABLE nodes ALTER COLUMN received SET DEFAULT 0.00;

-- Add constraints to ensure values are within reasonable ranges
-- Progress and percentage values should be between 0.00 and 100.00
ALTER TABLE projects ADD CONSTRAINT check_progress_range CHECK (progress >= 0.00 AND progress <= 100.00);
ALTER TABLE models ADD CONSTRAINT check_model_progress_range CHECK (progress >= 0.00 AND progress <= 100.00);
ALTER TABLE models ADD CONSTRAINT check_accuracy_range CHECK (accuracy >= 0.00 AND accuracy <= 100.00);
ALTER TABLE nodes ADD CONSTRAINT check_node_progress_range CHECK (progress >= 0.00 AND progress <= 100.00);
ALTER TABLE nodes ADD CONSTRAINT check_cpu_usage_range CHECK (cpu_usage >= 0.00 AND cpu_usage <= 100.00);
ALTER TABLE nodes ADD CONSTRAINT check_memory_usage_range CHECK (memory_usage >= 0.00 AND memory_usage <= 100.00);
ALTER TABLE nodes ADD CONSTRAINT check_disk_usage_range CHECK (disk_usage >= 0.00 AND disk_usage <= 100.00);

-- Ensure size and transfer values are non-negative
ALTER TABLE models ADD CONSTRAINT check_size_positive CHECK (size >= 0.00);
ALTER TABLE nodes ADD CONSTRAINT check_sent_positive CHECK (sent >= 0.00);
ALTER TABLE nodes ADD CONSTRAINT check_received_positive CHECK (received >= 0.00);

-- Commit transaction
COMMIT;

-- Verify the migration
SELECT
    'projects' AS table_name,
    column_name,
    data_type,
    numeric_precision,
    numeric_scale
FROM information_schema.columns
WHERE table_name = 'projects'
    AND column_name IN ('progress')
    AND table_schema = 'public'

UNION ALL

SELECT
    'models' AS table_name,
    column_name,
    data_type,
    numeric_precision,
    numeric_scale
FROM information_schema.columns
WHERE table_name = 'models'
    AND column_name IN ('size', 'progress', 'loss', 'accuracy')
    AND table_schema = 'public'

UNION ALL

SELECT
    'nodes' AS table_name,
    column_name,
    data_type,
    numeric_precision,
    numeric_scale
FROM information_schema.columns
WHERE table_name = 'nodes'
    AND column_name IN ('progress', 'cpu_usage', 'memory_usage', 'disk_usage', 'sent', 'received')
    AND table_schema = 'public'
ORDER BY table_name, column_name;