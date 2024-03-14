-- Create the 'liberal' table
CREATE TABLE liberal (
    id SERIAL PRIMARY KEY,
    headline VARCHAR(255),
    body TEXT,
    url VARCHAR(255)
);

-- Create the 'conservative' table
CREATE TABLE conservative (
    id SERIAL PRIMARY KEY,
    headline VARCHAR(255),
    body TEXT,
    url VARCHAR(255)
);
