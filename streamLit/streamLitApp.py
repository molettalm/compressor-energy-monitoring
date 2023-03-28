import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np

mydb = mysql.connector.connect(
  host="localhost",
  user="dev",
  password="dev",
  database="node_test"
)
tableName='node'
#para pegar todos os dados da table do db
mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM " + tableName)
dadosDB = mycursor.fetchall()
for result in dadosDB:
  print(result[1])
  dataMedidas = result[1] #armazenando as datas do sql

#adicionando dados para os linechart
st.header('Compressor UTFPR - Informações Elétricas')
d = st.date_input("Escolha o dia das medições: ") #Pegamos o dia que o usuário quer ver as medições
#Fazer um dataframe com o panda separando pelo dia

df = pd.DataFrame(dadosDB, columns=['value','created_at'])
st.line_chart(df[['value','created_at']], x = 'created_at',y='value')
