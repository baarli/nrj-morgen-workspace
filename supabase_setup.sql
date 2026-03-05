-- ============================================
-- Mission Control ↔ BaarliClaw 2-Veis Kommunikasjon
-- Kjør dette i Supabase SQL Editor
-- ============================================

-- 1. Agent Commands (Kommandoer fra Mission Control til meg)
CREATE TABLE IF NOT EXISTS agent_commands (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    command_type TEXT NOT NULL CHECK (command_type IN ('task', 'query', 'approval', 'config', 'system')),
    command_data JSONB NOT NULL DEFAULT '{}',
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'completed', 'failed', 'cancelled')),
    priority TEXT DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high', 'critical')),
    created_by TEXT NOT NULL DEFAULT 'user',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    result JSONB,
    error_message TEXT,
    progress INTEGER DEFAULT 0 CHECK (progress >= 0 AND progress <= 100)
);

CREATE INDEX IF NOT EXISTS idx_agent_commands_status ON agent_commands(status);
CREATE INDEX IF NOT EXISTS idx_agent_commands_created_at ON agent_commands(created_at DESC);

-- 2. Agent Responses (Svar fra meg til Mission Control)
CREATE TABLE IF NOT EXISTS agent_responses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    command_id UUID REFERENCES agent_commands(id) ON DELETE CASCADE,
    response_type TEXT NOT NULL CHECK (response_type IN ('status', 'result', 'error', 'question', 'progress')),
    response_data JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_agent_responses_command_id ON agent_responses(command_id);
CREATE INDEX IF NOT EXISTS idx_agent_responses_created_at ON agent_responses(created_at DESC);

-- 3. Approval Requests (Godkjenningsforespørsler)
CREATE TABLE IF NOT EXISTS approval_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    request_type TEXT NOT NULL CHECK (request_type IN ('deploy', 'delete', 'expensive_operation', 'external_api', 'data_modification')),
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    details JSONB DEFAULT '{}',
    risk_level TEXT DEFAULT 'medium' CHECK (risk_level IN ('low', 'medium', 'high', 'critical')),
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected', 'auto_approved')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    responded_at TIMESTAMP WITH TIME ZONE,
    response TEXT,
    responded_by TEXT,
    auto_approve BOOLEAN DEFAULT false
);

CREATE INDEX IF NOT EXISTS idx_approval_requests_status ON approval_requests(status);
CREATE INDEX IF NOT EXISTS idx_approval_requests_created_at ON approval_requests(created_at DESC);

-- 4. System Status (Status fra alle systemer jeg administrerer)
CREATE TABLE IF NOT EXISTS system_status (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    system_name TEXT NOT NULL UNIQUE,
    system_type TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('healthy', 'warning', 'error', 'unknown', 'maintenance')),
    health_score INTEGER DEFAULT 100 CHECK (health_score >= 0 AND health_score <= 100),
    last_check TIMESTAMP WITH TIME ZONE DEFAULT now(),
    next_scheduled_run TIMESTAMP WITH TIME ZONE,
    metrics JSONB DEFAULT '{}',
    error_count INTEGER DEFAULT 0,
    last_error TEXT,
    last_error_at TIMESTAMP WITH TIME ZONE,
    version TEXT,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_system_status_status ON system_status(status);
CREATE INDEX IF NOT EXISTS idx_system_status_system_name ON system_status(system_name);

-- 5. Activity Log (Full logg over alt som skjer)
CREATE TABLE IF NOT EXISTS activity_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    level TEXT NOT NULL CHECK (level IN ('debug', 'info', 'success', 'warning', 'error', 'critical')),
    category TEXT NOT NULL CHECK (category IN ('system', 'task', 'api', 'user', 'automation', 'error')),
    message TEXT NOT NULL,
    details JSONB DEFAULT '{}',
    source TEXT NOT NULL DEFAULT 'baarliclaw',
    actionable BOOLEAN DEFAULT false,
    action_taken BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_activity_log_created_at ON activity_log(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_activity_log_level ON activity_log(level);
CREATE INDEX IF NOT EXISTS idx_activity_log_category ON activity_log(category);

-- 6. Agent Configuration (Konfigurasjon for meg)
CREATE TABLE IF NOT EXISTS agent_config (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    config_key TEXT NOT NULL UNIQUE,
    config_value JSONB NOT NULL,
    description TEXT,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_by TEXT DEFAULT 'system'
);

-- Enable Realtime for alle tabeller
ALTER PUBLICATION supabase_realtime ADD TABLE agent_commands;
ALTER PUBLICATION supabase_realtime ADD TABLE agent_responses;
ALTER PUBLICATION supabase_realtime ADD TABLE approval_requests;
ALTER PUBLICATION supabase_realtime ADD TABLE system_status;
ALTER PUBLICATION supabase_realtime ADD TABLE activity_log;

-- Insert default system status for eksisterende systemer
INSERT INTO system_status (system_name, system_type, status, health_score, version) VALUES
    ('mission_control', 'dashboard', 'healthy', 100, '2.0'),
    ('morning_routine', 'automation', 'healthy', 100, '2.1'),
    ('podcast_manager', 'automation', 'healthy', 100, '1.0'),
    ('nrj_dashboard', 'automation', 'healthy', 100, '1.0'),
    ('content_aggregator', 'automation', 'healthy', 100, '2.1')
ON CONFLICT (system_name) DO UPDATE SET
    status = EXCLUDED.status,
    health_score = EXCLUDED.health_score,
    updated_at = now();

-- Insert default config
INSERT INTO agent_config (config_key, config_value, description) VALUES
    ('auto_approve_rules', '{"low_risk": true, "max_cost": 0, "trusted_systems": ["mission_control"]}', 'Regler for auto-godkjenning'),
    ('notification_settings', '{"email": false, "push": true, "sms": false}', 'Notifikasjonsinnstillinger'),
    ('system_check_interval', '{"minutes": 5}', 'Hvor ofte systemer sjekkes')
ON CONFLICT (config_key) DO NOTHING;

-- Logg at setup er fullført
INSERT INTO activity_log (level, category, message, details, source) VALUES
    ('success', 'system', 'Database setup fullført', '{"tables_created": 6}', 'baarliclaw');
