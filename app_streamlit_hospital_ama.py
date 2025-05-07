import streamlit as st
import pandas as pd
import plotly.express as px

# Título centrado
st.markdown("<h1 style='text-align: center;'>📝 Informe Interactivo de Citas e Ingresos</h1>", unsafe_allow_html=True)

st.markdown("""
Este informe presenta un análisis exploratorio basado en los siguientes conjuntos de datos:
- Citas médicas agrupadas por estado
- Citas médicas por doctor
- Ingresos confirmados por tipo de servicio

Los datos provienen de archivos CSV estructurados y serán visualizados de forma interactiva.
""")

# 1. Citas por estado
st.header("1️⃣ Citas por estado")
df_estado = pd.read_csv("citas_estado.csv")
st.dataframe(df_estado)

fig_estado = px.bar(df_estado, x="estado", y="total_citas", title="Distribución de Citas por Estado", text="total_citas")
st.plotly_chart(fig_estado)

st.markdown("🔍 Observamos cómo varía el número total de citas médicas según el estado registrado.")

# 2. Citas por doctor
st.header("2️⃣ Citas por doctor")
df_doctor = pd.read_csv("citas_doctor.csv")
st.dataframe(df_doctor)

fig_doctor = px.bar(df_doctor, y="doctor", x="total_citas", orientation="h", title="Citas Atendidas por Cada Doctor", text="total_citas")
st.plotly_chart(fig_doctor)

st.markdown("📌 Esta sección muestra cuántas citas ha manejado cada doctor registrado en el sistema.")

# 3. Ingresos por servicio
st.header("3️⃣ Ingresos confirmados por servicio")
df_servicio = pd.read_csv("ingresos_servicio.csv")
st.dataframe(df_servicio)

fig_servicio = px.bar(df_servicio, y="servicio", x="total_ingresos", orientation="h", title="Ingresos por Tipo de Servicio", text="total_ingresos")
fig_servicio.update_traces(texttemplate='$%{text:,.2f}')
st.plotly_chart(fig_servicio)

st.markdown("💰 Los ingresos varían según el tipo de servicio prestado. Esta vista permite identificar los más rentables.")
