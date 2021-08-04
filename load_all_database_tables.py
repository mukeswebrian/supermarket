'''
author: Brian Mukeswe
date: July 24, 2021
contact: mukeswebrian@yahoo.com
'''

import pandas as pd
import database_utils as dbu

database = 'supermarket.db'


def load_products_table():

    # create the products table
    query = 'CREATE TABLE products (product CHAR, category CHAR, unit_cost_of_goods FLOAT)'
    dbu.execute_sql(database=database, sql=query)


    # insert all rows into the products table
    products = pd.read_excel('datasets/supermarket_products.xlsx')
    dbu.insert_data(database='supermarket.db', 
                table='products', 
                data=products)


def load_prices_table():

    # create the prices table
    query = 'CREATE TABLE prices (location CHAR, product CHAR, price FLOAT)'
    dbu.execute_sql(database=database, sql=query)

    # insert all rows into the prices table
    for i in range(1,6):
        location = f'location_{i}'
        prices = pd.read_csv(f'datasets/{location}_prices.csv', index_col=0).reset_index()
        labels = pd.Series([location for i in prices.index], name='location', index=prices.index)
        prices = prices.join(labels)
        prices = prices.rename(columns={'index':'product'})
        
        dbu.insert_data(database='supermarket.db', 
                table='prices', 
                data=prices)


def load_transactions_table():

    # create the transactions table
    query = 'CREATE TABLE transactions (timestamp CHAR, product CHAR, quantity FLOAT, location CHAR)'
    dbu.execute_sql(database=database, sql=query)

    # insert all rows into the transactions table
    for i in range(1,6):
        location = f'location_{i}'
        transactions = pd.read_csv(f'datasets/march_2021_transactions_{location}.csv', index_col=0)
        labels = pd.Series([location for i in transactions.index], name='location', index=transactions.index)
        transactions = transactions.join(labels)
        transactions = transactions.rename(columns={'item':'product'})
        
        dbu.insert_data(database='supermarket.db', 
                table='transactions', 
                data=transactions)

if __name__=='__main__':
    load_products_table()
    load_prices_table()
    load_transactions_table()
