import streamlit as st

# ---------------- CONFIGURACIÓN ----------------
st.set_page_config(
    page_title="Sistema Predictivo de Enfermedades Crónicas",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- ESTILOS CSS ----------------
st.markdown("""
<style>
    .main {
        background-color: #f3f4f6;
    }

    .title-bar {
        background-color: #1f5fbf;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 20px;
    }

    .card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }

    .risk-high {
        background-color: #ef4444;
        color: white;
        text-align: center;
        padding: 20px;
        border-radius: 10px;
        font-size: 40px;
        font-weight: bold;
    }

    .risk-bar {
        display: flex;
        margin-top: 20px;
        margin-bottom: 20px;
        border-radius: 10px;
        overflow: hidden;
    }

    .low {
        flex: 1;
        background-color: #65a30d;
        color: white;
        text-align: center;
        padding: 15px;
        font-weight: bold;
    }

    .medium {
        flex: 1;
        background-color: #eab308;
        color: white;
        text-align: center;
        padding: 15px;
        font-weight: bold;
    }

    .high {
        flex: 1;
        background-color: #dc2626;
        color: white;
        text-align: center;
        padding: 15px;
        font-weight: bold;
    }

    .recommendation {
        font-size: 18px;
        line-height: 1.8;
    }

</style>
""", unsafe_allow_html=True)

# ---------------- ENCABEZADO ----------------
st.markdown("""
<div class="title-bar">
    <h1>🫀 Sistema Predictivo de Enfermedades Crónicas</h1>
    <h3>Predicción de riesgo cardiovascular y enfermedades crónicas</h3>
</div>
""", unsafe_allow_html=True)

# ---------------- COLUMNAS ----------------
col1, col2 = st.columns([1, 1])

# ---------------- PANEL IZQUIERDO ----------------
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Datos del Paciente")

    edad = st.number_input("Edad", min_value=1, max_value=100, value=58)
    peso = st.number_input("Peso (kg)", min_value=1.0, max_value=200.0, value=85.0)
    altura = st.number_input("Altura (cm)", min_value=50.0, max_value=250.0, value=170.0)

    sistolica = st.number_input("Presión Sistólica", value=150)
    diastolica = st.number_input("Presión Diastólica", value=95)

    glucosa = st.number_input("Glucosa", value=130)
    colesterol = st.number_input("Colesterol", value=230)

    fumador = st.selectbox("Fumador", ["Sí", "No"])
    alcohol = st.selectbox("Consumo de Alcohol", ["Sí", "No"])
    actividad = st.selectbox("Actividad Física", ["Sí", "No"])

    predecir = st.button("Predecir Riesgo", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- PANEL DERECHO ----------------
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Resultado de la Predicción")

    # Simulación del resultado
    riesgo = 82

    if predecir:
        st.markdown("""
        <div class="risk-high">
            ALTO RIESGO
        </div>
        """, unsafe_allow_html=True)

        st.markdown(
            f"<h2 style='margin-top:20px;'>Probabilidad Estimada: <b>{riesgo}%</b></h2>",
            unsafe_allow_html=True
        )

        st.markdown("""
        <div class="risk-bar">
            <div class="low">Bajo</div>
            <div class="medium">Moderado</div>
            <div class="high">Alto</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="recommendation">
            <h3>Recomendaciones:</h3>
            <ul>
                <li>Paciente con alta probabilidad de enfermedad crónica.</li>
                <li>Remitir a medicina interna.</li>
                <li>Realizar perfil lipídico y control en 30 días.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
