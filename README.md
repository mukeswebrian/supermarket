# supermarket
This repository contains a synthetic dataset that can be used to teach and learn different data analytics concepts using SQL Lite and Python.



Windows
## Step 1: Load all the data files into a SQLite database
- open a new terminal in VS Code
- run each of the commands below as described
- Note: if you are using a macbook, you may need to replace `python` with `python3` is the commands shown below

```
Windows
python --version

# install the required python dependancies
python -m pip install -r requirements.txt

# run the provided script to create a sqlite database on your local computer
python load_all_database_tables.py
```

```
Macbook bash - terminal
# check python version - make sure it is at least python 3
python3 --version

# install the required python dependancies
python3 -m pip install -r requirements.txt

# run the provided script to create a sqlite database on your local computer
python3 load_all_database_tables.py
```

## Step 2: Test SQL Lite database with example queries
Open the notebook test_queries.ipynb and run all the cells to confirm that the data has actually been loaded into the database.
