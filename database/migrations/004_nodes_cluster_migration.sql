-- Migration: Update nodes table to use cluster_id instead of project_id
-- Date: 2024-01-01
-- Description: This migration updates the nodes table to use cluster_id as foreign key to cluster table instead of project_id

-- Step 1: Add cluster_id column if it doesn't exist (it should already exist based on models.py)
-- ALTER TABLE nodes ADD COLUMN cluster_id INTEGER;

-- Step 2: Create foreign key constraint for cluster_id
ALTER TABLE nodes ADD CONSTRAINT fk_nodes_cluster_id 
    FOREIGN KEY (cluster_id) REFERENCES cluster(id) ON DELETE SET NULL;

-- Step 3: Create index for cluster_id for better query performance
CREATE INDEX IF NOT EXISTS idx_nodes_cluster_id ON nodes(cluster_id);

-- Step 4: Update existing data - migrate project_id to cluster_id
-- This assumes that for each project, there should be a corresponding cluster
-- If no cluster exists for a project, we'll create one
INSERT INTO cluster (name, user_id, project_id, created_time, last_updated_time)
SELECT 
    CONCAT('Cluster for ', p.name) as name,
    p.user_id,
    p.id as project_id,
    NOW() as created_time,
    NOW() as last_updated_time
FROM projects p
WHERE p.id IN (
    SELECT DISTINCT project_id 
    FROM nodes 
    WHERE project_id IS NOT NULL
) 
AND NOT EXISTS (
    SELECT 1 FROM cluster c WHERE c.project_id = p.id
);

-- Step 5: Update nodes table to set cluster_id based on project_id
UPDATE nodes n
SET cluster_id = (
    SELECT c.id 
    FROM cluster c 
    WHERE c.project_id = n.project_id
)
WHERE n.project_id IS NOT NULL;

-- Step 6: Remove the old project_id column (commented out for safety)
-- ALTER TABLE nodes DROP COLUMN project_id;

-- Note: The project_id column removal is commented out for safety.
-- Uncomment the line above only after verifying that all data has been migrated
-- and all application code has been updated to use cluster_id instead of project_id.
