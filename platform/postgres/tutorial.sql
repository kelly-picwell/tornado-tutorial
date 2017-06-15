CREATE TABLE IF NOT EXISTS threshold(
  id uuid PRIMARY KEY,
  external_id varchar(45) NOT NULL,
  family boolean,
  network varchar(50) NOT NULL,
  drug_moop integer,
  medical_moop integer,
  medical_drug_moop integer,
  moop_embedded boolean,
  drug_deductible integer,
  medical_deductible integer,
  medical_drug_deductible integer,
  deductible_embedded boolean
)
