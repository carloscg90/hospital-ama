import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Conexión a la base de datos
conn = sqlite3.connect('hospital_ama.db')

st.set_page_config(layout="wide")
st.title("📝 Informe Interactivo de Citas e Ingresos")

with st.sidebar:
    st.header("🎛️ Filtros")
    estados = pd.read_sql_query("SELECT DISTINCT estado FROM Citas", conn)['estado'].tolist()
    estado_sel = st.multiselect("Estado de la cita", estados, default=estados)

    doctores = pd.read_sql_query("SELECT DISTINCT nombre FROM Doctores", conn)['nombre'].tolist()
    doctor_sel = st.selectbox("Doctor", ["Todos"] + doctores)

    fecha_min, fecha_max = pd.read_sql_query("SELECT MIN(fecha), MAX(fecha) FROM Citas", conn).iloc[0]
    fecha_rango = st.date_input("Rango de fechas", [fecha_min, fecha_max])

tabs = st.tabs(["📊 Citas por Estado", "👨‍⚕️ Citas por Doctor", "💰 Ingresos por Servicio"])

# TAB 1 - Citas por Estado
with tabs[0]:
    st.subheader("Distribución de Citas por Estado")
    query1 = f"""
        SELECT estado, COUNT(*) AS total_citas
        FROM Citas
        WHERE estado IN ({','.join(['?'] * len(estado_sel))})
          AND fecha BETWEEN ? AND ?
        GROUP BY estado
    """
    params1 = estado_sel + [str(fecha_rango[0]), str(fecha_rango[1])]
    df_estado = pd.read_sql_query(query1, conn, params=params1)
    st.dataframe(df_estado)
    fig1 = px.bar(df_estado, x="estado", y="total_citas", text="total_citas", title="Citas por Estado")
    st.plotly_chart(fig1, use_container_width=True)

# TAB 2 - Citas por Doctor
with tabs[1]:
    st.subheader("Citas por Doctor")
    query2 = f"""
        SELECT d.nombre AS doctor, COUNT(*) AS total_citas
        FROM Citas c
        JOIN Doctores d ON c.doctor_id = d.id
        WHERE fecha BETWEEN ? AND ?
        {"AND d.nombre = ?" if doctor_sel != "Todos" else ""}
        GROUP BY d.nombre
        ORDER BY total_citas DESC
    """
    params2 = [str(fecha_rango[0]), str(fecha_rango[1])]
    if doctor_sel != "Todos":
        params2.append(doctor_sel)
    df_doctor = pd.read_sql_query(query2, conn, params=params2)
    st.dataframe(df_doctor)
    fig2 = px.bar(df_doctor, y="doctor", x="total_citas", orientation="h", text="total_citas", title="Citas por Doctor")
    st.plotly_chart(fig2, use_container_width=True)

# TAB 3 - Ingresos por Servicio
with tabs[2]:
    st.subheader("Ingresos por Tipo de Servicio")
    query3 = f"""
        SELECT s.nombre_servicio AS servicio, SUM(s.precio) AS total_ingresos
        FROM Citas c
        JOIN Servicios s ON c.servicio_id = s.id
        WHERE c.estado = 'Confirmada'
          AND fecha BETWEEN ? AND ?
        GROUP BY s.nombre_servicio
        ORDER BY total_ingresos DESC
    """
    params3 = [str(fecha_rango[0]), str(fecha_rango[1])]
    df_servicio = pd.read_sql_query(query3, conn, params=params3)
    st.dataframe(df_servicio)
    fig3 = px.bar(df_servicio, y="servicio", x="total_ingresos", orientation="h", text="total_ingresos", title="Ingresos por Servicio")
    st.plotly_chart(fig3, use_container_width=True)

    # Botón para descargar
    st.download_button("⬇️ Descargar tabla", data=df_servicio.to_csv(index=False), file_name="ingresos_servicio.csv", mime="text/csv")

conn.close()

fig_servicio.update_traces(texttemplate='$%{text:,.2f}')
st.plotly_chart(fig_servicio)

st.markdown("💰 Los ingresos varían según el tipo de servicio prestado. Esta vista permite identificar los más rentables.")
