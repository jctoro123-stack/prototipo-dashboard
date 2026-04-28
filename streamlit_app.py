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
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

.main-title {
    background: linear-gradient(135deg, #1f5fbf, #2563eb);
    color: white;
    padding: 1.5rem;
    border-radius: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    margin-bottom: 1.5rem;
}

.card {
    background: white;
    border-radius: 20px;
    padding: 1.5rem;
    box-shadow: 0 4px 15px rgba(0,0,0,0.06);
    border: 1px solid #e5e7eb;
}

.result-card {
    border-radius: 20px;
    padding: 1.5rem;
    text-align: center;
    color: white;
    font-weight: bold;
    font-size: clamp(22px, 3vw, 36px);
    margin-bottom: 1rem;
}

.metric-card {
    background: #f8fafc;
    padding: 1rem;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
}

@media (max-width: 768px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .main-title {
        padding: 1rem;
        border-radius: 16px;
    }

    .card {
        padding: 1rem;
        border-radius: 16px;
    }

    .result-card {
        padding: 1rem;
        font-size: 22px;
    }
}
</style>
""", unsafe_allow_html=True)
# ---------------- ENCABEZADO ----------------
st.markdown("""
<div class='main-title'>
    <h1 style='margin:0;'>🫀 Sistema Predictivo de Enfermedades Crónica</h1>
    <p style='margin:0.5rem 0 0 0; font-size: 18px;'>Predicción de riesgo cardiovascular con XGBoost</p>
</div>
""", unsafe_allow_html=True)

# ================= LAYOUT =================
left_col, right_col = st.columns([1.1, 1], gap="large")

with left_col:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📋 Datos del paciente")

    c1, c2 = st.columns(2)
    with c1:
        edad = st.number_input("Edad", 1, 100, 58)
        altura = st.number_input("Altura (cm)", 100, 250, 170)
        ap_hi = st.number_input("Presión sistólica", 80, 250, 150)
        colesterol = st.selectbox(
        "Nivel de Colesterol",
        [1, 2, 3],
        format_func=lambda x: {
            1: "Normal",
            2: "Por encima de lo normal",
            3: "Muy alto"
        }[x]
    )
        fuma = st.selectbox("Fumador", [0, 1], format_func=lambda x: "No" if x == 1 else "Sí")

    with c2:
        genero = st.selectbox("Género", [1, 2], format_func=lambda x: "Masculino" if x == 1 else "Femenino")
        peso = st.number_input("Peso (kg)", 30, 200, 85)
        ap_lo = st.number_input("Presión diastólica", 50, 150, 95)
        glucosa = st.selectbox(
        "Nivel de Glucosa",
        [1, 2, 3],
        format_func=lambda x: {
            1: "Normal",
            2: "Por encima de lo normal",
            3: "Muy alto"
        }[x]
    )
        alcohol = st.selectbox("Consume Alcohol", [0, 1], format_func=lambda x: "No" if x == 1 else "Sí")

    actividad = st.selectbox("Actividad física", [0, 1],format_func=lambda x: "No" if x == 1 else "Sí")

    predecir = st.button("🔍 Analizar Riesgo", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with right_col:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📊 Resultado clínico")

if predecir:
    imc = peso / ((altura / 100) ** 2)

    categorias = ["Bajo peso", "Normal", "Sobrepeso", "Obesidad"]

    imc_categoria = 1 if imc < 18.5 else 2 if imc < 25 else 3 if imc < 30 else 4
    texto_imc = categorias[imc_categoria - 1]

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
        "imc": [imc],
        "imc_categoria": [imc_categoria]
    })

    datos_scaled = scaler.transform(datos)
    prob = modelo.predict_proba(datos_scaled)[0][1]
    riesgo = prob * 100
       
    datos_scaled = scaler.transform(datos)
    prob = modelo.predict_proba(datos_scaled)[0][1]
    riesgo = prob * 100

    if riesgo >= 70:
        color = "#dc2626"
        estado = "🔴 ALTO RIESGO"
    elif riesgo >= 40:
        color = "#eab308"
        estado = "🟡 RIESGO MODERADO"
    else:
        color = "#16a34a"
        estado = "🟢 BAJO RIESGO"

    st.markdown(
        f"<div class='result-card' style='background:{color};'>{estado}</div>",
        unsafe_allow_html=True
    )

    m1, m2 = st.columns(2)
    with m1:
        st.metric("Probabilidad", f"{riesgo:.1f}%")
    with m2:
        st.metric("IMC", f"{imc:.1f}")
        st.write(f"**Clasificación IMC:** {texto_imc}")
            
    st.progress(int(riesgo))

    st.markdown("### 🩺 Recomendaciones")
if riesgo >= 70:
        st.error("Requiere evaluación médica prioritaria.")
elif riesgo >= 40:
    st.warning("Se recomienda seguimiento preventivo.")
else:
    st.success("Mantener hábitos saludables.")
else:
    st.info("Complete el formulario para visualizar el análisis.")
    
    st.markdown("</div>", unsafe_allow_html=True)

