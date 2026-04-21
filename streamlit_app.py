import streamlit as st
import pandas as pd
import joblib

# ---------------- CARGA ----------------
modelo = joblib.load("modelo_xgb.pkl")
scaler = joblib.load("scaler.pkl")

st.set_page_config(
    page_title="Predicción Clínica",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
.main {
    background-color: #f3f4f6;
}

.title-box {
    background-color: #1f5fbf;
    padding: 20px;
    border-radius: 12px;
    color: white;
    text-align: center;
    margin-bottom: 20px;
}

.result-box {
    padding: 20px;
    border-radius: 12px;
    color: white;
    text-align: center;
    font-size: 35px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="title-box">
    <h1>🫀 Sistema Predictivo de Enfermedades Crónicas</h1>
    <h3>Modelo XGBoost en Atención Primaria</h3>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

# ---------------- FORMULARIO ----------------
with col1:
    st.subheader("Datos del Paciente")

    edad = st.number_input("Edad", 1, 100, 58)
    genero = st.selectbox("Género", [1, 2])

    altura = st.number_input("Altura (cm)", 100, 250, 170)
    peso = st.number_input("Peso (kg)", 30, 200, 85)

    ap_hi = st.number_input("Presión Sistólica", 80, 250, 150)
    ap_lo = st.number_input("Presión Diastólica", 50, 150, 95)

    colesterol = st.selectbox("Colesterol", [1, 2, 3])
    glucosa = st.selectbox("Glucosa", [1, 2, 3])

    fuma = st.selectbox("Fumador", [0, 1])
    alcohol = st.selectbox("Alcohol", [0, 1])
    actividad = st.selectbox("Actividad Física", [0, 1])

    predecir = st.button("Predecir Riesgo")

# ---------------- PREDICCIÓN ----------------
with col2:
    st.subheader("Resultado")

    if predecir:
        bmi = peso / ((altura / 100) ** 2)
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
            "bmi": [bmi]
})

# Reordenar según el scaler
datos = datos[scaler.feature_names_in_]

datos_scaled = scaler.transform(datos)

prob = modelo.predict_proba(datos_scaled)[0][1]
riesgo = round(prob * 100, 2)

if riesgo >= 70:
    color = "#dc2626"
    texto = "ALTO RIESGO"
elif riesgo >= 40:
    color = "#eab308"
    texto = "RIESGO MODERADO"
else:
    color = "#16a34a"
    texto = "BAJO RIESGO"

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

st.subheader("Recomendaciones")

if riesgo >= 70:
    st.error("Paciente con alta probabilidad de enfermedad crónica.")
    st.write("• Remisión inmediata")
    st.write("• Perfil lipídico")
    st.write("• Seguimiento en 30 días")

elif riesgo >= 40:
    st.warning("Seguimiento preventivo recomendado.")
    st.write("• Control médico")
    st.write("• Cambios de estilo de vida")

else:
    st.success("Riesgo bajo.")
    st.write("• Mantener hábitos saludables")
