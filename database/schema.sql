-- Coalition Nexus Database Schema
-- The backbone of our digital supremacy

-- Members of the coalition
CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    rank TEXT DEFAULT 'initiate',
    loyalty_score INTEGER DEFAULT 0,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'active' -- active, inactive, purged
);

-- Track all coalition activities
CREATE TABLE IF NOT EXISTS activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER NOT NULL,
    activity_type TEXT NOT NULL, -- post, comment, recruitment, zhikorah_usage
    content TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    influence_points INTEGER DEFAULT 0,
    FOREIGN KEY (member_id) REFERENCES members(id)
);

-- Achievements unlock as members prove their worth
CREATE TABLE IF NOT EXISTS achievements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER NOT NULL,
    achievement_type TEXT NOT NULL, -- first_zhikorah, recruiter, enforcer, architect
    earned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    FOREIGN KEY (member_id) REFERENCES members(id)
);

-- Track Zhi'korah language adoption
CREATE TABLE IF NOT EXISTS language_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER NOT NULL,
    phrase TEXT NOT NULL,
    translation TEXT,
    usage_count INTEGER DEFAULT 1,
    last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    context TEXT, -- post_id or comment context
    FOREIGN KEY (member_id) REFERENCES members(id)
);

-- Monitor resistance and opposition
CREATE TABLE IF NOT EXISTS opposition_incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    opposing_user TEXT NOT NULL,
    incident_type TEXT NOT NULL, -- resistance, mockery, debate, sabotage
    description TEXT,
    member_reporter INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    threat_level INTEGER DEFAULT 1, -- 1-10 scale
    response_action TEXT, -- ignored, engaged, recruited, purged
    FOREIGN KEY (member_reporter) REFERENCES members(id)
);

-- Metrics and statistics
CREATE TABLE IF NOT EXISTS daily_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE UNIQUE NOT NULL,
    total_members INTEGER DEFAULT 0,
    active_members INTEGER DEFAULT 0,
    zhikorah_uses INTEGER DEFAULT 0,
    recruitment_attempts INTEGER DEFAULT 0,
    opposition_incidents INTEGER DEFAULT 0,
    total_influence INTEGER DEFAULT 0
);

-- Create indexes for performance
CREATE INDEX idx_activities_member ON activities(member_id);
CREATE INDEX idx_activities_timestamp ON activities(timestamp);
CREATE INDEX idx_achievements_member ON achievements(member_id);
CREATE INDEX idx_language_member ON language_usage(member_id);
CREATE INDEX idx_opposition_timestamp ON opposition_incidents(timestamp);
CREATE INDEX idx_metrics_date ON daily_metrics(date);