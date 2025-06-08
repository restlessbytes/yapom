-- create sessions table
CREATE TABLE IF NOT EXISTS sessions (
    pid INTEGER,
    start TEXT,
    end TEXT,
    runtime INTEGER,
    status TEXT
);

-- insert "dummy" data
INSERT INTO sessions (pid, start, end, runtime, status)
VALUES (123, '2025-06-01 12:00:00', '2025-06-01 12:05:00', 300, 'finished');

-- TODO dummy data with start and end times on different days!
