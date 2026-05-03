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
    margin-bottom: 1.5rem;
}
.card {
    background: white;
    border-radius: 20px;
    padding: 1.5rem;
    box-shadow: 0 4px 15px rgba(0,0,0,0.06);
}
.result-card {
    border-radius: 20px;
    padding: 1.5rem;
    text-align: center;
    color: white;
    font-weight: bold;
    font-size: 28px;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ---------------- ENCABEZADO ----------------
st.markdown("""
<div class='main-title'>
<h1>🫀 Sistema Predictivo de Enfermedades Crónicas</h1>
<p>Diagnóstico clínico asistido con IA</p>
</div>
""", unsafe_allow_html=True)

# ---------------- FUNCIONES ----------------
def clasificar_peso(genero, altura, peso):
    factor = 1.07 if genero == 1 else 1.0
    if peso < 60 * factor:
        return 1, "Peso normal"
    elif peso < 80 * factor:
        return 2, "Sobrepeso"
    elif peso < 100 * factor:
        return 3, "Obesidad I"
    elif peso < 120 * factor:
        return 4, "Obesidad II"
    else:
        return 5, "Obesidad III"

def interpretacion_clinica(data):
    factores = []
    if data["ap_hi"] > 140: factores.append("Hipertensión sistólica")
    if data["ap_lo"] > 90: factores.append("Hipertensión diastólica")
    if data["cholesterol"] == 3: factores.append("Colesterol muy alto")
    if data["gluc"] == 3: factores.append("Glucosa muy alta")
    if data["smoke"] == 1: factores.append("Tabaquismo")
    if data["alco"] == 1: factores.append("Alcohol")
    if data["active"] == 0: factores.append("Sedentarismo")
    if data["imc"] > 30: factores.append("Obesidad")
    return factores

# ---------------- LAYOUT ----------------
left, right = st.columns([1.1,1])

with left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📋 Datos del paciente")

    c1, c2 = st.columns(2)

    with c1:
        edad = st.number_input("Edad", 1, 100, 58)
        altura = st.number_input("Altura (cm)", 100, 250, 170)
        ap_hi = st.number_input("Presión sistólica", 80, 250, 150)
        colesterol = st.selectbox("Colesterol", [1,2,3])
        fuma = st.selectbox("Fuma", [0,1])

    with c2:
        genero = st.selectbox("Género", [1,2])
        peso = st.number_input("Peso", 30, 200, 85)
        ap_lo = st.number_input("Presión diastólica", 50, 150, 95)
        glucosa = st.selectbox("Glucosa", [1,2,3])
        alcohol = st.selectbox("Alcohol", [0,1])

    actividad = st.selectbox("Actividad física", [0,1])

    predecir = st.button("🔍 Analizar Riesgo", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📊 Resultado clínico")

    if predecir:

        # ----------- VARIABLES -----------
        imc = peso / ((altura / 100) ** 2)
        imc_cat, texto_imc = clasificar_peso(genero, altura, peso)

        presion_pulso = ap_hi - ap_lo
        ratio_presion = ap_hi / ap_lo if ap_lo != 0 else 0
        riesgo_metabolico = colesterol + glucosa
        estilo_vida = fuma + alcohol - actividad

        imc_x_edad = imc * edad
        presion_x_edad = ap_hi * edad
        peso_x_altura = peso / altura

        # ----------- DATAFRAME -----------
        datos = pd.DataFrame({
            'age':[edad],'gender':[genero],'height':[altura],'weight':[peso],
            'ap_hi':[ap_hi],'ap_lo':[ap_lo],'cholesterol':[colesterol],'gluc':[glucosa],
            'smoke':[fuma],'alco':[alcohol],'active':[actividad],
            'imc':[imc],'imc_categoria':[imc_cat],
            'presion_pulso':[presion_pulso],'ratio_presion':[ratio_presion],
            'riesgo_metabolico':[riesgo_metabolico],'estilo_vida':[estilo_vida],
            'imc_x_edad':[imc_x_edad],'presion_x_edad':[presion_x_edad],
            'peso_x_altura':[peso_x_altura]
        })

        datos = datos[scaler.feature_names_in_]

        # ----------- PREDICCIÓN -----------
        prob = modelo.predict_proba(scaler.transform(datos))[0][1]
        riesgo = prob * 100

        # ----------- RESULTADO VISUAL -----------
        if riesgo >= 70:
            color, estado = "#dc2626", "🔴 ALTO RIESGO"
        elif riesgo >= 40:
            color, estado = "#eab308", "🟡 MODERADO"
        else:
            color, estado = "#16a34a", "🟢 BAJO"

        st.markdown(f"<div class='result-card' style='background:{color}'>{estado}</div>", unsafe_allow_html=True)

        st.metric("Probabilidad", f"{riesgo:.1f}%")
        st.metric("IMC", f"{imc:.1f}")
        st.write(f"Clasificación: {texto_imc}")

        st.progress(int(riesgo))

        # ----------- FACTORES -----------
        st.markdown("### ⚠️ Factores de riesgo")
        factores = interpretacion_clinica({
            "ap_hi":ap_hi,"ap_lo":ap_lo,"cholesterol":colesterol,
            "gluc":glucosa,"smoke":fuma,"alco":alcohol,
            "active":actividad,"imc":imc
        })

        if factores:
            for f in factores:
                st.write(f"• {f}")
        else:
            st.success("Sin factores relevantes")

        # ----------- DIAGNÓSTICO -----------
        st.markdown("### 🧾 Diagnóstico")
        if riesgo >= 70:
            st.error("Alto riesgo cardiovascular")
        elif riesgo >= 40:
            st.warning("Riesgo moderado")
        else:
            st.success("Riesgo bajo")

        # ----------- ALERTAS -----------
        st.markdown("### 🚨 Alertas")
        if ap_hi > 180 or ap_lo > 120:
            st.error("Crisis hipertensiva")

        # ----------- PLAN -----------
        st.markdown("### 🩺 Plan")
        if riesgo >= 70:
            st.write("• Evaluación inmediata")
        elif riesgo >= 40:
            st.write("• Seguimiento preventivo")
        else:
            st.write("• Control anual")

        st.caption("⚠️ Este sistema no reemplaza un diagnóstico médico profesional.")

    st.markdown("</div>", unsafe_allow_html=True)
