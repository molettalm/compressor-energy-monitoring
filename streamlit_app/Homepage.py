import streamlit as st
import numpy as np
import plotly.express as px 
from datetime import time,datetime, timedelta
import polars as pl
import connectorx as cx
import lttbc


def seconds_to_hours(seconds):
    hours = round((seconds / 3600),2)
    return f"{hours} Horas"


def load_data(date_select,df):

    sample_size = 40000

    df = df.with_columns(pl.col("moment").apply(lambda x: x.timestamp()))
    moment_downsampled = df['moment'].to_list()
    voltage_downsampled = df['voltage'].to_list()
    current_downsampled = df['current'].to_list()
    power_W_downsampled = df['power_W'].to_list()
    power_factor_measured_downsampled = df['power_factor_measured'].to_list()
    power_factor_calc_downsampled = df['power_factor_calc'].to_list()
    phase_angle_measured_downsampled = df['phase_angle_measured'].to_list()
    phase_angle_calc_downsampled = df['phase_angle_calc'].to_list()
    opMode_downsampled = df['opMode'].to_list()

    n_moment_downsampled , n_voltage_downsampled = lttbc.downsample(moment_downsampled, voltage_downsampled, sample_size)
    n_moment_downsampled , n_current_downsampled = lttbc.downsample(moment_downsampled, current_downsampled, sample_size)
    n_moment_downsampled , n_power_W_downsampled = lttbc.downsample(moment_downsampled, power_W_downsampled, sample_size)
    n_moment_downsampled , n_power_factor_measured_downsampled = lttbc.downsample(moment_downsampled, power_factor_measured_downsampled, sample_size)
    n_moment_downsampled , n_power_factor_calc_downsampled = lttbc.downsample(moment_downsampled,  power_factor_calc_downsampled, sample_size)
    n_moment_downsampled , n_phase_angle_measured_downsampled = lttbc.downsample(moment_downsampled,  phase_angle_measured_downsampled, sample_size)
    n_moment_downsampled , n_phase_angle_calc_downsampled = lttbc.downsample(moment_downsampled,  phase_angle_calc_downsampled, sample_size)
    n_moment_downsampled , n_opMode_downsampled = lttbc.downsample(moment_downsampled,  opMode_downsampled, sample_size)
    data = {"moment": n_moment_downsampled
            , "voltage": n_voltage_downsampled
            , "current": n_current_downsampled
            , "power_W": n_power_W_downsampled
            , "power_factor_measured": n_power_factor_measured_downsampled
            , "power_factor_calc": n_power_factor_calc_downsampled
            , "phase_angle_measured": n_phase_angle_measured_downsampled
            , "phase_angle_calc": n_phase_angle_calc_downsampled
            , "opMode": n_opMode_downsampled
            }
    final_df = pl.DataFrame(data)
    final_df = final_df.with_columns(pl.col("moment").apply(lambda x:datetime.fromtimestamp(x)))
    final_df = final_df.with_columns(pl.col("moment").dt.strftime("%Y-%U").alias('week'))
    final_df = final_df.filter(pl.col("moment").is_between(date_select[0],date_select[1]))
    return final_df



charts = {
    'Tensão': lambda df: px.scatter( x = df_final['moment'], y = df_final['voltage'], title='Tensão [V]', labels = {'voltage': 'Tensão', 'moment': 'Horário'}, render_mode='webgl'),
    'Corrente': lambda df_final: px.scatter( x = df_final['moment'], y = df_final['current'], title='Corrente [A]',  labels = {'current': 'Corrente', 'moment': 'Horário'}, render_mode='webgl'),
    'Potência': lambda df_final: px.scatter( x = df_final['moment'], y = df_final['power_W'], title='Potência [W]',  labels = {'power_W': 'Potência', 'moment': 'Horário'}, render_mode='webgl')
    ##ARRUMAR ESSES DOIS GRAFICOS
    #'Fator de Potência': lambda df: px.scatter( x = df['moment'], y = df.select(pl.col(['power_factor_measured', 'power_factor_calc'])), title='Fator de Potência',  color_discrete_map = {'power_factor_measured': 'green', 'power_factor_calc': 'blue'} , labels = {'power_factor_measured': 'Medido', 'power_factor_calc': 'Calculado', 'moment': 'Horário'}, render_mode='webgl'),
    #'Ângulo de Fase' : lambda df: px.scatter(x = df['moment'], y = df.select(pl.col(["phase_angle_measured", "phase_angle_calc"])),  title='Ângulo de Fase [Graus]',  color_discrete_map = {'phase_angle_measured': 'green', 'phase_angle_calc': 'blue'} , labels = {'phase_angle_measured': 'Medido', 'phase_angle_calc': 'Calculado', 'moment': 'Horário'}, render_mode='webgl'),
}

connectionstring = "mysql://python:python@utfpr-pi2-compressor-monitor.mysql.database.azure.com:3306/pi2"
column_names = ['moment', 'voltage', 'current', 'power_W', 'energy_WH', 'power_factor_measured', 'power_factor_calc', 'phase_angle_measured', 'phase_angle_calc', 'opMode']
mapping = {1: 'On', 2: 'StandBy', 0: 'Off'}

measuringTime = 1
tableName = 'compressor_measurements'


conn = pymysql.connect(host='utfpr-pi2-compressor-monitor.mysql.database.azure.com',
                       user='pi2root',
                       password='UTFPR@senha',
                       database='pi2')

if 'min' not in st.session_state:
    query = "SELECT moment , voltage, current, power_W, power_factor_measured, power_factor_calc, phase_angle_measured, phase_angle_calc, opMode FROM " + tableName + ";"
    st.session_state.df = cx.read_sql(connectionstring, query, return_type = "polars")
    st.session_state.min = st.session_state.df['moment'].min()
    st.session_state.min_selected = st.session_state.df['moment'].min()
    st.session_state.max_selected = st.session_state.df['moment'].max()
    st.session_state.max= st.session_state.df['moment'].max()
    
    if isinstance(st.session_state.min, str):
        st.session_state.min = datetime.strptime(st.session_state.min, '%Y-%m-%d %H:%M:%S')
    if isinstance(st.session_state.max, str):
        st.session_state.max = datetime.strptime(st.session_state.max, '%Y-%m-%d %H:%M:%S')


page1 = "Monitoramento Compressor - UTFPR"
st.set_page_config(page_title=page1)
st.markdown("# " + page1)
st.write(
    "Escolha os limites de data que você quer ver o funcionamento do compressor da UTFPR: "
)

date_select = st.slider('Select the time range:',
                        value=( st.session_state.min_selected, st.session_state.max_selected),
                        min_value=st.session_state.min,
                        max_value=st.session_state.max,
                        format="DD/MM/YY - hh:mm",
                        step=timedelta(hours=8),
                        key=("slider"))

st.sidebar.header("Data das informações: \n" + str(date_select[0]) + " até \n" + str(date_select[1]))
charts_selected = st.multiselect('Selecione os gráficos que deseja ver:', list(charts.keys()), default=list(charts.keys()))

df_final = load_data(date_select,st.session_state.df)
print(df_final.head())
print(df_final.dtypes)

for chart_name in charts_selected:
    chart_function = charts[chart_name]
    with st.container():
        fig = chart_function(df_final)
        st.plotly_chart(fig, use_container_width=True)


#############TENQ ARRUMAR ISSO AQUI

# qtyOff = df[df['opMode'] == 0]['opMode'].count()
# qtyOffSec = qtyOff * measuringTime

# qtyOn = df[df['opMode'] == 1]['opMode'].count()
# qtyOnSec = qtyOn * measuringTime

# qtyStandby = df[df['opMode'] == 2]['opMode'].count()
# qtyStandbySec = qtyStandby * measuringTime


# with st.container():
#     st.write("Modos de operação")
#     stackeddf = df
#     stackeddf['moment'] = pd.to_datetime(stackeddf['moment']).dt.strftime('%Y-%m-%d')
#     dailyValues = stackeddf.groupby(['moment','opMode']).size()
#     result_df = dailyValues.apply(lambda x: round((x)/60),2).reset_index(name='result')
#     groupedAgain = result_df.groupby(['moment', 'opMode'])['result'].sum().reset_index()
#     groupedAgain['opMode'] = groupedAgain['opMode'].replace(mapping)
#     fig = px.bar(groupedAgain,  x='moment',  y='result', color='opMode', labels = {'result': 'Tempo de operação (m)', 'moment': 'Horário','opMode':'Modo de Operação' })
#     st.plotly_chart(fig, use_container_width=True)



#Para as métricas de modo de operação, quantas vezes ficou ligado, quantas vezes desligado, o outro modo de operação lá e por fim a qtd de Ah do período
with st.sidebar:
    if (len(df_final['current']) != 0):
        currentAvg = df_final['current'].mean()
        powerFacAvg = df_final['power_factor_calc'].mean()
        st.metric("Corrente Média no período",  str(round(currentAvg, 3)) + " A")
        st.metric("Fator de Potência calculado no período", round(powerFacAvg, 3))
        ##ARRUMAR LA EM CIMA PRA PODER PRINTAR METRICAS
        # st.metric("Tempo desligado durante o período", seconds_to_hours(qtyOffSec))
        # st.metric("Tempo ligado durante o período", seconds_to_hours(qtyOnSec))
        # st.metric("Tempo em standby durante o período", seconds_to_hours(qtyStandbySec))

st.text('Lucas Moletta')
