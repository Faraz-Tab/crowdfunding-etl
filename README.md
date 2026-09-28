# Crowdfunding ETL Pipeline

End-to-end ETL pipeline transforming raw crowdfunding spreadsheets into a normalized PostgreSQL database.

*Team project — built with T. Nguyen, U. Olusoga, and J. Zhang.*

## Pipeline

**Extract** — two Excel sources: 1,000 campaign records (`crowdfunding.xlsx`) and contact data stored as embedded JSON strings (`contacts.xlsx`).

**Transform** (pandas)
- Split a combined `category & sub-category` column into separate normalized category (9) and subcategory (24) lookup tables with sequential IDs
- Converted Unix timestamps to dates, cast money columns to `float`, renamed columns to match the schema
- Parsed the JSON contact blobs into structured columns and split full names into first/last name fields
- Merged lookup IDs back into the campaign table and exported four clean CSVs whose columns match the schema exactly, in the same order

**Load** — PostgreSQL schema with four tables (`contacts`, `category`, `subcategory`, `campaign`), primary/foreign key constraints, designed from an ERD (included in `Crowdfunding_Database/`). The CSVs were imported into PostgreSQL and checked with SELECT queries (screenshots in `Verified_Select_Tables/`).

## Validation

CI re-runs the notebook on every pull request, checks that the regenerated CSVs match the committed ones, and tests them against the schema: column names and order, unique primary keys, foreign keys that resolve, and valid date ranges.

## Repository

- `ETL_Mini_Project_*.ipynb` — extraction and transformation
- `Crowdfunding_Database/Crowdfunding_db_schema.sql` — DDL
- `Crowdfunding_Database/Crowdfunding_ETL_ERD.png` — entity-relationship diagram
- `Resources/` — source spreadsheets and exported CSVs
- `tests/test_outputs.py` — schema and integrity checks

## How to Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
jupyter nbconvert --to notebook --execute --inplace ETL_Mini_Project_*.ipynb   # regenerates Resources/*.csv
pytest -q
```

**Tools:** Python · pandas · NumPy · PostgreSQL · JSON parsing · ERD design · pytest · GitHub Actions
