-- Multi-instance support (v2)

CREATE TABLE IF NOT EXISTS instances (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    config_path TEXT NOT NULL,
    tags TEXT NOT NULL DEFAULT '',
    active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Insert default instance for backward compatibility
INSERT OR IGNORE INTO instances (id, name, config_path)
VALUES ('default', 'Default', '/etc/openclaw/config.yaml');

-- Add instance_id to existing tables (SQLite doesn't support ADD COLUMN IF NOT EXISTS,
-- so we use a trick: create column only if it doesn't exist by catching the error)

-- For scans
CREATE TABLE IF NOT EXISTS _scans_migration_check (done INTEGER);
INSERT OR IGNORE INTO _scans_migration_check VALUES (1);

-- Note: SQLite ALTER TABLE ADD COLUMN is idempotent if column doesn't exist
-- but fails if it does. We'll handle this in the migration runner.

INSERT OR IGNORE INTO schema_version (version) VALUES (2);
