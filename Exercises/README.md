# Beginner Exercises: Python and SQL

Do the notebooks in this order:

| Notebook | Topics | Exercises |
|---|---|---|
| `01_python_basics.ipynb` | variables, strings, lists, if/else, loops, dictionaries, functions | 16 |
| `02_sql_basics.ipynb` | SELECT, WHERE, ORDER BY, LIMIT, COUNT/AVG, GROUP BY, HAVING, JOIN | 18 |
| `03_python_and_sql.ipynb` | run SQL from Python, pandas, parameters, charts, write to the DB | 6 |

## How to work

1. Open a notebook and select the `.venv` Python kernel (top right).
2. Run the first cell (it loads `helpers.py`).
3. Write your answer, run the cell with **Shift + Enter**, then run the check.
   You get ✅ or ❌ with a hint.
4. Solutions are in `solutions/`. Try yourself first!

Notebooks 02 and 03 need the PostgreSQL container to be running
(see the main `README.md`). They load the Northwind data automatically.

After that, continue with the harder questions in `SQL/QUESTIONS.sql`.
