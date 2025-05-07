
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Título
st.title("Análisis Visual de Datos desde Archivos CSV")

# Cargar datos desde CSVs
citas_estado = pd.read_csv("citas_estado.csv")
citas_doctor = pd.read_csv("citas_doctor.csv")
ingresos_servicio = pd.read_csv("ingresos_servicio.csv")

# Crear 3 columnas para mostrar las gráficas una al lado de otra
col1, col2, col3 = st.columns(3)

# 1. Citas por estado
with col1:
    fig1, ax1 = plt.subplots()
    bars = ax1.bar(citas_estado['estado'], citas_estado['total_citas'], color='skyblue')
    ax1.set_title("Citas por estado")
    ax1.set_xlabel("Estado")
    ax1.set_ylabel("Total")
    for bar in bars:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, yval + 0.5, int(yval), ha='center', va='bottom')
    st.pyplot(fig1)

# 2. Citas por doctor
with col2:
    fig2, ax2 = plt.subplots()
    bars = ax2.barh(citas_doctor['doctor'], citas_doctor['total_citas'], color='lightgreen')
    ax2.set_title("Citas por doctor")
    ax2.set_xlabel("Total")
    ax2.set_ylabel("Doctor")
    for bar in bars:
        ax2.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, int(bar.get_width()), va='center')
    st.pyplot(fig2)

# 3. Ingresos por servicio
with col3:
    fig3, ax3 = plt.subplots()
    bars = ax3.barh(ingresos_servicio['servicio'], ingresos_servicio['total_ingresos'], color='salmon')
    ax3.set_title("Ingresos por servicio confirmado")
    ax3.set_xlabel("Ingresos")
    ax3.set_ylabel("Servicio")
    for bar in bars:
        ax3.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, f"${bar.get_width():,.2f}", va='center')
    st.pyplot(fig3)
