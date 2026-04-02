-- Migration 005: Tables for v1.2-v2.0 features

CREATE TABLE IF NOT EXISTS notification_templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    channel TEXT NOT NULL DEFAULT 'json',  -- json, slack, teams, email
    template_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS api_keys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    key_hash TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    expires_at TIMESTAMP,
    revoked INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS instance_permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    instance_id TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'viewer',  -- admin, officer, viewer
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, instance_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (instance_id) REFERENCES instances(id)
);

CREATE TABLE IF NOT EXISTS instance_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    instance_id TEXT NOT NULL,
    score INTEGER NOT NULL,
    status TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (instance_id) REFERENCES instances(id)
);

CREATE TABLE IF NOT EXISTS policy_templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL DEFAULT '',
    content_json TEXT NOT NULL,
    category TEXT NOT NULL DEFAULT 'general',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS skill_executions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    instance_id TEXT,
    skill_name TEXT NOT NULL,
    parameters TEXT DEFAULT '{}',
    result TEXT DEFAULT '{}',
    duration_ms INTEGER DEFAULT 0,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS evidence (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    compliance_control TEXT NOT NULL,
    snapshot_json TEXT NOT NULL,
    captured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Seed default notification templates
INSERT OR IGNORE INTO notification_templates (name, channel, template_text) VALUES
    ('default_slack', 'slack', '{{ emoji }} *ClawSafe Alert*\n{{ message }}\n{% if old_status and new_status %}Previous: {{ old_status }} → Current: {{ new_status }}{% endif %}'),
    ('default_teams', 'teams', '{{ emoji }} ClawSafe Alert\n{{ message }}\n{% if old_status and new_status %}Status: {{ old_status }} → {{ new_status }}{% endif %}'),
    ('default_email', 'email', 'Subject: ClawSafe Alert - {{ event_type }}\n\n{{ message }}\n\n{% if old_status and new_status %}Status changed from {{ old_status }} to {{ new_status }}.{% endif %}\n\n-- ClawSafe Security Monitor');

-- Seed default policy templates
INSERT OR IGNORE INTO policy_templates (name, description, content_json, category) VALUES
    ('strict', 'Maximum security - blocks all high-risk tools, requires auth, localhost only', '{"version":"1","name":"strict","network":{"bind_address":"127.0.0.1","vpn_only":true},"tools":{"rules":[{"name":"*","risk":"high","action":"block"},{"name":"*","risk":"critical","action":"block"}]},"data":{"allow_mounts":false},"auth":{"enabled":true,"method":"token"}}', 'security'),
    ('permissive', 'Minimal restrictions - for trusted development environments', '{"version":"1","name":"permissive","network":{"bind_address":"0.0.0.0"},"tools":{"rules":[{"name":"*","action":"allow"}]},"data":{"allow_mounts":true},"auth":{"enabled":false}}', 'development'),
    ('compliance', 'SOC 2 aligned - audit logging, auth required, restricted access', '{"version":"1","name":"compliance","network":{"bind_address":"127.0.0.1","vpn_only":true},"tools":{"rules":[{"name":"*","risk":"high","action":"ask"},{"name":"*","risk":"critical","action":"block"}]},"data":{"allow_mounts":false},"auth":{"enabled":true,"method":"token"},"monitoring":{"audit_log":true,"retention_days":365}}', 'compliance'),
    ('development', 'Balanced for local development - moderate restrictions', '{"version":"1","name":"development","network":{"bind_address":"127.0.0.1"},"tools":{"rules":[{"name":"*","risk":"critical","action":"block"}]},"data":{"allow_mounts":true},"auth":{"enabled":false},"monitoring":{"audit_log":false}}', 'development');
