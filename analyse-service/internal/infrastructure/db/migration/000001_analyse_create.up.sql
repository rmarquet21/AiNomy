CREATE TABLE history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    owner VARCHAR NOT NULL,
    filename VARCHAR NOT NULL,
    image BYTEA NOT NULL,
    Kind VARCHAR NOT NULL,
    prediction JSON NOT NULL
);