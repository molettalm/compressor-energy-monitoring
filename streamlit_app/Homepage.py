import streamlit as st
import pandas as pd
import pymysql.cursors
import numpy as np
from datetime import datetime
from datetime import time


conn = pymysql.connect(host='127.0.0.1',
                       user='dev',
                       password='dev',
                       database='node_test')

tableName = 'node'

if 'min' not in st.session_state:
    cursor = conn.cursor()
    cursor.execute("SELECT Min(created_at) FROM "+ tableName)
    st.session_state.min = cursor.fetchall()

    cursor.execute("SELECT Max(created_at) FROM "+ tableName)
    st.session_state.max= cursor.fetchall()

page1 = "Main Page"
st.set_page_config(page_title=page1)
st.markdown("# " + page1)
st.write(
    "Escolha os limites de data que você quer ver o funcionamento do compressor da UTFPR: "
)

@st.cache_data
def load_data(date_select):
    cursor = conn.cursor()
    cursor.execute("SELECT value,created_at FROM node_test.node")
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['value', 'created_at'])
    df['created_at'] = pd.to_datetime(df['created_at'])
    df = df[(df['created_at']>=date_select[0]) & (df['created_at']<date_select[1])]
    df = df.set_index('created_at') 
    df.index = df.index.strftime('%d/%m/%y %H:%M:%S') 
    return df

date_select = st.slider('Select the time range:',
                        value=(st.session_state.min[0][0], st.session_state.max[0][0]),
                        min_value=st.session_state.min[0][0],
                        max_value=st.session_state.max[0][0],
                        format="DD/MM/YY - hh:mm")

st.sidebar.header("Data das informações: \n" + str(date_select[0]) + " até \n" + str(date_select[1]))


df = load_data(date_select)

with st.container():
    st.write("Tensão")
    st.line_chart(df, use_container_width=True) #Tensão
with st.container():
    st.write("Corrente")
    st.line_chart(df, use_container_width=True) #Corrente 
with st.container():
    st.write("Potência")
    st.line_chart(df, use_container_width=True) #Potencia
with st.container():
    st.write("Modos de operação")
    chart_data = pd.DataFrame(np.random.randn(20,3), columns=["a", "b", "c"]) #Chart com a qtd de vezes do modo de operação
    st.bar_chart(chart_data) #Chart com a qtd de vezes do modo de operação
#st.dataframe(df.reset_index()) 

#Para as métricas de modo de operação, quantas vezes ficou ligado, quantas vezes desligado, o outro modo de operação lá e por fim a qtd de Ah do período
with st.sidebar:
    st.metric("Humidity", "86%", "4%")
    st.metric("Wind", "9 mph", "-8%")
    st.metric("Temperature", "70 °F", "1.2 °F")
    st.metric("Corrente (Ah)", "1000 Ah", "2 Ah")

st.text('Lucas Moletta')