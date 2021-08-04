'''
author: Brian Mukeswe
date: July 24, 2021
contact: mukeswebrian@yahoo.com
'''
import sqlite3
import pandas as pd


def connect(database):
    con = sqlite3.connect(database)
    return con

def create_table(database, table, col_str):
    
    con = connect(database)
    cur = con.cursor()

    query = f'''CREATE TABLE {table} ({col_str})'''

    # create table
    cur.execute(query)

    con.commit()
    con.close()

    print(f'created table {table} using sql:\n {query}')

def drop_table(database, table):
    con = connect(database)
    cur = con.cursor()

    # drop
    cur.execute(f'DROP TABLE {table}')
    con.commit()
    con.close()


def insert_data(database, table, data):
    con = connect(database)
    cur = con.cursor()

    data = data.rename(columns={c:c.lower().strip().replace(' ','_') for c in data.columns})

    columns = ', '.join(list(data.columns))
    success_count = 0


    for i in data.index:
        values = ', '.join([f"'{str(data[col].loc[i])}'" for col in data.columns])
        sql = rf'INSERT INTO {table} ({columns}) VALUES ({values});'
        
        try:
            cur.execute(sql)
            success_count += 1

        except Exception as inst:
            print(f'Error occured while executing the query!\n{sql}')
            print(f'Failed to insert row {i}: {data.loc[i]}')
            print(inst)
            

    con.commit()
    con.close()
    print(f'successfully inserted {success_count} rows into {table}')


def delete_data(database, table, condition):
    con = connect(database)
    cur = con.cursor()
    sql = f'DELETE FROM {table} WHERE {condition};'
    print(sql)
    cur.execute(sql)
    con.commit()
    con.close()

def execute_sql(database, sql):
    con = connect(database)
    cur = con.cursor()

    try:
        cur.execute(sql)
        print('Query executed successfully!')

    except Exception as inst:
        print('Error occured while executing the query!')
        print(inst)

    con.commit()
    con.close()

def query_sql(database, sql):

    con = connect(database)
    cur = con.cursor()

    rows = [] 

    try:
        for row in cur.execute(sql):
            rows.append(row)

        print('Query executed successfully!')

        if len(rows) == 0:
            print('query returned 0 rows')
        else:
            print(F'query returned {len(rows)} rows')
            data = pd.DataFrame(rows)
            return data
    
    except Exception as inst:
        print('Error occured while executing the query!')
        print(inst)
