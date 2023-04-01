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
    cursor.execute("SELECT moment, voltage, current, power_W, energy_WH, power_factor_measured, power_factor_calc, phase_angle_measured, phase_angle_calc FROM pi2." + tableName)
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['moment', 'voltage', 'current', 'power_W', 'energy_WH', 'power_factor_measured', 'power_factor_calc', 'phase_angle_measured', 'phase_angle_calc'])
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

def classifyOpMode(valor):
    if valor > 0.2:
        return 'On'
    elif valor < 0.05:
        return 'Off'
    else:
        return 'StandBy'

currentAvgOld = df['current'].iloc[:-4000].mean()
powerFacAvgOld = df['power_factor_calc'].iloc[:-4000].mean()
opModeOld = df['current'].iloc[:-4000].apply(classifyOpMode)
contOpModeOld = opModeOld.value_counts()
qtyOnOld = contOpModeOld['On']
qtyStandByOld = contOpModeOld['StandBy']
qtyOffOld = contOpModeOld['Off']



with st.container():
    # st.write("Tensão")
    # st.line_chart(df.rename(columns = {'voltage': 'Tensão (V)'})['Tensão (V)'], use_container_width=True) #Tensão
    fig = px.line(df, x = 'moment', y = 'voltage', title='Tensão [V]', labels = {'voltage': 'Tensão', 'moment': 'Horário'})
    st.plotly_chart(fig, use_container_width=True)
with st.container():
    # st.write("Corrente")
    # st.line_chart(df.rename(columns = {'current': 'Corrente (A)'})['Corrente (A)'], use_container_width=True) #Corrente 
    fig = px.line(df, x = 'moment', y = 'current', title='Corrente [A]', labels = {'current': 'Corrente', 'moment': 'Horário'})
    st.plotly_chart(fig, use_container_width=True)
with st.container():
    # st.write("Potência")
    # st.line_chart(df.rename(columns = {'power_W': 'Potência (W)'})['Potência (W)'], use_container_width=True) #Potencia
    fig = px.line(df, x = 'moment', y = 'power_W', title='Potência [W]', labels = {'power_W': 'Potência', 'moment': 'Horário'})
    st.plotly_chart(fig, use_container_width=True)
with st.container():
    # st.write("Energia")
    # st.line_chart(df.rename(columns = {'energy_WH': 'Energia (W/h)'})['Energia (W/h)'], use_container_width=True) #Energia
    fig = px.line(df, x = 'moment', y = 'energy_WH', title='Energia [W/h]', labels = {'energy_WH': 'Energia', 'moment': 'Horário'})
    st.plotly_chart(fig, use_container_width=True)
with st.container():
    # st.write("Fator de Potência")
    # st.line_chart(df.rename(columns = {'power_factor_measured': 'Fat de Pot Medido', 'power_factor_calc': 'Fat de Pot Calc'})[['Fat de Pot Medido', 'Fat de Pot Calc']], use_container_width=True) #Fator de Potência
    fig = px.line(df, x = 'moment', y = ['power_factor_measured', 'power_factor_calc'], title='Fator de Potência', color_discrete_map = {'power_factor_measured': 'green', 'power_factor_calc': 'blue'} , labels = {'power_factor_measured': 'Medido', 'power_factor_calc': 'Calculado', 'moment': 'Horário'})
    st.plotly_chart(fig, use_container_width=True)
with st.container():
    # st.write("Ângulo de Fase")
    # st.line_chart(df.rename(columns = {'phase_angle_measured': 'Âng de Fase Medido (Graus)', 'phase_angle_calc': 'Âng de Fase Calc (Graus)'})[['Âng de Fase Medido (Graus)', 'Âng de Fase Calc (Graus)']], use_container_width=True) #Ângulo de Fase
    fig = px.line(df, x = 'moment', y = ['phase_angle_measured', 'phase_angle_calc'], title='Ângulo de Fase [Graus]', color_discrete_map = {'phase_angle_measured': 'green', 'phase_angle_calc': 'blue'} , labels = {'phase_angle_measured': 'Medido', 'phase_angle_calc': 'Calculado', 'moment': 'Horário'})
    st.plotly_chart(fig, use_container_width=True)
with st.container():
    st.write("Modos de operação")
    chart_data = pd.DataFrame(np.random.randn(20,3), columns=["a", "b", "c"]) #Chart com a qtd de vezes do modo de operação
    st.bar_chart(chart_data) #Chart com a qtd de vezes do modo de operação
#st.dataframe(df.reset_index()) 

#Para as métricas de modo de operação, quantas vezes ficou ligado, quantas vezes desligado, o outro modo de operação lá e por fim a qtd de Ah do período
with st.sidebar:
    currentAvg = df['current'].mean()
    powerFacAvg = df['power_factor_calc'].mean()
    opMode = df['current'].apply(classifyOpMode)
    contOpMode = opMode.value_counts()
    qtyOn = contOpMode['On']
    qtyStandBy = contOpMode['StandBy']
    qtyOff = contOpMode['Off']
    st.metric("Corrente Média no período",  str(round(currentAvg, 3)) + " A", str(round(currentAvgOld-currentAvg, 3)) + " A" )
    st.metric("Fator de Potência calculado no período", round(powerFacAvg, 3), round(powerFacAvgOld-powerFacAvg, 3))
    st.metric("Quantidade de vezes ligado durante o período", str(qtyOn) + ' vezes', str(qtyOnOld-qtyOn) + ' vezes')
    st.metric("Quantidade de vezes em standby durante o período", str(qtyStandBy) + ' vezes', str(qtyStandByOld-qtyStandBy) + ' vezes')
    st.metric("Quantidade de vezes desligado durante o período", str(qtyOff) + ' vezes', str(qtyOffOld-qtyOff) + ' vezes')

st.text('Lucas Moletta')