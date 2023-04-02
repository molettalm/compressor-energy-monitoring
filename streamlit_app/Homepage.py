import streamlit as st
import pandas as pd
import pymysql.cursors
import numpy as np
import plotly.express as px 
from datetime import datetime
from datetime import time


conn = pymysql.connect(host='192.168.18.27',
                       user='piuser',
                       password='piuser',
                       database='pi2')

tableName = 'compressor_measurements'

if 'min' not in st.session_state:
    cursor = conn.cursor()
    cursor.execute("SELECT Min(moment) FROM "+ tableName)
    st.session_state.min = cursor.fetchall()

    cursor.execute("SELECT Max(moment) FROM "+ tableName)
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
    cursor.execute("SELECT moment, voltage, current, power_W, energy_WH, power_factor_measured, power_factor_calc, phase_angle_measured, phase_angle_calc, opMode FROM pi2." + tableName)
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['moment', 'voltage', 'current', 'power_W', 'energy_WH', 'power_factor_measured', 'power_factor_calc', 'phase_angle_measured', 'phase_angle_calc', 'opMode'])
    df['moment'] = pd.to_datetime(df['moment'])
    df = df[(df['moment']>=date_select[0]) & (df['moment']<date_select[1])]
    #df = df.set_index('moment') 
    #df.index = df.index.strftime('%d/%m/%y %H:%M:%S') 
    return df

date_select = st.slider('Select the time range:',
                        value=(st.session_state.min[0][0], st.session_state.max[0][0]),
                        min_value=st.session_state.min[0][0],
                        max_value=st.session_state.max[0][0],
                        format="DD/MM/YY - hh:mm")

st.sidebar.header("Data das informações: \n" + str(date_select[0]) + " até \n" + str(date_select[1]))


df = load_data(date_select)

def seconds_to_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    
    return f"{days} d, {hours} hr, {minutes} min, {seconds} seg"

measuringTime = 5

qtyOff = df[df['opMode'] == 0]['opMode'].count()
qtyOffSec = qtyOff * measuringTime

qtyOn = df[df['opMode'] == 1]['opMode'].count()
qtyOnSec = qtyOn * measuringTime

qtyStandby = df[df['opMode'] == 2]['opMode'].count()
qtyStandbySec = qtyStandby * measuringTime

with st.container():
    fig = px.line(df, x = 'moment', y = 'voltage', title='Tensão [V]', connectgaps=False, labels = {'voltage': 'Tensão', 'moment': 'Horário'})
    st.plotly_chart(fig, use_container_width=True)
with st.container():
    fig = px.line(df, x = 'moment', y = 'current', title='Corrente [A]', connectgaps=False, labels = {'current': 'Corrente', 'moment': 'Horário'})
    st.plotly_chart(fig, use_container_width=True)
with st.container():
    fig = px.line(df, x = 'moment', y = 'power_W', title='Potência [W]', connectgaps=False, labels = {'power_W': 'Potência', 'moment': 'Horário'})
    st.plotly_chart(fig, use_container_width=True)
with st.container():
    fig = px.line(df, x = 'moment', y = 'energy_WH', title='Energia [W/h]', connectgaps=False, labels = {'energy_WH': 'Energia', 'moment': 'Horário'})
    st.plotly_chart(fig, use_container_width=True)
with st.container():
    fig = px.line(df, x = 'moment', y = ['power_factor_measured', 'power_factor_calc'], connectgaps=False, title='Fator de Potência', color_discrete_map = {'power_factor_measured': 'green', 'power_factor_calc': 'blue'} , labels = {'power_factor_measured': 'Medido', 'power_factor_calc': 'Calculado', 'moment': 'Horário'})
    st.plotly_chart(fig, use_container_width=True)
with st.container():
    fig = px.line(df, x = 'moment', y = ['phase_angle_measured', 'phase_angle_calc'],  connectgaps=False, title='Ângulo de Fase [Graus]', color_discrete_map = {'phase_angle_measured': 'green', 'phase_angle_calc': 'blue'} , labels = {'phase_angle_measured': 'Medido', 'phase_angle_calc': 'Calculado', 'moment': 'Horário'})
    st.plotly_chart(fig, use_container_width=True)
with st.container():
    st.write("Modos de operação")
    stackeddf = df
    stackeddf['moment'] = pd.to_datetime(stackeddf['moment']).dt.strftime('%Y-%m-%d')
    dailyValues = stackeddf.groupby(['moment','opMode']).size()
    result_df = dailyValues.apply(lambda x: x*5).reset_index(name='result')
    groupedAgain = result_df.groupby(['moment', 'opMode'])['result'].sum().reset_index()
    st.bar_chart( data=groupedAgain, x='moment', y='result', color='opMode')
    #chart_data = pd.DataFrame(np.random.randn(20,3), columns=["Desligado", "Ligado", "StandBy"]) #Chart com a qtd de vezes do modo de operação
    #st.bar_chart(chart_data) #Chart com a qtd de vezes do modo de operação
    #Fazer isso pelos dias, quantas vezes em cada dia...

#Para as métricas de modo de operação, quantas vezes ficou ligado, quantas vezes desligado, o outro modo de operação lá e por fim a qtd de Ah do período
with st.sidebar:
    if (len(df['current']) != 0):
        currentAvg = df['current'].mean()
        powerFacAvg = df['power_factor_calc'].mean()

        st.metric("Corrente Média no período",  str(round(currentAvg, 3)) + " A")
        st.metric("Fator de Potência calculado no período", round(powerFacAvg, 3))
        
        st.metric("Tempo desligado durante o período", seconds_to_time(qtyOffSec))
        st.metric("Tempo ligado durante o período", seconds_to_time(qtyOnSec))
        st.metric("Tempo em standby durante o período", seconds_to_time(qtyStandbySec))

st.text('Lucas Moletta')