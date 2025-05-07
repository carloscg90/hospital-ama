
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Conexión a la base de datos
conn = sqlite3.connect('hospital_ama.db')

st.set_page_config(layout="wide")
st.title("📝 Dashboard Hospital_ama")

# Filtros en barra lateral
with st.sidebar:
    st.header("🎛️ Filtros generales")
    
    estados = pd.read_sql_query("SELECT DISTINCT estado FROM Citas", conn)['estado'].tolist()
    estado_sel = st.multiselect("Estado de la cita", estados, default=estados)

    doctores = pd.read_sql_query("SELECT DISTINCT nombre FROM Doctores", conn)['nombre'].tolist()
    doctor_sel = st.selectbox("Doctor", ["Todos"] + doctores)

    servicios = pd.read_sql_query("SELECT DISTINCT nombre_servicio FROM Servicios", conn)['nombre_servicio'].tolist()
    servicio_sel = st.multiselect("Servicio", servicios, default=servicios)

    fecha_min, fecha_max = pd.read_sql_query("SELECT MIN(fecha), MAX(fecha) FROM Citas", conn).iloc[0]
    fecha_rango = st.date_input("Rango de fechas", [fecha_min, fecha_max])

    paciente_input = st.text_input("Buscar paciente por nombre (opcional)")
    tipo_grafico = st.radio("Tipo de gráfico por estado", ["Torta", "Barras"], horizontal=True)

tabs = st.tabs(["📊 Citas por Estado", "👨‍⚕️ Citas por Doctor", "💰 Ingresos por Servicio", "📅 Citas por Fecha", "🧾 Detalle de Citas"])



# TAB 1 - Citas por Estado
with tabs[0]:
    st.subheader("Distribución de Citas por Estado")

    query_base = f'''
        SELECT estado, COUNT(*) AS total_citas
        FROM Citas c
        JOIN Pacientes p ON c.paciente_id = p.id
        WHERE c.estado IN ({','.join(['?'] * len(estado_sel))})
          AND c.fecha BETWEEN ? AND ?
    '''
    params1 = estado_sel + [str(fecha_rango[0]), str(fecha_rango[1])]

    if paciente_input:
        query_base += " AND LOWER(p.nombre) LIKE ?"
        params1.append(f"%{paciente_input.lower()}%")

    query_base += " GROUP BY estado"

    df_estado = pd.read_sql_query(query_base, conn, params=params1)
    st.dataframe(df_estado)

    if tipo_grafico == "Torta":
        fig1 = px.pie(df_estado, names="estado", values="total_citas", title="Distribución de Citas por Estado", hole=0.3)
    else:
        fig1 = px.bar(df_estado, x="estado", y="total_citas", text="total_citas", title="Distribución de Citas por Estado")

    st.plotly_chart(fig1, use_container_width=True)


# TAB 2 - Citas por Doctor
with tabs[1]:
    st.subheader("Citas por Doctor")
    query2 = f'''
        SELECT d.nombre AS doctor, COUNT(*) AS total_citas
        FROM Citas c
        JOIN Doctores d ON c.doctor_id = d.id
        WHERE fecha BETWEEN ? AND ?
        {'AND d.nombre = ?' if doctor_sel != "Todos" else ""}
        GROUP BY d.nombre
        ORDER BY total_citas DESC
    '''
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
    query3 = f'''
        SELECT s.nombre_servicio AS servicio, SUM(s.precio) AS total_ingresos
        FROM Citas c
        JOIN Servicios s ON c.servicio_id = s.id
        WHERE c.estado = 'Confirmada'
          AND fecha BETWEEN ? AND ?
          AND s.nombre_servicio IN ({','.join(['?'] * len(servicio_sel))})
        GROUP BY s.nombre_servicio
        ORDER BY total_ingresos DESC
    '''
    params3 = [str(fecha_rango[0]), str(fecha_rango[1])] + servicio_sel
    df_servicio = pd.read_sql_query(query3, conn, params=params3)
    st.dataframe(df_servicio)
    fig3 = px.bar(df_servicio, y="servicio", x="total_ingresos", orientation="h", text="total_ingresos", title="Ingresos por Servicio")
    st.plotly_chart(fig3, use_container_width=True)

    st.download_button("⬇️ Descargar tabla", data=df_servicio.to_csv(index=False), file_name="ingresos_servicio.csv", mime="text/csv")

# TAB 4 - Citas por Fecha
with tabs[3]:
    st.subheader("Citas por Día")
    query4 = f'''
        SELECT fecha, COUNT(*) AS total_citas
        FROM Citas
        WHERE fecha BETWEEN ? AND ?
        GROUP BY fecha
        ORDER BY fecha
    '''
    df_fecha = pd.read_sql_query(query4, conn, params=[str(fecha_rango[0]), str(fecha_rango[1])])
    st.line_chart(df_fecha.set_index("fecha"))

# TAB 5 - Detalle de Citas
with tabs[4]:
    st.subheader("🔍 Detalle de todas las citas filtradas")
    query5 = f'''
        SELECT c.id, p.nombre AS paciente, d.nombre AS doctor, s.nombre_servicio AS servicio,
               c.fecha, c.hora, c.estado
        FROM Citas c
        JOIN Pacientes p ON c.paciente_id = p.id
        JOIN Doctores d ON c.doctor_id = d.id
        JOIN Servicios s ON c.servicio_id = s.id
        WHERE c.estado IN ({','.join(['?'] * len(estado_sel))})
          AND c.fecha BETWEEN ? AND ?
          AND s.nombre_servicio IN ({','.join(['?'] * len(servicio_sel))})
          {'AND d.nombre = ?' if doctor_sel != "Todos" else ""}
        ORDER BY c.fecha, c.hora
    '''
    params5 = estado_sel + [str(fecha_rango[0]), str(fecha_rango[1])] + servicio_sel
    if doctor_sel != "Todos":
        params5.append(doctor_sel)
    df_detalle = pd.read_sql_query(query5, conn, params=params5)
    st.dataframe(df_detalle, use_container_width=True)

conn.close()
