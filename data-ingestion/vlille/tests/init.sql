-- This script is executed when the Docker container for PostgreSQL starts.

-- Create the table to store raw V'Lille data
CREATE TABLE IF NOT EXISTS raw_vlille (
    id SERIAL PRIMARY KEY,
    raw_content JSONB NOT NULL,
    ingested_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- You can grant permissions if needed, though the default user will have them
GRANT ALL PRIVILEGES ON TABLE raw_vlille TO testuser;
