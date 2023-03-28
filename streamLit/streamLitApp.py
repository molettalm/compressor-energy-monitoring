import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="dev",
  password="dev",
  database="node_test"
)
tableName='node'
#para pegar todos os dados da table do db
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM " + tableName)
myresult = mycursor.fetchall()
for result in myresult:
  print(result)

#adicionando dados para os linechart
st.header('Compressor UTFPR - Informações Elétricas')
df = pd.DataFrame(myresult, columns=['value','created_at'])
datas = df[['value', 'created_at']]
st.line_chart(datas)
st.dataframe(df)
st.line_chart(df[['value','created_at']], x = 'created_at',y='value')
