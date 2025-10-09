#!/usr/bin/env python3
"""
Database migration script to convert Float fields to DECIMAL for better precision.
This script will execute the SQL migration safely with proper error handling.
"""

import os
import sys
import logging
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('migration.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def get_database_url():
    """Get database URL from environment or use default."""
    # Try to get from environment first
    db_url = os.getenv('DATABASE_URL')
    if db_url:
        return db_url

    # Default development database URL
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'edgeai_db')
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', 'password')

    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

def read_migration_sql():
    """Read the migration SQL file."""
    script_dir = Path(__file__).parent
    sql_file = script_dir / "001_decimal_precision_migration.sql"

    if not sql_file.exists():
        raise FileNotFoundError(f"Migration SQL file not found: {sql_file}")

    with open(sql_file, 'r', encoding='utf-8') as f:
        return f.read()

def check_table_exists(engine, table_name):
    """Check if a table exists in the database."""
    try:
        with engine.connect() as conn:
            result = conn.execute(text(f"""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables
                    WHERE table_schema = 'public'
                    AND table_name = '{table_name}'
                );
            """))
            return result.scalar()
    except SQLAlchemyError as e:
        logger.error(f"Error checking if table {table_name} exists: {e}")
        return False

def backup_tables(engine):
    """Create backup tables before migration."""
    logger.info("Creating backup tables...")

    backup_queries = [
        "DROP TABLE IF EXISTS projects_backup_decimal_migration;",
        "CREATE TABLE projects_backup_decimal_migration AS SELECT * FROM projects;",
        "DROP TABLE IF EXISTS models_backup_decimal_migration;",
        "CREATE TABLE models_backup_decimal_migration AS SELECT * FROM models;",
        "DROP TABLE IF EXISTS nodes_backup_decimal_migration;",
        "CREATE TABLE nodes_backup_decimal_migration AS SELECT * FROM nodes;"
    ]

    try:
        with engine.connect() as conn:
            for query in backup_queries:
                conn.execute(text(query))
            conn.commit()
        logger.info("Backup tables created successfully")
        return True
    except SQLAlchemyError as e:
        logger.error(f"Failed to create backup tables: {e}")
        return False

def run_migration():
    """Run the decimal precision migration."""
    logger.info("Starting decimal precision migration...")

    # Get database connection
    db_url = get_database_url()
    logger.info(f"Connecting to database: {db_url.split('@')[1] if '@' in db_url else 'local'}")

    try:
        engine = create_engine(db_url)

        # Check if required tables exist
        required_tables = ['projects', 'models', 'nodes']
        for table in required_tables:
            if not check_table_exists(engine, table):
                logger.error(f"Required table '{table}' does not exist. Migration aborted.")
                return False

        logger.info("All required tables exist. Proceeding with migration...")

        # Create backups
        if not backup_tables(engine):
            logger.error("Failed to create backup tables. Migration aborted.")
            return False

        # Read migration SQL
        migration_sql = read_migration_sql()

        # Execute migration
        logger.info("Executing migration SQL...")
        with engine.connect() as conn:
            # Split SQL into individual statements and execute them
            statements = [stmt.strip() for stmt in migration_sql.split(';') if stmt.strip()]

            for i, statement in enumerate(statements, 1):
                if statement.upper().startswith(('BEGIN', 'COMMIT')):
                    # Skip transaction control statements as we're managing our own transaction
                    continue

                if statement.upper().startswith('SELECT') and 'information_schema' in statement.lower():
                    # This is the verification query at the end
                    logger.info("Executing verification query...")
                    result = conn.execute(text(statement))

                    # Log the results
                    logger.info("Migration verification results:")
                    for row in result:
                        logger.info(f"  {row}")
                else:
                    logger.debug(f"Executing statement {i}: {statement[:100]}...")
                    conn.execute(text(statement))

            conn.commit()

        logger.info("Migration completed successfully!")

        # Test a simple query to ensure everything works
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM projects"))
            count = result.scalar()
            logger.info(f"Verification: Found {count} projects in database")

        return True

    except SQLAlchemyError as e:
        logger.error(f"Database error during migration: {e}")
        logger.error("Migration failed. Database should be restored from backup if needed.")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during migration: {e}")
        return False

def rollback_migration():
    """Rollback migration by restoring from backup tables."""
    logger.info("Starting migration rollback...")

    db_url = get_database_url()

    try:
        engine = create_engine(db_url)

        rollback_queries = [
            "BEGIN;",
            "DROP TABLE IF EXISTS projects CASCADE;",
            "ALTER TABLE projects_backup_decimal_migration RENAME TO projects;",
            "DROP TABLE IF EXISTS models CASCADE;",
            "ALTER TABLE models_backup_decimal_migration RENAME TO models;",
            "DROP TABLE IF EXISTS nodes CASCADE;",
            "ALTER TABLE nodes_backup_decimal_migration RENAME TO nodes;",
            "COMMIT;"
        ]

        with engine.connect() as conn:
            for query in rollback_queries:
                if query.strip():
                    conn.execute(text(query))

        logger.info("Migration rollback completed successfully!")
        return True

    except SQLAlchemyError as e:
        logger.error(f"Error during rollback: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "rollback":
        success = rollback_migration()
    else:
        success = run_migration()

    sys.exit(0 if success else 1)