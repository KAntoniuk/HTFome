DROP TABLE IF EXISTS htf;
DROP TABLE IF EXISTS drug;

CREATE TABLE htf (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  COLUMN_HEADER_2 TEXT UNIQUE NOT NULL,
  COLUMN_HEADER_3 TEXT NOT NULL
);

CREATE TABLE drug (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  COLUMN_HEADER_2 INTEGER NOT NULL,
  COLUMN_HEADER_3 TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  COLUMN_HEADER_4 TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (id) REFERENCES htf (id)
);
