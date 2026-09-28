"""Check the exported CSVs against the PostgreSQL schema: columns, primary keys and foreign keys."""
import re
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = (ROOT / "Crowdfunding_Database" / "Crowdfunding_db_schema.sql").read_text()
CSV_FOR_TABLE = {"contacts": "contacts_clean", "category": "category", "subcategory": "subcategory", "campaign": "campaign"}


def schema_columns(table):
    body = re.search(rf"CREATE TABLE {table}\((.*?)\n\);", SCHEMA, re.S).group(1)
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    return [line.split()[0] for line in lines if not line.startswith(("PRIMARY", "FOREIGN"))]


def load(table):
    return pd.read_csv(ROOT / "Resources" / f"{CSV_FOR_TABLE[table]}.csv")


@pytest.mark.parametrize("table", CSV_FOR_TABLE)
def test_csv_columns_match_schema_order(table):
    assert list(load(table).columns) == schema_columns(table)


@pytest.mark.parametrize("table, key", [("contacts", "contact_id"), ("category", "category_id"),
                                        ("subcategory", "subcategory_id"), ("campaign", "cf_id")])
def test_primary_keys_unique_and_present(table, key):
    ids = load(table)[key]
    assert ids.notna().all() and ids.is_unique


@pytest.mark.parametrize("column, table", [("contact_id", "contacts"), ("category_id", "category"),
                                           ("subcategory_id", "subcategory")])
def test_campaign_foreign_keys_resolve(column, table):
    assert load("campaign")[column].isin(load(table)[column]).all()


def test_campaign_dates_are_valid():
    campaign = load("campaign")
    launched = pd.to_datetime(campaign["launched_date"], format="%Y-%m-%d")
    ended = pd.to_datetime(campaign["end_date"], format="%Y-%m-%d")
    assert (ended >= launched).all()
