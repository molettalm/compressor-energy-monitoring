import streamlit as st
import pandas as pd
import mysql.connector

def app():
    conn = mysql.connector.connect( host="127.0.0.1",
                                    port="3306",
                                    user="root",
                                    passwd="root",
                                    db="node_test"
                                  )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM node_test.node")
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['id',
                                     'value',
                                     'created_at']
                      )
   
    st.dataframe(df)


    st.text('Lucas Moletta')