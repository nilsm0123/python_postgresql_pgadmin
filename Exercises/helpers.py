"""
Helper functions for the beginner exercises.

You do NOT need to understand this file to do the exercises.
It connects to the database, loads the Northwind data and checks
your answers.
"""

from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, inspect, text

# Database connection (same credentials as in docker-compose.yml)
DB_URL = "postgresql://pgadmin:geheim@localhost:5432/northwind"
DATA_PATH = Path(__file__).resolve().parent.parent / "Data"

TABLES = {
    "categories": "Categories.csv",
    "customers": "Customers.csv",
    "employees": "Employees.csv",
    "orderdetails": "OrderDetails.csv",
    "orders": "Orders.csv",
    "products": "Products.csv",
    "shippers": "Shippers.csv",
    "suppliers": "Suppliers.csv",
}

engine = create_engine(DB_URL)


# ---------------------------------------------------------------------------
# General helpers
# ---------------------------------------------------------------------------

def check(is_correct, hint=""):
    """Print a green check or a red cross with a hint."""
    if is_correct:
        print("✅ Correct, well done!")
    else:
        print("❌ Not yet." + (f" Hint: {hint}" if hint else ""))


def setup_database():
    """Load the Northwind CSV files into PostgreSQL (only missing tables)."""
    existing = inspect(engine).get_table_names()
    for table, file_name in TABLES.items():
        if table in existing:
            print(f"  table '{table}' already exists")
        else:
            df = pd.read_csv(DATA_PATH / file_name)
            df.columns = df.columns.str.lower()
            df.to_sql(table, engine, index=False)
            print(f"  table '{table}' created ({len(df)} rows)")
    print("Database is ready!")


def sql(query, params=None):
    """Run a SQL query and return the result as a pandas DataFrame."""
    with engine.connect() as connection:
        return pd.read_sql(text(query), connection, params=params)


# ---------------------------------------------------------------------------
# SQL exercise checker
# ---------------------------------------------------------------------------

# Reference solutions for 02_sql_basics.ipynb.
# (Try the exercises yourself before looking here!)
SQL_SOLUTIONS = {
    1: "SELECT * FROM shippers",
    2: "SELECT productname, price FROM products",
    3: "SELECT * FROM customers WHERE country = 'Germany'",
    4: "SELECT productname, price FROM products WHERE price > 50",
    5: "SELECT productname, price FROM products "
       "WHERE categoryid = 1 AND price < 20",
    6: "SELECT customername, country FROM customers "
       "WHERE country IN ('France', 'Spain', 'Italy')",
    7: "SELECT productname FROM products WHERE productname LIKE 'Ch%'",
    8: "SELECT productname, price FROM products ORDER BY price DESC",
    9: "SELECT productname, price FROM products ORDER BY price ASC LIMIT 5",
    10: "SELECT DISTINCT country FROM customers ORDER BY country",
    11: "SELECT COUNT(*) FROM customers",
    12: "SELECT MIN(price), MAX(price), ROUND(AVG(price)::numeric, 2) "
        "FROM products",
    13: "SELECT country, COUNT(*) AS number_of_customers FROM customers "
        "GROUP BY country ORDER BY number_of_customers DESC, country",
    14: "SELECT country, COUNT(*) FROM customers "
        "GROUP BY country HAVING COUNT(*) > 5",
    15: "SELECT p.productname, c.categoryname FROM products p "
        "JOIN categories c ON p.categoryid = c.categoryid",
    16: "SELECT c.categoryname, COUNT(*) AS number_of_products "
        "FROM products p JOIN categories c ON p.categoryid = c.categoryid "
        "GROUP BY c.categoryname ORDER BY number_of_products DESC, "
        "c.categoryname",
    17: "SELECT c.customername, COUNT(*) AS number_of_orders "
        "FROM customers c JOIN orders o ON c.customerid = o.customerid "
        "GROUP BY c.customername ORDER BY number_of_orders DESC, "
        "c.customername LIMIT 5",
    18: "SELECT e.firstname, e.lastname, COUNT(*) AS number_of_orders "
        "FROM employees e JOIN orders o ON e.employeeid = o.employeeid "
        "GROUP BY e.firstname, e.lastname ORDER BY number_of_orders DESC",
}


def _normalize(df, keep_order):
    """Make a result comparable: ignore column names, round numbers."""
    df = df.copy()
    df.columns = range(len(df.columns))
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].astype(float).round(2)
        else:
            df[col] = df[col].astype(str)
    if not keep_order:
        df = df.sort_values(list(df.columns))
    return df.reset_index(drop=True)


def check_sql(number, query):
    """Run your query, show the result and compare it with the solution."""
    if not query.strip():
        print("❌ Write your SQL query between the \"\"\" quotes first.")
        return None
    try:
        result = sql(query)
    except Exception as error:
        message = str(error).split(") ", 1)[-1].split("\n")[0]
        print("❌ Your query has an error:")
        print("  ", message)
        return None

    expected = sql(SQL_SOLUTIONS[number])
    keep_order = "ORDER BY" in SQL_SOLUTIONS[number].upper()

    if len(result.columns) != len(expected.columns):
        print(f"❌ Not yet. You return {len(result.columns)} column(s), "
              f"expected {len(expected.columns)}: {list(expected.columns)}")
    elif len(result) != len(expected):
        print(f"❌ Not yet. You return {len(result)} row(s), "
              f"expected {len(expected)} row(s).")
    elif not _normalize(result, keep_order).equals(
            _normalize(expected, keep_order)):
        hint = " Check the sort order." if keep_order else ""
        print("❌ Not yet. The number of rows is right, "
              "but some values are different." + hint)
    else:
        print("✅ Correct, well done!")
    return result
