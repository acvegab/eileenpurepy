CREATE TABLE IF NOT EXISTS users(
    UserID text PRIMARY KEY,
    UserName text,
    MessagesSent integer DEFAULT 0,
    Coins integer DEFAULT 0,
    CoinLock text DEFAULT CURRENT_TIMESTAMP,
    Warnings integer DEFAULT 0
);

-- ALTER TABLE users ADD COLUMN UserName text;
-- ALTER TABLE users ADD COLUMN Warnings integer DEFAULT 0;