import streamlit as st
import pandas as pd
import pymysql.cursors
import numpy as np

connection = pymysql.connect(host='127.0.0.1',
                         user='root',
                         password='root',
                         database='node_test',
                         cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()
cursor.execute("SELECT value,created_at FROM node_test.node LIMIT 5")
data = cursor.fetchall()
df = pd.DataFrame(data, columns=['value',
                                 'created_at']

                  )
datas = df[['value', 'created_at']] # Also include the "date" column
st.line_chart(datas)
st.dataframe(df)
st.line_chart(df[['value','created_at']], x = 'created_at',y='value')


st.text('Lucas Moletta')