'''
author: Brian Mukeswe
date: April 30, 2022
contact: mukeswebrian@yahoo.com
'''

# import libraries
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from datetime import timedelta


@st.cache()
def fetchData():
    # set up credentials to connect to remote database
    conn = {
        'host': 'da-class-db.cxcjjheb3bem.us-east-1.rds.amazonaws.com',
        'port': '3306',
        'database': 'supermarket',
        'username': 'hibreed_student',
        'password': open('password.txt','r').read()
        }


    # Write query to fetch all the supermarket data
    sqlQuery = '''
        select timestamp, t3.product, t3.location, quantity, t2.price, t1.category, t1.unit_cost_of_goods
        from transactions t3

        left join prices t2 on t3.product=t2.product and t3.location=t2.location
        left join products t1 on t3.product=t1.product

        order by 1
    '''

    ## run query to fetch the data
    # create connection string
    connectionString = f'mysql+pymysql://{conn["username"]}:{conn["password"]}@{conn["host"]}/{conn["database"]}'

    # create connection engine
    engine = create_engine(connectionString) 

    # fetch the data
    supermarket = pd.read_sql(sql=sqlQuery, con=engine)

    return supermarket

supermarket = fetchData()



# add revenue and date columns
revenue = supermarket.price * supermarket.quantity
revenue.name = 'revenue'

date = supermarket.timestamp.apply(lambda d: str(d.__format__('%Y-%m-%d')))
date.name = 'date'
supermarket = pd.concat([supermarket, revenue, date], axis=1)



st.markdown('# Daily Supermarket Summary Report')


# specify date input and corresponding previous day
date = st.date_input('Report Date')
prev = date - timedelta(days=1)

# fromat date strings
dateStr = date.__format__('%Y-%m-%d')
prevStr = prev.__format__('%Y-%m-%d')

# fiter for data on the specified daates
dateData = supermarket.query(f'date=="{dateStr}"')
prevData = supermarket.query(f'date=="{prevStr}"')

# calculate revenue for each date
today_revenue = dateData.revenue.sum()
prev_revenue = prevData.revenue.sum()

# display the revenue metric
st.metric('Total Revenue', 
          '{:,.0f} Shs'.format(today_revenue), 
          '{:,.0f} Shs'.format(today_revenue-prev_revenue)
          )

# Table of daily revenue per location
st.markdown(f'## 1. Daily revenue per location ({dateStr})')
toDate =  supermarket.query(f'date<="{dateStr}"')
toDate = toDate.groupby(['date','location']).sum().revenue.unstack(level=1)

# format table values
table1 = toDate.style.format({i:"{:,.0f}" for i in toDate.columns})

# display table in streamlit
st.table(table1)


# Cumulative daily revenue per location
st.markdown(f'## 2. Cumulative daily revenue per location ({dateStr})')
toDateCum = toDate.cumsum()

# format table values
table2 = toDateCum.style.format({i:"{:,.0f}" for i in toDateCum.columns})

# display table in streamlit
st.table(table2)

fig0, ax = plt.subplots(1,1)
toDateCum.plot(kind='bar', 
               figsize=(12,6), 
               stacked=True,
               ax=ax
               )
# format lables                  
ytick_labels = ['{:,.0f}'.format(int(y)) for y in ax.get_yticks()]
ax.set_yticklabels(ytick_labels, size=10)
st.pyplot(fig0)




# plot top products
# leading products
st.markdown(f'## 3. Products ({dateStr})')
products = dateData.groupby(['product','location'])
products = products.revenue.sum().unstack(level=1)

# build a filter for the top 5 products
top5 = dateData.groupby('product').revenue.sum().sort_values(ascending=True)[-5:]
top = filter(lambda i: any([i==p for p in top5.index]), products.index)

# plot
fig1, ax = plt.subplots(1,1)
products.loc[list(top)].sort_values(by='location_2').plot(kind='barh',
                  figsize=(6,3),
                  title='Top 5 Products by Revenue',
                  stacked=True,
                  ax=ax
                  )
# format lables                  
xtick_labels = ['{:,.0f}'.format(int(x)) for x in ax.get_xticks()]
ax.set_xticklabels(xtick_labels, size=8)

# display figure in streamlit
st.pyplot(fig1)


# lagging products
fig2, ax = plt.subplots(1,1)
products = dateData.groupby('product').revenue.sum().sort_values(ascending=True)
products[:5].plot(kind='barh',
                  figsize=(6,3),
                  title='Bottom 5 Products by Revenue',
                  ax=ax
                  )

# format lables                  
xtick_labels = ['{:,.0f}'.format(int(x)) for x in ax.get_xticks()]
ax.set_xticklabels(xtick_labels, size=8)

# display figure in streamlit
st.pyplot(fig2)

# Busiest hour
st.markdown(f'## 4. Transactions ({dateStr})')
fig3, ax = plt.subplots(1,1)
hours = dateData.groupby('timestamp').product.count()
hours.plot(kind='bar', 
           figsize=(6,3),
           title='Hourly Number of Transactions',
           ax=ax)

# format lables                  
xtick_labels = [x.__format__('%H:00') for x in hours.index]
ax.set_xticklabels(xtick_labels, size=8)

# display figure in streamlit
st.pyplot(fig3)

