import streamlit as st
import pandas as pd


st.header('Compressor UTFPR - Informações Elétricas')

if st.button('Corrente'):
    st.write('DADOS DE CORRENTE AQUI')
else:
    st.write('Qual dado você gostaria de saber')