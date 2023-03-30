import streamlit as st
#import mysql.connector
import pymysql.cursors
import pandas as pd
import numpy as np
from datetime import datetime

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="dev",
#   password="dev",
#   database="node_test"
# )

connection = pymysql.connect(
  host="localhost",
  user="dev",
  password="dev",
  database="node_test"
)

tableName='node'
cursor = connection.cursor()

if 'max' not in st.session_state:
    cursor.execute("SELECT Min(created_at) FROM "+ tableName)
    st.session_state.min = cursor.fetchall()

    cursor.execute("SELECT Max(created_at) FROM "+ tableName)
    st.session_state.max= cursor.fetchall()


start_time = st.slider(
                        'When do you start?'
                        , value=(st.session_state.min ,st.session_state.max)
                        , format="MM/DD/YY - hh:mm"
                      )

cursor.execute("SELECT * FROM " + tableName)
dadosDB = cursor.fetchall()
for result in dadosDB:
  print(result[1])
  dataMedidas = result[1] #armazenando as datas do sql

#adicionando dados para os linechart
st.header('Compressor UTFPR - Informações Elétricas')
#d = st.date_input("Escolha o dia das medições: ") #Pegamos o dia que o usuário quer ver as medições
#Fazer um dataframe com o panda separando pelo dia

#teste com slide de datetime - coloca o primeiro valor do database e o outro é o now
#start_time = st.slider('When do you start?', value=(datetime(2023, 1, 1, 9, 30),datetime.now()), format="MM/DD/YY - hh:mm")

#start_time = st.slider('When do you start?', value=(datetime(2023, 1, 1, 9, 30)), min_value = (datetime(2023, 1, 1, 9, 30)), max_value = (datetime(2023, 3, 29, 9, 30)) , format="MM/DD/YY - hh:mm")

st.write("Start time:", start_time)

df = pd.DataFrame(dadosDB, columns=['value','created_at'])
st.line_chart(df[['value','created_at']], x = 'created_at',y='value')
