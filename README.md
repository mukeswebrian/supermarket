# supermarket
This repository contains a synthetic dataset that can be used to teach and learn different data analytics concepts using SQL Lite and Python.

Note: if you are using a macbook, you may need to replace `python` with `python3` is the commands shown below


## Step 1: Load all the data files into a SQLite database
- open a new terminal in VS Code
- run each of the commands below as described

```bash
# check python version - make sure it is at least python 3
python --version

# create and activate the python environment where you will be working
python -m venv hibreed_data_env
.\hibreed_data_env\Scripts\activate

# install the required python dependancies
python -m pip install -r requirements.txt

# run the provided script to create a sqlite database on your local computer
python load_all_database_tables.py
```

## Step 2: Test SQL Lite database with example queries
Open the notebook test_queries.ipynb and run all the cells to confirm that the data has actually been loaded into the database.
