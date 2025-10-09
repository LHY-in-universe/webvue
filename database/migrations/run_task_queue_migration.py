#!/usr/bin/env python3
"""
Task Queue Migration Script
Creates the TaskQueue table and related database structures for task scheduling and concurrency control.
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
        logging.FileHandler('task_queue_migration.log'),
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
    """Read the task queue migration SQL file."""
    script_dir = Path(__file__).parent
    sql_file = script_dir / "002_task_queue_migration.sql"

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

def check_prerequisites(engine):
    """Check if required tables exist before migration."""
    required_tables = ['projects', 'users']
    missing_tables = []

    for table in required_tables:
        if not check_table_exists(engine, table):
            missing_tables.append(table)

    return missing_tables

def run_migration():
    """Run the task queue migration."""
    logger.info("Starting Task Queue Migration...")

    # Get database connection
    db_url = get_database_url()
    logger.info(f"Connecting to database: {db_url.split('@')[1] if '@' in db_url else 'local'}")

    try:
        engine = create_engine(db_url)

        # Check prerequisites
        missing_tables = check_prerequisites(engine)
        if missing_tables:
            logger.error(f"Required tables missing: {missing_tables}")
            logger.error("Please run the main database migration first.")
            return False

        # Check if TaskQueue table already exists
        if check_table_exists(engine, 'task_queue'):
            logger.warning("TaskQueue table already exists. Migration may have been run before.")
            user_input = input("Continue anyway? (y/N): ").lower().strip()
            if user_input != 'y':
                logger.info("Migration cancelled by user.")
                return False

        # Read migration SQL
        migration_sql = read_migration_sql()

        # Execute migration
        logger.info("Executing task queue migration SQL...")
        with engine.connect() as conn:
            # Execute the entire migration script
            try:
                conn.execute(text(migration_sql))
                conn.commit()
                logger.info("Task queue migration completed successfully!")

                # Verify the migration
                logger.info("Verifying migration...")

                # Check if task_queue table was created
                if check_table_exists(engine, 'task_queue'):
                    logger.info("✅ task_queue table created successfully")

                    # Check table structure
                    result = conn.execute(text("""
                        SELECT column_name, data_type, is_nullable
                        FROM information_schema.columns
                        WHERE table_name = 'task_queue'
                          AND table_schema = 'public'
                        ORDER BY ordinal_position;
                    """))

                    columns = result.fetchall()
                    logger.info("✅ Task queue table structure:")
                    for col in columns:
                        nullable = "NULL" if col[2] == "YES" else "NOT NULL"
                        logger.info(f"  - {col[0]}: {col[1]} ({nullable})")

                    # Check indexes
                    result = conn.execute(text("""
                        SELECT indexname
                        FROM pg_indexes
                        WHERE tablename = 'task_queue'
                          AND schemaname = 'public';
                    """))

                    indexes = result.fetchall()
                    logger.info("✅ Task queue indexes:")
                    for idx in indexes:
                        logger.info(f"  - {idx[0]}")

                    # Check triggers
                    result = conn.execute(text("""
                        SELECT trigger_name
                        FROM information_schema.triggers
                        WHERE event_object_table = 'task_queue';
                    """))

                    triggers = result.fetchall()
                    logger.info("✅ Task queue triggers:")
                    for trigger in triggers:
                        logger.info(f"  - {trigger[0]}")

                else:
                    logger.error("❌ task_queue table was not created")
                    return False

            except SQLAlchemyError as e:
                logger.error(f"Error executing migration: {e}")
                conn.rollback()
                return False

        return True

    except SQLAlchemyError as e:
        logger.error(f"Database error during migration: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during migration: {e}")
        return False

def rollback_migration():
    """Rollback the task queue migration."""
    logger.info("Starting Task Queue Migration Rollback...")

    db_url = get_database_url()

    try:
        engine = create_engine(db_url)

        rollback_sql = """
        -- Remove triggers first
        DROP TRIGGER IF EXISTS trigger_check_project_concurrency ON task_queue;
        DROP TRIGGER IF EXISTS trigger_set_task_timestamps ON task_queue;

        -- Drop functions
        DROP FUNCTION IF EXISTS check_project_concurrency();
        DROP FUNCTION IF EXISTS set_task_started_at();

        -- Drop view
        DROP VIEW IF EXISTS task_queue_stats;

        -- Drop table (this will also drop indexes)
        DROP TABLE IF EXISTS task_queue CASCADE;
        """

        with engine.connect() as conn:
            conn.execute(text(rollback_sql))
            conn.commit()

        logger.info("Task queue migration rollback completed successfully!")
        return True

    except SQLAlchemyError as e:
        logger.error(f"Error during rollback: {e}")
        return False

def show_status():
    """Show current migration status."""
    logger.info("Checking Task Queue Migration Status...")

    db_url = get_database_url()

    try:
        engine = create_engine(db_url)

        with engine.connect() as conn:
            # Check if task_queue table exists
            table_exists = check_table_exists(engine, 'task_queue')

            if table_exists:
                logger.info("✅ TaskQueue table exists")

                # Get table statistics
                result = conn.execute(text("""
                    SELECT
                        COUNT(*) as total_tasks,
                        COUNT(*) FILTER (WHERE status = 'queued') as queued,
                        COUNT(*) FILTER (WHERE status = 'running') as running,
                        COUNT(*) FILTER (WHERE status = 'completed') as completed,
                        COUNT(*) FILTER (WHERE status = 'failed') as failed
                    FROM task_queue;
                """))

                stats = result.fetchone()
                logger.info(f"  Total tasks: {stats[0]}")
                logger.info(f"  Queued: {stats[1]}")
                logger.info(f"  Running: {stats[2]}")
                logger.info(f"  Completed: {stats[3]}")
                logger.info(f"  Failed: {stats[4]}")

            else:
                logger.info("❌ TaskQueue table does not exist")

            return table_exists

    except SQLAlchemyError as e:
        logger.error(f"Error checking status: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "rollback":
            success = rollback_migration()
        elif command == "status":
            success = show_status()
        elif command == "migrate":
            success = run_migration()
        else:
            logger.error("Usage: python run_task_queue_migration.py [migrate|rollback|status]")
            logger.error("  migrate  - Run the migration")
            logger.error("  rollback - Rollback the migration")
            logger.error("  status   - Show migration status")
            sys.exit(1)
    else:
        success = run_migration()

    sys.exit(0 if success else 1)