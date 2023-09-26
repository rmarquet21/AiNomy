CREATE TABLE users (
   address TEXT NOT NULL UNIQUE,
   nonce TEXT NOT NULL,
   created_at TIMESTAMP DEFAULT NOW(),
   updated_at TIMESTAMP DEFAULT NOW()
);