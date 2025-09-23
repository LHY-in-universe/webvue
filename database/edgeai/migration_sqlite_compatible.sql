-- SQLite compatible migration script to consolidate duplicate fields in projects table

-- Step 1: Add new unified columns (SQLite doesn't support IF NOT EXISTS for ALTER TABLE)
ALTER TABLE projects ADD COLUMN training_alg VARCHAR(100) DEFAULT 'sft';
ALTER TABLE projects ADD COLUMN fed_alg VARCHAR(100) DEFAULT 'fedavg';
ALTER TABLE projects ADD COLUMN secure_aggregation VARCHAR(100) DEFAULT 'shamir_threshold';
ALTER TABLE projects ADD COLUMN total_epochs INTEGER DEFAULT 100;
ALTER TABLE projects ADD COLUMN lr VARCHAR(50) DEFAULT '1e-4';
ALTER TABLE projects ADD COLUMN num_computers INTEGER DEFAULT 3;
ALTER TABLE projects ADD COLUMN threshold INTEGER DEFAULT 2;
ALTER TABLE projects ADD COLUMN num_clients INTEGER DEFAULT 2;
ALTER TABLE projects ADD COLUMN sample_clients INTEGER DEFAULT 2;
ALTER TABLE projects ADD COLUMN max_steps INTEGER DEFAULT 100;
ALTER TABLE projects ADD COLUMN model_name_or_path VARCHAR(500) DEFAULT 'sshleifer/tiny-gpt2';
ALTER TABLE projects ADD COLUMN dataset_name VARCHAR(200) DEFAULT 'vicgalle/alpaca-gpt4';
ALTER TABLE projects ADD COLUMN dataset_sample INTEGER DEFAULT 50;

-- Step 2: Migrate data from old fields to new unified fields (if old columns exist)
-- Copy strategy to training_alg
UPDATE projects SET training_alg = CASE
    WHEN strategy IS NOT NULL AND strategy != '' THEN strategy
    ELSE 'sft'
END;

-- Copy protocol to fed_alg
UPDATE projects SET fed_alg = CASE
    WHEN protocol IS NOT NULL AND protocol != '' THEN protocol
    ELSE 'fedavg'
END;

-- Copy epoches to total_epochs
UPDATE projects SET total_epochs = CASE
    WHEN epoches IS NOT NULL AND epoches > 0 THEN epoches
    ELSE 100
END;

-- Copy learning_rate to lr (convert float to string)
UPDATE projects SET lr = CASE
    WHEN learning_rate IS NOT NULL AND learning_rate > 0 THEN CAST(learning_rate AS TEXT)
    ELSE '1e-4'
END;

-- Update default batch_size if it's still 1 (old default)
UPDATE projects SET batch_size = 32 WHERE batch_size = 1;