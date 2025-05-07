
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Título centrado
st.markdown("<h1 style='text-align: center;'>Análisis Visual de Datos Hospital_ama</h1>", unsafe_allow_html=True)

# Cargar datos desde CSVs
citas_estado = pd.read_csv("citas_estado.csv")
citas_doctor = pd.read_csv("citas_doctor.csv")
ingresos_servicio = pd.read_csv("ingresos_servicio.csv")

# --- Crear los gráficos ---
# Gráfico 1: Citas por estado
fig1, ax1 = plt.subplots(figsize=(10, 6))
bars = ax1.bar(citas_estado['estado'], citas_estado['total_citas'], color='skyblue')
ax1.set_title("Citas por estado")
ax1.set_xlabel("Estado")
ax1.set_ylabel("Total")
for bar in bars:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, yval + 0.5, int(yval), ha='center', va='bottom')

# Gráfico 2: Citas por doctor
fig2, ax2 = plt.subplots(figsize=(10, 6))
bars = ax2.barh(citas_doctor['doctor'], citas_doctor['total_citas'], color='lightgreen')
ax2.set_title("Citas por doctor")
ax2.set_xlabel("Total")
ax2.set_ylabel("Doctor")
for bar in bars:
    ax2.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, int(bar.get_width()), va='center')

# Gráfico 3: Ingresos por servicio
fig3, ax3 = plt.subplots(figsize=(10, 6))
bars = ax3.barh(ingresos_servicio['servicio'], ingresos_servicio['total_ingresos'], color='salmon')
ax3.set_title("Ingresos por servicio confirmado")
ax3.set_xlabel("Ingresos")
ax3.set_ylabel("Servicio")
for bar in bars:
    ax3.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, f"${bar.get_width():,.2f}", va='center')

# --- Método de visualización ---
modo = st.radio("¿Cómo quieres ver los gráficos?", ["Menú desplegable", "Pestañas"])

if modo == "Menú desplegable":
    opcion = st.selectbox("Selecciona el gráfico a visualizar:", [
        "Citas por estado",
        "Citas por doctor",
        "Ingresos por servicio confirmado"
    ])
    if opcion == "Citas por estado":
        st.pyplot(fig1)
    elif opcion == "Citas por doctor":
        st.pyplot(fig2)
    else:
        st.pyplot(fig3)
else:
    tab1, tab2, tab3 = st.tabs(["📊 Citas por estado", "👨‍⚕️ Citas por doctor", "💰 Ingresos por servicio"])
    with tab1:
        st.pyplot(fig1)
    with tab2:
        st.pyplot(fig2)
    with tab3:
        st.pyplot(fig3)
