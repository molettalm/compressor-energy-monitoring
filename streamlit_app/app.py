import streamlit as st
import pandas as pd
import pymysql.cursors
import numpy as np
from datetime import datetime
from datetime import time


conn = pymysql.connect(host='127.0.0.1',
                       user='root',
                       password='root',
                       database='node_test')

tableName = 'node'

if 'min' not in st.session_state:
    cursor = conn.cursor()
    cursor.execute("SELECT Min(created_at) FROM "+ tableName)
    st.session_state.min = cursor.fetchall()

    cursor.execute("SELECT Max(created_at) FROM "+ tableName)
    st.session_state.max= cursor.fetchall()

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

df = load_data(date_select)

st.line_chart(df, use_container_width=True) 
st.dataframe(df.reset_index()) 

st.text('Lucas Moletta')