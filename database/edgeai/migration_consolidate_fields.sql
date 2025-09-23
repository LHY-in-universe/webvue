-- Migration script to consolidate duplicate fields in projects table
-- This script merges duplicate fields and updates existing data

-- Step 1: Add new unified columns if they don't exist
ALTER TABLE projects
ADD COLUMN IF NOT EXISTS training_alg VARCHAR(100) DEFAULT 'sft',
ADD COLUMN IF NOT EXISTS fed_alg VARCHAR(100) DEFAULT 'fedavg',
ADD COLUMN IF NOT EXISTS total_epochs INTEGER DEFAULT 100,
ADD COLUMN IF NOT EXISTS lr VARCHAR(50) DEFAULT '1e-4';

-- Step 2: Migrate data from old fields to new unified fields
-- Migrate strategy -> training_alg (if strategy has data)
UPDATE projects
SET training_alg = CASE
    WHEN strategy IS NOT NULL AND strategy != '' THEN strategy
    ELSE 'sft'
END
WHERE training_alg IS NULL OR training_alg = '';

-- Migrate protocol -> fed_alg (if protocol has data)
UPDATE projects
SET fed_alg = CASE
    WHEN protocol IS NOT NULL AND protocol != '' THEN protocol
    ELSE 'fedavg'
END
WHERE fed_alg IS NULL OR fed_alg = '';

-- Migrate epoches -> total_epochs (if epoches has data)
UPDATE projects
SET total_epochs = CASE
    WHEN epoches IS NOT NULL AND epoches > 0 THEN epoches
    ELSE 100
END
WHERE total_epochs IS NULL OR total_epochs = 0;

-- Migrate learning_rate -> lr (convert float to string)
UPDATE projects
SET lr = CASE
    WHEN learning_rate IS NOT NULL AND learning_rate > 0 THEN CAST(learning_rate AS VARCHAR)
    ELSE '1e-4'
END
WHERE lr IS NULL OR lr = '';

-- Step 3: Remove old duplicate columns after data migration
-- (Comment out these lines if you want to keep old columns for backup)
ALTER TABLE projects DROP COLUMN IF EXISTS strategy;
ALTER TABLE projects DROP COLUMN IF EXISTS protocol;
ALTER TABLE projects DROP COLUMN IF EXISTS epoches;
ALTER TABLE projects DROP COLUMN IF EXISTS learning_rate;

-- Step 4: Update default batch_size if it's still 1 (old default)
UPDATE projects
SET batch_size = 32
WHERE batch_size = 1;

-- Step 5: Verify the migration
SELECT
    COUNT(*) as total_projects,
    COUNT(CASE WHEN training_alg IS NOT NULL THEN 1 END) as has_training_alg,
    COUNT(CASE WHEN fed_alg IS NOT NULL THEN 1 END) as has_fed_alg,
    COUNT(CASE WHEN total_epochs IS NOT NULL THEN 1 END) as has_total_epochs,
    COUNT(CASE WHEN lr IS NOT NULL THEN 1 END) as has_lr
FROM projects;

-- Display sample of migrated data
SELECT
    id, name, training_alg, fed_alg, total_epochs, lr, batch_size, status
FROM projects
LIMIT 5;