# Crowdfunding ETL Pipeline

End-to-end ETL pipeline transforming raw crowdfunding spreadsheets into a normalized PostgreSQL database.

*Team project — built with T. Nguyen, U. Olusoga, and J. Zhang.*

## Pipeline

**Extract** — two Excel sources: 1,000 campaign records (`crowdfunding.xlsx`) and contact data stored as embedded JSON strings (`contacts.xlsx`).

**Transform** (pandas)
- Split a combined `category & sub-category` column into separate normalized category (9) and subcategory (24) lookup tables with sequential IDs
- Converted Unix timestamps to `datetime`, cast money columns to `float`, renamed columns to schema conventions
- Parsed the JSON contact blobs into structured columns and split full names into first/last name fields
- Merged lookup IDs back into the campaign table and exported four clean CSVs

**Load** — PostgreSQL schema with four tables (`contacts`, `category`, `subcategory`, `campaign`), primary/foreign key constraints, designed from an ERD (included in `Crowdfunding_Database/`). Loaded CSVs and verified integrity with SELECT queries (screenshots in `Verified_Select_Tables/`).

## Repository

- `ETL_Mini_Project_*.ipynb` — extraction and transformation
- `Crowdfunding_Database/Crowdfunding_db_schema.sql` — DDL
- `Crowdfunding_Database/Crowdfunding_ETL_ERD.png` — entity-relationship diagram

**Tools:** Python · pandas · NumPy · PostgreSQL · JSON parsing · ERD design
