import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Conexión a la base de datos SQLite
conn = sqlite3.connect('hospital_ama.db')

st.markdown("<h1 style='text-align: center;'>📝 Informe Interactivo de Citas e Ingresos</h1>", unsafe_allow_html=True)

st.markdown("""
Este informe presenta un análisis exploratorio basado en los siguientes datos:
- Citas médicas agrupadas por estado
- Citas médicas por doctor
- Ingresos confirmados por tipo de servicio

Los datos provienen de la base de datos SQLite y serán visualizados de forma interactiva.
""")

# 1. Citas por estado
st.header("1️⃣ Citas por estado")

query_estado = """
SELECT estado, COUNT(*) AS total_citas
FROM Citas
GROUP BY estado
ORDER BY total_citas DESC;
"""
df_estado = pd.read_sql_query(query_estado, conn)
st.dataframe(df_estado)

fig_estado = px.bar(df_estado, x="estado", y="total_citas", title="Distribución de Citas por Estado", text="total_citas")
st.plotly_chart(fig_estado)

st.markdown("🔍 Observamos cómo varía el número total de citas médicas según el estado registrado.")

# 2. Citas por doctor
st.header("2️⃣ Citas por doctor")

query_doctor = """
SELECT d.nombre AS doctor, COUNT(*) AS total_citas
FROM Citas c
JOIN Doctores d ON c.doctor_id = d.id
GROUP BY d.nombre
ORDER BY total_citas DESC;
"""
df_doctor = pd.read_sql_query(query_doctor, conn)
st.dataframe(df_doctor)

fig_doctor = px.bar(df_doctor, y="doctor", x="total_citas", orientation="h", title="Citas Atendidas por Cada Doctor", text="total_citas")
st.plotly_chart(fig_doctor)

st.markdown("📌 Esta sección muestra cuántas citas ha manejado cada doctor registrado en el sistema.")

# 3. Ingresos por servicio (asumimos que precio * cantidad = ingreso y todas las citas están confirmadas)
st.header("3️⃣ Ingresos confirmados por servicio")

query_servicio = """
SELECT s.nombre_servicio AS servicio, SUM(s.precio) AS total_ingresos
FROM Citas c
JOIN Servicios s ON c.servicio_id = s.id
WHERE c.estado = 'Confirmada'
GROUP BY s.nombre_servicio
ORDER BY total_ingresos DESC;
"""
df_servicio = pd.read_sql_query(query_servicio, conn)
st.dataframe(df_servicio)

fig_servicio = px.bar(df_servicio, y="servicio", x="total_ingresos", orientation="h", title="Ingresos por Tipo de Servicio", text="total_ingresos")
st.plotly_chart(fig_servicio)

conn.close()
fig_servicio.update_traces(texttemplate='$%{text:,.2f}')
st.plotly_chart(fig_servicio)

st.markdown("💰 Los ingresos varían según el tipo de servicio prestado. Esta vista permite identificar los más rentables.")
