-- Initial schema placeholder. Use Alembic (backend) for versioned migrations in production.

CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS etl_metadata;

CREATE TABLE IF NOT EXISTS etl_metadata.pipeline_runs (
    id          BIGSERIAL PRIMARY KEY,
    pipeline_id VARCHAR(128) NOT NULL,
    status      VARCHAR(32)  NOT NULL DEFAULT 'pending',
    started_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    finished_at TIMESTAMPTZ,
    row_count   BIGINT,
    error_message TEXT
);

CREATE INDEX IF NOT EXISTS idx_pipeline_runs_pipeline_id
    ON etl_metadata.pipeline_runs (pipeline_id);

CREATE TABLE IF NOT EXISTS analytics.sample_events (
    id              BIGSERIAL PRIMARY KEY,
    event_id        VARCHAR(64)  NOT NULL UNIQUE,
    user_id         VARCHAR(64)  NOT NULL,
    event_type      VARCHAR(64)  NOT NULL,
    event_timestamp TIMESTAMPTZ  NOT NULL,
    amount          NUMERIC(12, 2) NOT NULL DEFAULT 0,
    loaded_at       TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_sample_events_user_id
    ON analytics.sample_events (user_id);

CREATE INDEX IF NOT EXISTS idx_sample_events_event_timestamp
    ON analytics.sample_events (event_timestamp);
