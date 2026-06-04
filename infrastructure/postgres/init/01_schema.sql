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
