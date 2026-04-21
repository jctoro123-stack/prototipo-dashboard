import streamlit as st
import pandas as pd
import joblib

# ---------------- CONFIGURACIÓN ----------------
st.set_page_config(
    page_title="Sistema Predictivo de Enfermedades Crónicas",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- CARGAR MODELO ----------------
modelo = joblib.load("modelo_xgb.pkl")
scaler = joblib.load("scaler.pkl")

# ---------------- ESTILOS ----------------
st.markdown("""
<style>
.main {
    background-color: #f3f4f6;
}

.title-box {
    background-color: #1f5fbf;
    padding: 20px;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin-bottom: 20px;
}

.result-box {
    padding: 20px;
    border-radius: 15px;
    color: white;
    text-align: center;
    font-size: 35px;
    font-weight: bold;
    margin-top: 20px;
}

.recommendation-box {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- ENCABEZADO ----------------
st.markdown("""
<div class="title-box">
    <h1>🫀 Sistema Predictivo de Enfermedades Crónicas</h1>
    <h3>Modelo Predictivo con XGBoost para Atención Primaria</h3>
</div>
""", unsafe_allow_html=True)

# ---------------- COLUMNAS ----------------
col1, col2 = st.columns([1, 1])

# ---------------- FORMULARIO ----------------
with col1:
    st.subheader("📋 Datos del Paciente")

    edad = st.number_input("Edad", min_value=1, max_value=100, value=58)
    genero = st.selectbox("Género", [1, 2], format_func=lambda x: "Masculino" if x == 1 else "Femenino")

    altura = st.number_input("Altura (cm)", min_value=100, max_value=250, value=170)
    peso = st.number_input("Peso (kg)", min_value=30, max_value=200, value=85)

    ap_hi = st.number_input("Presión Sistólica", min_value=80, max_value=250, value=150)
    ap_lo = st.number_input("Presión Diastólica", min_value=50, max_value=150, value=95)

    colesterol = st.selectbox(
        "Nivel de Colesterol",
        [1, 2, 3],
        format_func=lambda x: {
            1: "Normal",
            2: "Por encima de lo normal",
            3: "Muy alto"
        }[x]
    )

    glucosa = st.selectbox(
        "Nivel de Glucosa",
        [1, 2, 3],
        format_func=lambda x: {
            1: "Normal",
            2: "Por encima de lo normal",
            3: "Muy alto"
        }[x]
    )

    fuma = st.selectbox("Fumador", [0, 1], format_func=lambda x: "Sí" if x == 1 else "No")
    alcohol = st.selectbox("Consume Alcohol", [0, 1], format_func=lambda x: "Sí" if x == 1 else "No")
    actividad = st.selectbox("Actividad Física", [0, 1], format_func=lambda x: "Sí" if x == 1 else "No")

    predecir = st.button("🔍 Predecir Riesgo", use_container_width=True)

# ---------------- RESULTADO ----------------
with col2:
    st.subheader("📊 Resultado")

    if predecir:
        # Calcular IMC
        imc = peso / ((altura / 100) ** 2)

        # Crear DataFrame
        datos = pd.DataFrame({
            "age": [edad],
            "gender": [genero],
            "height": [altura],
            "weight": [peso],
            "ap_hi": [ap_hi],
            "ap_lo": [ap_lo],
            "cholesterol": [colesterol],
            "gluc": [glucosa],
            "smoke": [fuma],
            "alco": [alcohol],
            "active": [actividad],
            "imc": [imc]
        })

        # Escalar
        datos_scaled = scaler.transform(datos)

        # Predicción
        prob = modelo.predict_proba(datos_scaled)[0][1]
        riesgo = round(prob * 100, 1)

        # Clasificación del riesgo
        if riesgo >= 70:
            color = "#dc2626"
            texto = "🔴 ALTO RIESGO"
        elif riesgo >= 40:
            color = "#eab308"
            texto = "🟡 RIESGO MODERADO"
        else:
            color = "#16a34a"
            texto = "🟢 BAJO RIESGO"

        # Mostrar resultado
        st.markdown(
            f"""
            <div class="result-box" style="background-color:{color};">
                {texto}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.metric("Probabilidad estimada", f"{riesgo}%")
        st.progress(int(riesgo))

        # Mostrar IMC
        st.metric("IMC calculado", f"{imc:.2f}")

        # Recomendaciones
        st.markdown('<div class="recommendation-box">', unsafe_allow_html=True)
        st.subheader("🩺 Recomendaciones Clínicas")

        if riesgo >= 70:
            st.error("Paciente con alta probabilidad de enfermedad cardiovascular.")
            st.write("• Remisión inmediata a medicina interna")
            st.write("• Control prioritario de presión arterial")
            st.write("• Solicitar perfil lipídico y glucosa")
            st.write("• Seguimiento en 30 días")

        elif riesgo >= 40:
            st.warning("Riesgo moderado, se recomienda seguimiento preventivo.")
            st.write("• Control médico periódico")
            st.write("• Mejorar hábitos alimenticios")
            st.write("• Incrementar actividad física")
            st.write("• Reevaluación en 60 días")

        else:
            st.success("Riesgo bajo.")
            st.write("• Mantener hábitos saludables")
            st.write("• Seguimiento preventivo anual")

        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.info("Ingrese los datos del paciente y presione **Predecir Riesgo**.")
