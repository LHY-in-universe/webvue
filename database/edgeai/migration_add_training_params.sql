-- Migration script to add new training parameters to the projects table
-- This script adds all the new columns needed for test API integration

ALTER TABLE projects
ADD COLUMN training_alg VARCHAR(100) DEFAULT 'sft',
ADD COLUMN fed_alg VARCHAR(100) DEFAULT 'fedavg',
ADD COLUMN secure_aggregation VARCHAR(100) DEFAULT 'shamir_threshold',
ADD COLUMN num_computers INTEGER DEFAULT 3,
ADD COLUMN threshold INTEGER DEFAULT 2,
ADD COLUMN num_rounds INTEGER DEFAULT 10,
ADD COLUMN num_clients INTEGER DEFAULT 2,
ADD COLUMN sample_clients INTEGER DEFAULT 2,
ADD COLUMN max_steps INTEGER DEFAULT 100,
ADD COLUMN lr VARCHAR(50) DEFAULT '1e-4',
ADD COLUMN model_name_or_path VARCHAR(500) DEFAULT 'sshleifer/tiny-gpt2',
ADD COLUMN dataset_name VARCHAR(200) DEFAULT 'vicgalle/alpaca-gpt4',
ADD COLUMN dataset_sample INTEGER DEFAULT 50;

-- Update existing projects with default values
UPDATE projects
SET
    training_alg = 'sft',
    fed_alg = 'fedavg',
    secure_aggregation = 'shamir_threshold',
    num_computers = 3,
    threshold = 2,
    num_rounds = 10,
    num_clients = 2,
    sample_clients = 2,
    max_steps = 100,
    lr = '1e-4',
    model_name_or_path = 'sshleifer/tiny-gpt2',
    dataset_name = 'vicgalle/alpaca-gpt4',
    dataset_sample = 50
WHERE training_alg IS NULL;

-- Verify the migration
SELECT COUNT(*) as total_projects FROM projects;
SELECT training_alg, fed_alg, secure_aggregation FROM projects LIMIT 5;