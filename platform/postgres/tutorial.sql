CREATE TABLE IF NOT EXISTS household(
  id uuid PRIMARY KEY,
  external_id varchar(45) NOT NULL,
  income integer NOT NULL DEFAULT '1',
  zip_code_3 varchar(3) NOT NULL DEFAULT '1',
  client_name varchar(50) NOT NULL
)
