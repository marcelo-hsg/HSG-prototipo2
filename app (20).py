import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Hospital San Gabriel — Sistema de Confirmacion",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Forzar tema claro
st.markdown("""
    <style>
        html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
            background-color: #f5f7fa !important;
            color: #1a3a6b !important;
        }
        [data-testid="stHeader"] { background-color: #f5f7fa !important; }
        .stSelectbox label, .stTextInput label, .stRadio label { color: #1a3a6b !important; }
        .stDataFrame { background-color: white !important; }
        p, span, div, label, h1, h2, h3 { color: #1a3a6b; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .stApp { background-color: #f5f7fa !important; }
    .main .block-container {
        padding-top: 0px !important;
        padding-left: 0px !important;
        padding-right: 0px !important;
        max-width: 100% !important;
        background-color: #f5f7fa !important;
    }

    .hsg-header {
        background: white;
        padding: 18px 48px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid #dde3ec;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .hsg-logo-wrap { display:flex; align-items:center; gap:20px; }
    .hsg-logo-text span.top { display:block; font-size:12px; font-weight:500; color:#5f7a9e; letter-spacing:2px; text-transform:uppercase; }
    .hsg-logo-text span.bottom { display:block; font-size:36px; font-weight:900; color:#1a3a6b; letter-spacing:-1px; line-height:1; }
    .hsg-header-right { text-align:right; font-size:12px; color:#666; }
    .hsg-header-right b { color:#1a3a6b; font-size:13px; }

    .hero-section { background: linear-gradient(135deg, #1a3a6b 0%, #1565c0 60%, #1a73e8 100%); padding: 60px 48px 50px; color: white !important; }
    .hero-title { font-size:38px; font-weight:800; margin-bottom:10px; letter-spacing:-0.5px; color:white !important; }
    .hero-sub { font-size:16px; opacity:0.85; max-width:600px; line-height:1.6; margin-bottom:32px; color:white !important; }
    .hero-stats { display:flex; gap:32px; flex-wrap:wrap; }
    .hero-stat { text-align:center; }
    .hero-stat-num { font-size:36px; font-weight:800; line-height:1; color:white !important; }
    .hero-stat-label { font-size:12px; opacity:0.75; text-transform:uppercase; letter-spacing:1px; margin-top:4px; color:white !important; }
    .hero-divider { width:1px; background:rgba(255,255,255,0.25); height:50px; align-self:center; }

    .info-section { padding:40px 48px; background:#f5f7fa; }
    .info-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:20px; margin-bottom:32px; }
    .info-card { background:white; border-radius:12px; padding:28px 24px; box-shadow:0 1px 6px rgba(0,0,0,0.06); border-top:4px solid #1a73e8; }
    .info-card.verde { border-top-color:#34a853; }
    .info-card.naranja { border-top-color:#f9ab00; }
    .info-card.rojo { border-top-color:#ea4335; }
    .info-card.morado { border-top-color:#7c4dff; }
    .info-card.celeste { border-top-color:#00acc1; }
    .info-card-title { font-size:13px; font-weight:700; color:#1a3a6b; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:12px; }
    .info-card-body { font-size:13.5px; color:#444; line-height:1.7; }

    .esp-grid { display:grid; grid-template-columns:repeat(5,1fr); gap:12px; margin-top:8px; }
    .esp-item { background:white; border-radius:8px; padding:14px 12px; text-align:center; font-size:12px; color:#1a3a6b; font-weight:600; box-shadow:0 1px 4px rgba(0,0,0,0.06); border:1px solid #e8eaed; }
    .esp-dot { width:10px; height:10px; background:#1a73e8; border-radius:50%; margin:0 auto 8px; }

    .hsg-section-title { font-size:22px; font-weight:700; color:#1a3a6b; margin-bottom:4px; }
    .hsg-section-sub { font-size:13px; color:#666; margin-bottom:22px; }

    .badge-confirmada { background:#e6f4ea; color:#137333; padding:4px 14px; border-radius:20px; font-size:12px; font-weight:700; }
    .badge-pendiente  { background:#fef7e0; color:#b06000; padding:4px 14px; border-radius:20px; font-size:12px; font-weight:700; }
    .badge-cancelada  { background:#fce8e6; color:#c5221f; padding:4px 14px; border-radius:20px; font-size:12px; font-weight:700; }
    .badge-ausente    { background:#f1f3f4; color:#444;    padding:4px 14px; border-radius:20px; font-size:12px; font-weight:700; }

    .urg-alta  { background:#fce8e6; color:#c5221f; padding:3px 12px; border-radius:20px; font-size:12px; font-weight:700; border:1px solid #f5c6c6; }
    .urg-media { background:#fef7e0; color:#b06000; padding:3px 12px; border-radius:20px; font-size:12px; font-weight:700; border:1px solid #fde9a2; }
    .urg-baja  { background:#e6f4ea; color:#137333; padding:3px 12px; border-radius:20px; font-size:12px; font-weight:700; border:1px solid #b7dfbf; }

    .cita-card { background:white; border-radius:10px; border-left:5px solid #1a73e8; padding:18px 22px; margin-bottom:12px; box-shadow:0 1px 4px rgba(0,0,0,0.07); }
    .cita-card.confirmada { border-left-color:#34a853; }
    .cita-card.pendiente  { border-left-color:#f9ab00; }
    .cita-card.cancelada  { border-left-color:#ea4335; }
    .cita-card.ausente    { border-left-color:#9aa0a6; }
    .cita-card-header { display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; }
    .cita-nombre { font-size:15px; font-weight:700; color:#1a3a6b; }
    .cita-badges { display:flex; gap:8px; align-items:center; }
    .cita-info { font-size:13px; color:#555; margin-bottom:2px; }

    /* AGENDA MEDICO */
    .medico-card { background:white; border-radius:10px; padding:16px 20px; margin-bottom:10px; box-shadow:0 1px 4px rgba(0,0,0,0.07); border-left:4px solid #1a73e8; }
    .medico-nombre { font-size:14px; font-weight:700; color:#1a3a6b; margin-bottom:8px; }
    .slot-grid { display:flex; flex-wrap:wrap; gap:6px; }
    .slot-libre { background:#e6f4ea; color:#137333; padding:4px 10px; border-radius:6px; font-size:12px; font-weight:600; cursor:pointer; }
    .slot-ocupado { background:#fce8e6; color:#c5221f; padding:4px 10px; border-radius:6px; font-size:12px; font-weight:600; text-decoration:line-through; }

    hr { border-color:#e8eaed; margin:16px 0; }
    .hero-section * { color: white !important; }
    .hero-section .hero-title { color: white !important; }
    .hero-section .hero-sub { color: white !important; }
    .hero-section .hero-stat-num { color: white !important; }
    .hero-section .hero-stat-label { color: white !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MEDICOS POR ESPECIALIDAD
# ─────────────────────────────────────────────
MEDICOS = {
    "Cardiologia": ["Dr. Roberto Fuentes", "Dra. Carmen Ortega"],
    "Traumatologia": ["Dr. Felipe Rojas", "Dr. Andres Vega"],
    "Neurologia": ["Dra. Patricia Medina", "Dr. Carlos Silva"],
    "Ginecologia": ["Dra. Valentina Torres", "Dra. Isabel Reyes"],
    "Oftalmologia": ["Dr. Diego Morales", "Dra. Elena Castro"],
    "Urologia": ["Dr. Marcelo Diaz", "Dr. Hector Espinoza"],
    "Dermatologia": ["Dra. Sofia Alvarez", "Dr. Gabriel Munoz"],
    "Endocrinologia": ["Dra. Claudia Vargas", "Dr. Nicolas Herrera"],
    "Gastroenterologia": ["Dr. Rodrigo Lopez", "Dra. Francisca Jimenez"],
    "Reumatologia": ["Dra. Ana Gonzalez", "Dr. Sebastian Cortez"],
}

DIAS_SEMANA = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
DATA_VERSION = "v7_fix_espera"  # Cambiar esto fuerza regeneracion
HORARIOS = ["08:30", "09:00", "09:30", "10:00", "10:30", "11:00",
            "11:30", "14:00", "14:30", "15:00", "15:30", "16:00"]

MESES_ES = {
    1:"enero", 2:"febrero", 3:"marzo", 4:"abril",
    5:"mayo", 6:"junio", 7:"julio", 8:"agosto",
    9:"septiembre", 10:"octubre", 11:"noviembre", 12:"diciembre"
}
DIAS_ES = {
    0:"lunes", 1:"martes", 2:"miercoles", 3:"jueves",
    4:"viernes", 5:"sabado", 6:"domingo"
}

def fecha_es(fecha_dt):
    """Convierte datetime a fecha en español."""
    return f"{fecha_dt.day} de {MESES_ES[fecha_dt.month]} de {fecha_dt.year}"

def sync_agenda():
    """Reconstruye la agenda completa desde el estado actual de las citas."""
    if "agenda" not in st.session_state:
        return
    # Limpiar y reconstruir
    hoy_s = datetime.today().replace(hour=0,minute=0,second=0,microsecond=0)
    todas_fechas = [(hoy_s + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(90)]
    # Reiniciar todas las fechas futuras a None
    for medico in st.session_state.agenda:
        for fecha in todas_fechas:
            if fecha not in st.session_state.agenda[medico]:
                st.session_state.agenda[medico][fecha] = {h: None for h in HORARIOS}
            else:
                for hora in HORARIOS:
                    st.session_state.agenda[medico][fecha][hora] = None
    # Recargar desde citas actuales (solo Confirmada y Pendiente)
    for _, row in st.session_state.citas[
        st.session_state.citas["estado"].isin(["Confirmada","Pendiente"])
    ].iterrows():
        medico = row.get("medico","")
        fecha  = row.get("fecha","")
        hora   = row.get("hora","")
        if medico in st.session_state.agenda:
            if fecha not in st.session_state.agenda[medico]:
                st.session_state.agenda[medico][fecha] = {h: None for h in HORARIOS}
            if hora in HORARIOS:
                st.session_state.agenda[medico][fecha][hora] = row["nombre_paciente"]

def get_semana_actual():
    hoy = datetime.today()
    lunes = hoy - timedelta(days=hoy.weekday())
    return [(lunes + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(5)]

def generar_datos():
    random.seed(7)
    np.random.seed(7)
    nombres = ["Ana","Maria","Juan","Carlos","Luis","Rosa","Pedro","Elena","Jorge","Carmen",
               "Felipe","Isabel","Diego","Claudia","Rodrigo","Patricia","Andres","Veronica",
               "Tomas","Francisca","Gabriel","Valentina","Ignacio","Sofia","Sebastian","Daniela",
               "Matias","Camila","Nicolas","Alejandra","Cristobal","Javiera","Mauricio","Lorena",
               "Roberto","Cecilia","Marcelo","Pilar","Hector","Beatriz"]
    apellidos = ["Gonzalez","Munoz","Rodriguez","Lopez","Martinez","Perez","Sanchez","Ramirez",
                 "Torres","Flores","Rivera","Morales","Jimenez","Ortega","Herrera","Medina",
                 "Castro","Rojas","Vargas","Alvarez","Reyes","Diaz","Vega","Contreras","Ramos",
                 "Espinoza","Fuentes","Cortes","Miranda","Silva"]
    especialidades = list(MEDICOS.keys())
    comunas = ["Concepcion","Talcahuano","San Pedro","Chiguayante","Penco","Tome","Coronel",
               "Lota","Lebu","Los Angeles","Chillan","Arauco","Canete","Tirua","Curanilahue"]
    causas_ausencia = ["No sabia que tenia hora","Olvido la cita","Problemas de transporte",
                       "Trabajaba y no pudo ausentarse","Enfermedad intercurrente",
                       "Contacto invalido","Error de agenda"]
    pacientes = []
    for i in range(1, 2001):
        pacientes.append({
            "id_paciente": f"P{i:04d}",
            "nombre": f"{random.choice(nombres)} {random.choice(apellidos)} {random.choice(apellidos)}",
            "edad": random.randint(18, 85),
            "rut": f"{random.randint(5000000,25000000)}-{random.randint(0,9)}",
            "telefono": f"+569{random.randint(10000000,99999999)}",
            "comuna": random.choice(comunas),
            "contacto_valido": random.random() > 0.15
        })
    df_pac = pd.DataFrame(pacientes)
    hoy = datetime.today().replace(hour=0,minute=0,second=0,microsecond=0)
    citas = []
    for j in range(1,2001):
        pac = df_pac.sample(1).iloc[0]
        estado = random.choices(["Pendiente","Confirmada","Cancelada","Ausente"],weights=[45,30,15,10])[0]
        urgencia = random.choices(["Alta","Media","Baja"],weights=[20,45,35])[0]
        esp = random.choice(especialidades)
        medico = random.choice(MEDICOS[esp])
        PATOLOGIAS_GES = [
            ("Cancer de mama", 30),
            ("Diabetes Mellitus tipo 2", 180),
            ("Hipertension arterial", 180),
            ("Depresion", 90),
            ("Artrosis de cadera o rodilla", 180),
            ("Cancer colorrectal", 30),
            ("Cataratas", 90),
            ("Epilepsia", 180),
            ("Insuficiencia renal cronica", 180),
            ("VIH/SIDA", 15),
        ]
        es_ges = random.random() < 0.20
        if es_ges:
            pat_ges, plazo_ges = random.choice(PATOLOGIAS_GES)
            fecha_diag = hoy - timedelta(days=random.randint(1, plazo_ges+30))
            fecha_op   = fecha_diag + timedelta(days=plazo_ges)
            pat_ges_val = pat_ges
            fecha_diag_val = fecha_diag.strftime("%Y-%m-%d")
            fecha_op_val   = fecha_op.strftime("%Y-%m-%d")
        else:
            pat_ges_val    = ""
            fecha_diag_val = ""
            fecha_op_val   = ""

        citas.append({
            "id_cita": f"C{j:04d}",
            "nombre_paciente": pac["nombre"],
            "edad": pac["edad"],
            "rut": pac["rut"],
            "telefono": pac["telefono"],
            "comuna": pac["comuna"],
            "especialidad": esp,
            "medico": medico,
            "fecha": (hoy+timedelta(days=random.randint(0,89))).strftime("%Y-%m-%d"),
            "hora": random.choice(HORARIOS),
            "estado": estado,
            "urgencia": urgencia if urgencia in ["Alta","Media","Baja"] else "Media",
            "causa_ausencia": random.choice(causas_ausencia) if estado=="Ausente" else "",
            "contacto_valido": pac["contacto_valido"],
            "es_ges": es_ges,
            "patologia_ges": pat_ges_val,
            "fecha_diagnostico_ges": fecha_diag_val,
            "fecha_oportunidad_ges": fecha_op_val,
        })
    df_citas = pd.DataFrame(citas)
    espera = []
    for k in range(1,501):
        pac = df_pac.sample(1).iloc[0]
        esp = random.choice(especialidades)
        espera.append({
            "id_espera": f"E{k:04d}",
            "nombre": pac["nombre"],
            "rut": pac["rut"],
            "telefono": pac["telefono"],
            "comuna": pac["comuna"],
            "especialidad": esp,
            "fecha_ingreso_espera": (hoy-timedelta(days=random.randint(1,180))).strftime("%Y-%m-%d"),
            "prioridad": random.choices(["Alta","Media","Baja"],weights=[25,45,30])[0],
            "estado_espera": random.choices(["Esperando","Asignado"],weights=[80,20])[0]
        })
        df_citas["urgencia"] = df_citas["urgencia"].replace({"Media":"Media","Media":"Media"})
    return df_pac, df_citas, pd.DataFrame(espera)

# Forzar regeneracion si los datos son insuficientes o no tienen columnas nuevas
# Regenerar si version no coincide o datos insuficientes
# Siempre verificar prioridades correctas
espera_actual = st.session_state.get("espera", pd.DataFrame())
if (st.session_state.get("data_version") != DATA_VERSION or
    espera_actual.empty or
    "prioridad" not in espera_actual.columns or
    set(espera_actual["prioridad"].unique()) == {"Alta"} or
    len(espera_actual) < 400):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    _, df_c, df_e = generar_datos()
    df_c['urgencia'] = df_c['urgencia'].replace({'Media': 'Media', 'Media': 'Media'})
    st.session_state.citas = df_c.copy()
    st.session_state.citas["urgencia"] = st.session_state.citas["urgencia"].apply(
        lambda x: x if x in ["Alta","Media","Baja"] else "Media"
    )
    # Calcular score de riesgo de inasistencia
    COMUNAS_LEJANAS = ["Tirua","Lebu","Canete","Arauco","Curanilahue","Lota","Los Angeles","Chillan"]
    def calcular_riesgo(row):
        score = 0
        if row.get("comuna","") in COMUNAS_LEJANAS: score += 3
        if not row.get("contacto_valido", True): score += 3
        if row.get("urgencia","") == "Baja": score += 2
        if row.get("estado","") == "Pendiente": score += 1
        if row.get("edad", 0) >= 65: score += 1
        if score >= 6: return "Alto"
        elif score >= 3: return "Medio"
        else: return "Bajo"
    st.session_state.citas["riesgo_inasistencia"] = st.session_state.citas.apply(calcular_riesgo, axis=1)
    st.session_state.citas["urgencia"] = st.session_state.citas["urgencia"].map(
        lambda x: "Media" if x not in ["Alta","Media","Baja"] else x
    )
    st.session_state.espera = df_e.copy()
    st.session_state.data_version = DATA_VERSION

    # Agenda cubre los proximos 30 dias
    hoy_ag = datetime.today().replace(hour=0,minute=0,second=0,microsecond=0)
    todas_fechas = [(hoy_ag+timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30)]

    st.session_state.agenda = {}
    for esp, medicos in MEDICOS.items():
        for medico in medicos:
            st.session_state.agenda[medico] = {}
            for fecha in todas_fechas:
                st.session_state.agenda[medico][fecha] = {h: None for h in HORARIOS}

    # Cargar TODAS las citas confirmadas en la agenda
    for _, row in st.session_state.citas[st.session_state.citas["estado"]=="Confirmada"].iterrows():
        medico = row.get("medico","")
        fecha  = row.get("fecha","")
        hora   = row.get("hora","")
        if medico in st.session_state.agenda:
            if fecha not in st.session_state.agenda[medico]:
                st.session_state.agenda[medico][fecha] = {h: None for h in HORARIOS}
            if hora in st.session_state.agenda[medico][fecha]:
                st.session_state.agenda[medico][fecha][hora] = row["nombre_paciente"]

if "modulo" not in st.session_state:
    st.session_state.modulo = "inicio"

df_citas  = st.session_state.citas
df_espera = st.session_state.espera

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="hsg-header">
  <div class="hsg-logo-wrap">
    <svg width="58" height="58" viewBox="0 0 58 58" xmlns="http://www.w3.org/2000/svg">
      <rect width="58" height="58" rx="12" fill="#1a3a6b"/>
      <rect x="25" y="10" width="8" height="38" rx="3" fill="white"/>
      <rect x="10" y="25" width="38" height="8" rx="3" fill="white"/>
      <circle cx="29" cy="29" r="25" fill="none" stroke="#1a73e8" stroke-width="2.5"/>
    </svg>
    <div class="hsg-logo-text">
      <span class="top">Red Asistencial Sur &nbsp;·&nbsp; Servicio de Salud Biobio</span>
      <span class="bottom">Hospital San Gabriel</span>
    </div>
  </div>
  <div class="hsg-header-right">
    <b>Sistema de Gestion de Consultas</b><br>
    {datetime.today().strftime('%d/%m/%Y')} &nbsp;|&nbsp; Usuario: Admin OIRS
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# NAVEGACION
# ─────────────────────────────────────────────
modulos_nav = [
    ("inicio","Inicio"),("dashboard","Panel de Control"),
    ("confirmacion","Confirmación de Citas"),
    ("espera","Lista de Espera"),("reportes","Reportes de Ausentismo"),
    ("agenda_semana","Agenda de Confirmaciones"),
    ("ges","Pacientes GES"),
]
cols_nav = st.columns(len(modulos_nav))
for i,(key,label) in enumerate(modulos_nav):
    with cols_nav[i]:
        if st.button(label, key=f"nav_{key}", use_container_width=True,
                     type="primary" if st.session_state.modulo==key else "secondary"):
            st.session_state.modulo = key
            st.rerun()

st.markdown("<hr style='margin:0;border-color:#dde3ec;'>", unsafe_allow_html=True)
modulo = st.session_state.modulo

# ─────────────────────────────────────────────
# INICIO
# ─────────────────────────────────────────────
if modulo == "inicio":
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">Bienvenido al Hospital San Gabriel</div>
        <div class="hero-sub">Hospital publico de alta complejidad al servicio de la comunidad del sur de Chile. Comprometidos con la salud, el acceso equitativo y la calidad de atencion de mas de 420.000 personas de la region del Biobio.</div>
        <div class="hero-stats">
            <div class="hero-stat"><div class="hero-stat-num">320</div><div class="hero-stat-label">Camas disponibles</div></div>
            <div class="hero-divider"></div>
            <div class="hero-stat"><div class="hero-stat-num">6</div><div class="hero-stat-label">Pabellones quirurgicos</div></div>
            <div class="hero-divider"></div>
            <div class="hero-stat"><div class="hero-stat-num">1.800+</div><div class="hero-stat-label">Funcionarios</div></div>
            <div class="hero-divider"></div>
            <div class="hero-stat"><div class="hero-stat-num">420.000</div><div class="hero-stat-label">Personas atendidas</div></div>
            <div class="hero-divider"></div>
            <div class="hero-stat"><div class="hero-stat-num">10</div><div class="hero-stat-label">Especialidades medicas</div></div>
        </div>
    </div>
    <div class="info-section">
        <div class="info-grid">
            <div class="info-card"><div class="info-card-title">Nuestra Mision</div><div class="info-card-body">Proveer atencion medica integral, oportuna y de calidad a la poblacion del sur de Chile, con enfasis en la equidad, el respeto a la dignidad del paciente y la mejora continua de los procesos clinicos y administrativos.</div></div>
            <div class="info-card verde"><div class="info-card-title">Nuestra Vision</div><div class="info-card-body">Ser el hospital publico de referencia del sur de Chile, reconocido por la excelencia clinica, la innovacion en gestion hospitalaria y el compromiso con el bienestar de las comunidades que atendemos.</div></div>
            <div class="info-card naranja"><div class="info-card-title">Nuestros Valores</div><div class="info-card-body"><ul style="padding-left:16px;margin:0;"><li>Compromiso con el paciente</li><li>Transparencia y probidad</li><li>Trabajo colaborativo</li><li>Mejora continua</li><li>Respeto e inclusion</li></ul></div></div>
            <div class="info-card rojo"><div class="info-card-title">Urgencias 24/7</div><div class="info-card-body">Nuestro servicio de urgencias opera las 24 horas del dia, los 7 dias de la semana, con equipos clinicos especializados en atencion de emergencias y trauma. Contamos con 2 pabellones de urgencia permanentes.</div></div>
            <div class="info-card morado"><div class="info-card-title">Red Asistencial</div><div class="info-card-body">Recibimos derivaciones desde mas de 15 CESFAM y hospitales comunitarios de la red asistencial del Biobio, coordinando la atencion de pacientes desde comunas como Tirua, Canete y Lebu.</div></div>
            <div class="info-card celeste"><div class="info-card-title">Acreditacion</div><div class="info-card-body">Hospital acreditado por la Superintendencia de Salud bajo los estandares de calidad del Ministerio de Salud de Chile. En proceso de certificacion ISO 9001 en procesos de gestion clinica y administrativa.</div></div>
        </div>
        <div style="background:white;border-radius:12px;padding:28px 24px;box-shadow:0 1px 6px rgba(0,0,0,0.06);margin-bottom:20px;">
            <div class="info-card-title" style="margin-bottom:16px;">Especialidades Medicas Disponibles</div>
            <div class="esp-grid">
                <div class="esp-item"><div class="esp-dot"></div>Cardiologia</div>
                <div class="esp-item"><div class="esp-dot" style="background:#34a853"></div>Traumatologia</div>
                <div class="esp-item"><div class="esp-dot" style="background:#ea4335"></div>Neurologia</div>
                <div class="esp-item"><div class="esp-dot" style="background:#f9ab00"></div>Ginecologia</div>
                <div class="esp-item"><div class="esp-dot" style="background:#7c4dff"></div>Oftalmologia</div>
                <div class="esp-item"><div class="esp-dot" style="background:#00acc1"></div>Urologia</div>
                <div class="esp-item"><div class="esp-dot" style="background:#e91e63"></div>Dermatologia</div>
                <div class="esp-item"><div class="esp-dot" style="background:#ff7043"></div>Endocrinologia</div>
                <div class="esp-item"><div class="esp-dot" style="background:#43a047"></div>Gastroenterologia</div>
                <div class="esp-item"><div class="esp-dot" style="background:#1a3a6b"></div>Reumatologia</div>
            </div>
        </div>
        <div style="background:#1a3a6b;border-radius:12px;padding:24px 28px;color:white;display:flex;justify-content:space-between;align-items:center;">
            <div>
                <div style="font-size:15px;font-weight:700;margin-bottom:4px;color:white !important;">Horario de Atencion</div>
                <div style="font-size:13px;opacity:0.8;">Consultas de especialidad: Lunes a Viernes, 08:00 - 17:00 hrs &nbsp;|&nbsp; Urgencias: 24 horas &nbsp;|&nbsp; Cirugias electivas: Lunes a Viernes, 07:30 - 16:00 hrs</div>
            </div>
            <div style="text-align:right;font-size:13px;opacity:0.8;">
                <div style="font-weight:700;font-size:15px;margin-bottom:4px;">Contacto OIRS</div>
                <div>+56 41 234 5678</div>
                <div>oirs@hospitalsangabriel.cl</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PANEL DE CONTROL
# ─────────────────────────────────────────────
elif modulo == "dashboard":
    st.markdown("<div style='padding:24px 8px;'>", unsafe_allow_html=True)
    st.markdown("<div class='hsg-section-title'>Panel de Control</div>", unsafe_allow_html=True)
    st.markdown("<div class='hsg-section-sub'>Resumen de actividad — proximos 30 dias</div>", unsafe_allow_html=True)

    hoy_str = datetime.today().strftime("%Y-%m-%d")
    prox30  = (datetime.today()+timedelta(days=30)).strftime("%Y-%m-%d")
    semana  = df_citas[(df_citas["fecha"]>=hoy_str)&(df_citas["fecha"]<=prox30)]
    total = len(semana)
    conf  = len(semana[semana["estado"]=="Confirmada"])
    pend  = len(semana[semana["estado"]=="Pendiente"])
    ausen = len(semana[semana["estado"]=="Ausente"])
    canc  = len(semana[semana["estado"]=="Cancelada"])

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total citas periodo", total)
    c2.metric("Confirmadas", conf, f"{round(conf/total*100) if total else 0}%")
    c3.metric("Pendientes de confirmar", pend, delta_color="inverse", delta=f"-{pend}")
    c4.metric("Ausencias registradas", ausen)

    # Indicador de impacto del sistema
    st.divider()
    st.markdown("**Impacto del sistema de confirmacion automatica**")
    ci1, ci2, ci3, ci4 = st.columns(4)
    total_enviados = len(st.session_state.get("envios_realizados",{}))
    confirmados_auto = len([r for r in st.session_state.get("respuestas_pacientes",{}).values() if r=="Confirmo"])
    cancelados_auto  = len([r for r in st.session_state.get("respuestas_pacientes",{}).values() if r=="Cancelo"])
    tasa_respuesta   = round(confirmados_auto/(total_enviados) * 100) if total_enviados > 0 else 0
    ci1.metric("Mensajes enviados", total_enviados)
    ci2.metric("Confirmaciones via mensaje", confirmados_auto)
    ci3.metric("Cupos liberados via mensaje", cancelados_auto)
    ci4.metric("Tasa de respuesta", f"{tasa_respuesta}%")
    st.divider()

    col_a,col_b = st.columns(2)
    with col_a:
        st.markdown("**Citas por especialidad**")
        esp = semana.groupby("especialidad").size().reset_index(name="Total")
        esp = esp.sort_values("Total",ascending=True)
        colores_esp=["#1a3a6b","#1565c0","#1a73e8","#2196f3","#42a5f5","#64b5f6","#90caf9","#34a853","#00acc1","#7c4dff"]
        fig=px.bar(esp,x="Total",y="especialidad",orientation="h",color="especialidad",
                   color_discrete_sequence=colores_esp,text="Total")
        fig.update_traces(textposition="outside",textfont_size=12)
        fig.update_layout(margin=dict(l=0,r=40,t=10,b=0),height=340,xaxis_title="",yaxis_title="",
                          plot_bgcolor="white",paper_bgcolor="white",showlegend=False,
                          xaxis=dict(showgrid=True,gridcolor="#f0f0f0"),
                          yaxis=dict(tickfont=dict(size=13,color="#1a3a6b")))
        st.plotly_chart(fig,use_container_width=True)
    with col_b:
        st.markdown("**Distribucion de estados**")
        ec=semana["estado"].value_counts().reset_index(); ec.columns=["estado","cantidad"]
        cm={"Confirmada":"#34a853","Pendiente":"#f9ab00","Cancelada":"#ea4335","Ausente":"#9aa0a6"}
        fig2=px.pie(ec,names="estado",values="cantidad",color="estado",color_discrete_map=cm,hole=0.45)
        fig2.update_traces(textposition="inside",textinfo="percent+label",textfont_size=13)
        fig2.update_layout(margin=dict(l=0,r=0,t=10,b=0),height=340,paper_bgcolor="white",
                           legend=dict(orientation="h",y=-0.1))
        st.plotly_chart(fig2,use_container_width=True)

    st.markdown("**Citas pendientes de confirmar — proximos 30 dias**")
    pdf=semana[semana["estado"]=="Pendiente"][["id_cita","nombre_paciente","rut","especialidad","urgencia","fecha","hora","telefono","comuna"]].copy()
    pdf.columns=["ID","Paciente","RUT","Especialidad","Urgencia","Fecha","Hora","Telefono","Comuna"]
    st.dataframe(pdf,use_container_width=True,hide_index=True)

# ─────────────────────────────────────────────
# CONFIRMACION DE CITAS
# ─────────────────────────────────────────────
elif modulo == "confirmacion":
    st.markdown("<div style='padding:24px 8px;'>", unsafe_allow_html=True)
    st.markdown("<div class='hsg-section-title'>Confirmación de Citas</div>", unsafe_allow_html=True)
    st.markdown("<div class='hsg-section-sub'>Busca una cita para confirmar, cancelar o registrar ausencia</div>", unsafe_allow_html=True)

    col_f1,col_f2=st.columns([2,2])
    with col_f1: busqueda=st.text_input("Buscar por nombre, RUT o ID",placeholder="Ej: Gonzalez / 12345678-9 / C0023")
    with col_f2: filtro_esp=st.selectbox("Especialidad",["Todas"]+sorted(df_citas["especialidad"].unique().tolist()), key="conf_esp")
    
    col_f3,col_f4,col_f5=st.columns([1,1,2])
    with col_f3: filtro_estado=st.selectbox("Estado",["Todos","Pendiente","Confirmada","Cancelada","Ausente"], key="conf_estado")
    with col_f4: filtro_riesgo=st.selectbox("Riesgo inasistencia",["Todos","Alto","Medio","Bajo"], key="conf_riesgo")
    with col_f5:
        hoy_conf = datetime.today().date()
        fecha_max = hoy_conf + timedelta(days=90)
        fechas_disponibles = sorted(df_citas["fecha"].unique().tolist())
        filtro_fecha = st.selectbox("Filtrar por fecha", 
            ["Todas las fechas"] + fechas_disponibles, key="conf_fecha")

    mask=pd.Series([True]*len(df_citas),index=df_citas.index)
    if busqueda:
        b=busqueda.lower()
        mask=(df_citas["nombre_paciente"].str.lower().str.contains(b)|
              df_citas["rut"].str.lower().str.contains(b)|
              df_citas["id_cita"].str.lower().str.contains(b))
    if filtro_esp!="Todas": mask=mask&(df_citas["especialidad"]==filtro_esp)
    if filtro_estado!="Todos": mask=mask&(df_citas["estado"]==filtro_estado)
    if filtro_riesgo!="Todos": mask=mask&(df_citas["riesgo_inasistencia"]==filtro_riesgo)
    if filtro_fecha!="Todas las fechas": mask=mask&(df_citas["fecha"]==filtro_fecha)

    resultados = df_citas[mask].reset_index(drop=True).head(30)
    
    # Resumen contextual
    total_res    = len(df_citas[mask])
    riesgo_alto  = len(df_citas[mask & (df_citas["riesgo_inasistencia"]=="Alto")]) if "riesgo_inasistencia" in df_citas.columns else 0
    sin_contacto = len(df_citas[mask & (df_citas["contacto_valido"]==False)])
    ges_res      = len(df_citas[mask & (df_citas["es_ges"]==True)]) if "es_ges" in df_citas.columns else 0
    
    resumen_parts = [f"**{total_res}** resultado(s) encontrados"]
    if riesgo_alto > 0:
        resumen_parts.append(f"🔴 **{riesgo_alto}** riesgo alto")
    if sin_contacto > 0:
        resumen_parts.append(f"⚠️ **{sin_contacto}** contacto inválido")
    if ges_res > 0:
        resumen_parts.append(f"🏥 **{ges_res}** GES")
    
    st.markdown(" · ".join(resumen_parts))

    for _,row in resultados.iterrows():
        estado=row["estado"]; urgencia=row["urgencia"]
        clase=estado.lower(); urg_clase=urgencia.lower()
        contacto_color="#137333" if row["contacto_valido"] else "#c5221f"
        contacto_txt="Valido" if row["contacto_valido"] else "Invalido — actualizar"
        riesgo = row.get("riesgo_inasistencia","Bajo")
        # GES info
        ges_html = ""
        if row.get("es_ges") and row.get("patologia_ges"):
            f_op = row.get("fecha_oportunidad_ges","")
            if f_op:
                hoy_s = datetime.today().strftime("%Y-%m-%d")
                dias_r = (datetime.strptime(f_op,"%Y-%m-%d")-datetime.today()).days
                if f_op < hoy_s:
                    col_ges="#7b0000"; txt_ges=f"VENCIDA hace {abs(dias_r)} dias"
                elif dias_r <= 15:
                    col_ges="#ea4335"; txt_ges=f"URGENTE {dias_r} dias restantes"
                else:
                    col_ges="#1a73e8"; txt_ges=f"Vigente {dias_r} dias restantes"
                ges_html = f'<div class="cita-info"><b style="color:{col_ges};">GES:</b> <span style="color:#1a73e8;font-weight:600;">{row["patologia_ges"]}</span> — <span style="color:{col_ges};font-weight:700;">{txt_ges}</span></div>'
        st.markdown(f"""
        <div class="cita-card {clase}">
            <div class="cita-card-header">
                <div class="cita-nombre">{row['nombre_paciente']}</div>
                <div class="cita-badges">
                    <span style="font-size:12px;color:#666;margin-right:4px;">Estado:</span>
                    <span class="badge-{clase}">{estado}</span>
                    &nbsp;&nbsp;
                    <span style="font-size:12px;color:#666;margin-right:4px;">Riesgo inasistencia:</span>
                    <span style="padding:3px 10px;border-radius:20px;font-size:12px;font-weight:700;
                        background:{'#fce8e6' if riesgo=='Alto' else '#fef7e0' if riesgo=='Medio' else '#e6f4ea'};
                        color:{'#c5221f' if riesgo=='Alto' else '#b06000' if riesgo=='Medio' else '#137333'};">
                        {riesgo}
                    </span>
                </div>
            </div>
            <div style="display:flex;gap:36px;flex-wrap:wrap;">
                <div class="cita-info"><b>Especialidad:</b> {row['especialidad']}</div>
                <div class="cita-info"><b>Medico:</b> {row.get('medico','—')}</div>
                <div class="cita-info"><b>Fecha:</b> {fecha_es(datetime.strptime(row['fecha'], '%Y-%m-%d'))} — {row['hora']} hrs</div>
                <div class="cita-info"><b>RUT:</b> {row['rut']}</div>
                <div class="cita-info"><b>Telefono:</b> {row['telefono']}</div>
                <div class="cita-info"><b>Comuna:</b> {row['comuna']}</div>
                <div class="cita-info"><b>Edad:</b> {row['edad']} años</div>
                <div class="cita-info"><b>Contacto:</b> <span style="color:{contacto_color};font-weight:600;">{contacto_txt}</span></div>
                <div class="cita-info"><b>ID:</b> {row['id_cita']}</div>
            </div>
            {ges_html}
        </div>
        """, unsafe_allow_html=True)
        # ── Disponibilidad del medico asignado
        medico_actual = row.get("medico","")
        esp_actual    = row["especialidad"]
        if medico_actual and medico_actual in st.session_state.agenda:
            # Semana de la cita
            fecha_cita = datetime.strptime(row["fecha"], "%Y-%m-%d")
            dia_semana = fecha_cita.weekday()
            # Si es fin de semana mostrar semana siguiente
            if dia_semana >= 5:
                lunes_cita = fecha_cita + timedelta(days=(7 - dia_semana))
            else:
                lunes_cita = fecha_cita - timedelta(days=dia_semana)
            fechas_semana_cita = [(lunes_cita + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(5)]
            dias_labels  = ["Lunes","Martes","Miercoles","Jueves","Viernes"]
            semana_label = f"{lunes_cita.strftime('%d/%m')} al {(lunes_cita+timedelta(days=4)).strftime('%d/%m/%Y')}"
            agenda_med   = st.session_state.agenda[medico_actual]

            # Sincronizar agenda antes de mostrar
            sync_agenda()
            agenda_med = st.session_state.agenda[medico_actual]

            # Asegurar que las fechas de la semana existan
            for fecha in fechas_semana_cita:
                if fecha not in agenda_med:
                    agenda_med[fecha] = {h: None for h in HORARIOS}

            with st.expander(f"Ver disponibilidad de {medico_actual} — semana del {semana_label}"):
                tabla_data = []
                for hora in HORARIOS:
                    fila = {"Hora": hora}
                    for i, fecha in enumerate(fechas_semana_cita):
                        ocupado = agenda_med.get(fecha, {}).get(hora, None)
                        fila[dias_labels[i]] = f"Ocupado: {str(ocupado)[:14]}..." if ocupado else "Disponible"
                    tabla_data.append(fila)

                df_ag = pd.DataFrame(tabla_data).set_index("Hora")

                def color_ag(val):
                    if "Ocupado" in str(val):
                        return "background-color:#fce8e6;color:#c5221f;font-weight:600;"
                    return "background-color:#e6f4ea;color:#137333;font-weight:600;"

                st.dataframe(df_ag.style.map(color_ag), use_container_width=True, height=380)

                # Reasignar hora
                st.markdown("**Reasignar hora para este paciente**")
                st.caption("Se muestran solo fechas con horas disponibles. Si no aparece la semana de la cita es porque el medico no tiene horas libres esa semana.")
                rc1, rc2, rc3 = st.columns(3)
                dias_libres = []
                for i, fecha in enumerate(fechas_semana_cita):
                    horas_libres = [h for h,p in agenda_med.get(fecha,{}).items() if p is None]
                    if horas_libres:
                        label = f"{dias_labels[i]} {datetime.strptime(fecha, '%Y-%m-%d').strftime('%d/%m')}"
                        dias_libres.append((label, fecha))

                if dias_libres:
                    dia_r   = rc1.selectbox("Dia", [d[0] for d in dias_libres], key=f"dia_r_{row['id_cita']}")
                    fecha_r = dict(dias_libres)[dia_r]
                    horas_r = [h for h,p in agenda_med.get(fecha_r,{}).items() if p is None]
                    hora_r  = rc2.selectbox("Hora disponible", horas_r, key=f"hora_r_{row['id_cita']}")
                    if rc3.button("Reasignar", key=f"reasig_{row['id_cita']}"):
                        hora_ant  = row["hora"]; fecha_ant = row["fecha"]
                        if fecha_ant in agenda_med and hora_ant in agenda_med.get(fecha_ant,{}):
                            st.session_state.agenda[medico_actual][fecha_ant][hora_ant] = None
                        if fecha_r not in st.session_state.agenda[medico_actual]:
                            st.session_state.agenda[medico_actual][fecha_r] = {h: None for h in HORARIOS}
                        st.session_state.agenda[medico_actual][fecha_r][hora_r] = row["nombre_paciente"]
                        idx = st.session_state.citas[st.session_state.citas["id_cita"]==row["id_cita"]].index
                        st.session_state.citas.loc[idx,"fecha"]  = fecha_r
                        st.session_state.citas.loc[idx,"hora"]   = hora_r
                        st.session_state.citas.loc[idx,"estado"] = "Confirmada"
                        st.success(f"Hora reasignada: {dia_r} {hora_r}")
                        st.rerun()
                else:
                    st.warning(f"{medico_actual} no tiene horas disponibles en la semana de la cita.")

                # Otros medicos misma especialidad
                otros_medicos = [m for m in MEDICOS.get(esp_actual,[]) if m != medico_actual]
                if otros_medicos:
                    st.markdown("**Disponibilidad de otros medicos en la misma especialidad**")
                    for otro in otros_medicos:
                        agenda_otro = st.session_state.agenda.get(otro, {})
                        horas_tot   = sum(1 for f in fechas_semana_cita for h,p in agenda_otro.get(f,{}).items() if p is None)
                        color_disp  = "#137333" if horas_tot > 0 else "#c5221f"
                        st.markdown(f"<span style='color:{color_disp};font-weight:600;'>{otro}</span> — {horas_tot} horas disponibles esa semana", unsafe_allow_html=True)

        b1,b2,b3,_=st.columns([1,1,1,2])
        if b1.button("Confirmar asistencia",key=f"conf_{row['id_cita']}"):
            st.session_state.citas.loc[st.session_state.citas["id_cita"]==row["id_cita"],"estado"]="Confirmada"
            sync_agenda()
            st.success(f"Cita de {row['nombre_paciente']} confirmada.")
            st.rerun()
        if b2.button("Cancelar y liberar cupo",key=f"canc_{row['id_cita']}"):
            st.session_state.citas.loc[st.session_state.citas["id_cita"]==row["id_cita"],"estado"]="Cancelada"
            sync_agenda()
            esp_liberada = row["especialidad"]
            siguiente_espera = st.session_state.espera[
                (st.session_state.espera["especialidad"]==esp_liberada) &
                (st.session_state.espera["estado_espera"]=="Esperando")
            ].sort_values("prioridad", key=lambda x: x.map({"Alta":0,"Media":1,"Baja":2}))
            if len(siguiente_espera) > 0:
                sig = siguiente_espera.iloc[0]
                # Guardar en session state para mostrar despues del rerun
                st.session_state["cupo_liberado"] = {
                    "id_cita": row["id_cita"],
                    "especialidad": esp_liberada,
                    "siguiente_nombre": sig["nombre"],
                    "siguiente_prioridad": sig["prioridad"],
                    "fecha": row["fecha"],
                    "hora": row["hora"]
                }
            else:
                st.session_state["cupo_liberado"] = None
            st.rerun()

        # Mostrar propuesta de asignacion si hay cupo liberado
        if st.session_state.get("cupo_liberado") and st.session_state["cupo_liberado"].get("id_cita") == row["id_cita"]:
            info_cupo = st.session_state["cupo_liberado"]
            st.warning(f"Cupo liberado en {info_cupo['especialidad']} — {info_cupo['fecha']} {info_cupo['hora']} hrs")
            st.info(f"Siguiente paciente en lista de espera: **{info_cupo['siguiente_nombre']}** (Prioridad {info_cupo['siguiente_prioridad']})")
            col_asig1, col_asig2 = st.columns([1,3])
            if col_asig1.button(f"Asignar a {info_cupo['siguiente_nombre']}", key=f"auto_asig_{row['id_cita']}", type="primary"):
                st.session_state.citas.loc[st.session_state.citas["id_cita"]==row["id_cita"],"estado"]="Confirmada"
                st.session_state.citas.loc[st.session_state.citas["id_cita"]==row["id_cita"],"nombre_paciente"]=info_cupo["siguiente_nombre"]
                idx_esp = st.session_state.espera[st.session_state.espera["nombre"]==info_cupo["siguiente_nombre"]].index
                if len(idx_esp)>0:
                    st.session_state.espera.loc[idx_esp[0],"estado_espera"]="Asignado"
                sync_agenda()
                st.session_state["cupo_liberado"] = None
                st.success(f"Cupo asignado a {info_cupo['siguiente_nombre']}.")
                st.rerun()
            if col_asig2.button("Mantener cupo libre por ahora", key=f"keep_libre_{row['id_cita']}"):
                st.session_state["cupo_liberado"] = None
                st.rerun()
        if b3.button("Registrar ausencia",key=f"aus_{row['id_cita']}"):
            st.session_state.citas.loc[st.session_state.citas["id_cita"]==row["id_cita"],"estado"]="Ausente"
            sync_agenda()
            st.error(f"Ausencia de {row['nombre_paciente']} registrada.")
            st.rerun()
        st.markdown("<hr>",unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LISTA DE ESPERA + AGENDA MEDICO
# ─────────────────────────────────────────────
elif modulo == "espera":
    st.markdown("<div style='padding:24px 8px;'>", unsafe_allow_html=True)
    st.markdown("<div class='hsg-section-title'>Lista de Espera</div>", unsafe_allow_html=True)
    st.markdown("<div class='hsg-section-sub'>Reasignacion de cupos — agenda de medicos disponibles</div>", unsafe_allow_html=True)

    # ── Pacientes en espera
    ea = df_espera[df_espera["estado_espera"]=="Esperando"].copy()
    ea["orden"] = ea["prioridad"].map({"Alta":0,"Media":1,"Baja":2})
    ea = ea.sort_values(["orden","fecha_ingreso_espera"])

    col1, col2 = st.columns([1,2])

    with col1:
        # Conteo por prioridad
        total_espera = len(df_espera[df_espera["estado_espera"]=="Esperando"])
        alta_e  = len(df_espera[(df_espera["estado_espera"]=="Esperando") & (df_espera["prioridad"]=="Alta")])
        media_e = len(df_espera[(df_espera["estado_espera"]=="Esperando") & (df_espera["prioridad"]=="Media")])
        baja_e  = len(df_espera[(df_espera["estado_espera"]=="Esperando") & (df_espera["prioridad"]=="Baja")])
        st.markdown(f"**Pacientes en lista de espera** — {total_espera} total · 🔴 {alta_e} Alta · 🟡 {media_e} Media · 🟢 {baja_e} Baja")
        col_fe1, col_fe2 = st.columns(2)
        filtro_esp_e = col_fe1.selectbox("Filtrar por especialidad",
            ["Todas"]+sorted(df_espera["especialidad"].unique().tolist()), key="esp_espera")
        filtro_pri_e = col_fe2.selectbox("Filtrar por prioridad",
            ["Todas","Alta","Media","Baja"], key="pri_espera")
        if filtro_esp_e != "Todas":
            ea = ea[ea["especialidad"]==filtro_esp_e]
        if filtro_pri_e != "Todas":
            ea = ea[ea["prioridad"]==filtro_pri_e]

        def color_p(val):
            return {"Alta":"background-color:#fce8e6;color:#c5221f",
                    "Media":"background-color:#fef7e0;color:#b06000",
                    "Baja":"background-color:#e6f4ea;color:#137333"}.get(val,"")

        def color_dias(val):
            try:
                d = int(val)
                if d > 180: return "background-color:#7b0000;color:white;font-weight:700;"
                if d > 90:  return "background-color:#fce8e6;color:#c5221f;font-weight:700;"
                if d > 30:  return "background-color:#fef7e0;color:#b06000;"
                return ""
            except: return ""

        ea_display = ea[["nombre","especialidad","prioridad","fecha_ingreso_espera","comuna"]].copy()
        ea_display["fecha_ingreso_espera"] = ea_display["fecha_ingreso_espera"].apply(
            lambda f: fecha_es(datetime.strptime(f, "%Y-%m-%d")) if f else f
        )
        ea_display["dias_espera"] = ea[["fecha_ingreso_espera"]]["fecha_ingreso_espera"].apply(
            lambda f: (datetime.today()-datetime.strptime(f,"%Y-%m-%d")).days if f else 0
        ).values
        ea_display.columns = ["Paciente","Especialidad","Prioridad","En espera desde","Comuna","Dias espera"]
        styled = ea_display.style.map(color_p, subset=["Prioridad"]).map(color_dias, subset=["Dias espera"])
        st.dataframe(styled, use_container_width=True, hide_index=True)

    with col2:
        st.markdown("**Agenda de disponibilidad medica**")

        # Seleccion de especialidad y medico
        esp_sel    = st.selectbox("Especialidad", sorted(MEDICOS.keys()), key="esp_agenda")
        medico_sel = st.selectbox("Medico", MEDICOS[esp_sel], key="med_agenda")
        agenda_medico = st.session_state.agenda.get(medico_sel, {})

        # Selector de semana por fecha
        hoy_esp = datetime.today().replace(hour=0,minute=0,second=0,microsecond=0)
        # Empezar desde la proxima semana por defecto
        dias_hasta_lunes = (7 - hoy_esp.weekday()) % 7
        if dias_hasta_lunes == 0:
            dias_hasta_lunes = 7
        semanas_disponibles = []
        for i in range(13):  # proximas 13 semanas (90 dias)
            lunes = hoy_esp + timedelta(days=dias_hasta_lunes + 7*i)
            viernes = lunes + timedelta(days=4)
            label = f"{lunes.strftime('%d %b')} — {viernes.strftime('%d %b %Y')}"
            semanas_disponibles.append((label, lunes))

        semana_label = st.selectbox(
            "Semana a visualizar",
            [s[0] for s in semanas_disponibles],
            key="semana_agenda"
        )
        lunes_sel = dict(semanas_disponibles)[semana_label]
        fechas_semana_esp = [(lunes_sel + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(5)]

        # Asegurar fechas en agenda
        for fecha in fechas_semana_esp:
            if fecha not in agenda_medico:
                agenda_medico[fecha] = {h: None for h in HORARIOS}

        st.markdown(f"**Disponibilidad — {medico_sel} — semana del {semana_label}**")

        dias_labels = ["Lunes","Martes","Miercoles","Jueves","Viernes"]
        # Agregar fecha real debajo del dia
        dias_con_fecha = [
            f"{dias_labels[i]}\n{(lunes_sel+timedelta(days=i)).strftime('%d/%m')}"
            for i in range(5)
        ]

        tabla_data = []
        for hora in HORARIOS:
            fila = {"Hora": hora}
            for i, fecha in enumerate(fechas_semana_esp):
                ocupado = agenda_medico.get(fecha, {}).get(hora, None)
                col_key = f"{dias_labels[i]} {(lunes_sel+timedelta(days=i)).strftime('%d/%m')}"
                fila[col_key] = f"Ocupado: {str(ocupado)[:16]}..." if ocupado else "Disponible"
            tabla_data.append(fila)

        df_agenda = pd.DataFrame(tabla_data).set_index("Hora")

        def color_celda(val):
            if "Ocupado" in str(val):
                return "background-color:#fce8e6;color:#c5221f;font-weight:600;"
            return "background-color:#e6f4ea;color:#137333;font-weight:600;"

        st.dataframe(
            df_agenda.style.map(color_celda),
            use_container_width=True, height=430
        )



    st.divider()

    # ── Asignacion de hora
    st.markdown("### Asignar hora a paciente en espera")
    st.caption("Selecciona el paciente, el medico, el dia y la hora disponible. Las horas ocupadas no pueden seleccionarse.")

    ca, cb, cc = st.columns([2,2,2])
    pa, pb, pc, pd_ = st.columns([2,2,2,1])

    pac_opciones = ea["nombre"].head(20).tolist() if len(ea)>0 else ["Sin pacientes"]
    pac_sel  = ca.selectbox("Paciente en espera", pac_opciones, key="pac_asignar")
    esp_asig = cb.selectbox("Especialidad", sorted(MEDICOS.keys()), key="esp_asignar")
    med_sel  = cc.selectbox("Medico", MEDICOS[esp_asig], key="med_asignar")

    # Buscar dias disponibles en los proximos 30 dias
    hoy_asig = datetime.today().replace(hour=0,minute=0,second=0,microsecond=0)
    todas_fechas_asig = [(hoy_asig+timedelta(days=i)).strftime("%Y-%m-%d") for i in range(90)
                         if (hoy_asig+timedelta(days=i)).weekday() < 5]
    dias_opciones = []
    for fecha in todas_fechas_asig:
        if fecha not in st.session_state.agenda.get(med_sel,{}):
            st.session_state.agenda.setdefault(med_sel,{})[fecha] = {h: None for h in HORARIOS}
        horas_libres = [h for h,p in st.session_state.agenda[med_sel][fecha].items() if p is None]
        if horas_libres:
            dt = datetime.strptime(fecha, "%Y-%m-%d")
            label = f"{DIAS_ES[dt.weekday()].capitalize()} {dt.day} de {MESES_ES[dt.month]} de {dt.year}"
            dias_opciones.append((label, fecha))

    if dias_opciones:
        dia_label = pa.selectbox("Fecha disponible", [d[0] for d in dias_opciones], key="dia_asignar")
        fecha_sel = dict(dias_opciones)[dia_label]
        horas_libres = [h for h,p in st.session_state.agenda[med_sel][fecha_sel].items() if p is None]
        hora_sel = pb.selectbox("Hora disponible", horas_libres, key="hora_asignar")

        if pc.button("Confirmar asignacion de hora", type="primary"):
            st.session_state.agenda[med_sel][fecha_sel][hora_sel] = pac_sel
            idx_esp = st.session_state.espera[st.session_state.espera["nombre"]==pac_sel].index
            if len(idx_esp)>0:
                st.session_state.espera.loc[idx_esp[0],"estado_espera"] = "Asignado"
            # Buscar datos reales del paciente en lista de espera
            pac_data = st.session_state.espera[st.session_state.espera["nombre"]==pac_sel]
            pac_info = pac_data.iloc[0] if len(pac_data)>0 else {}
            nueva_cita = {
                "id_cita": f"C{len(st.session_state.citas)+1:04d}",
                "nombre_paciente": pac_sel,
                "edad": pac_info.get("edad", 0) if hasattr(pac_info, "get") else 0,
                "rut": pac_info.get("rut","—") if hasattr(pac_info, "get") else "—",
                "telefono": pac_info.get("telefono","—") if hasattr(pac_info, "get") else "—",
                "comuna": pac_info.get("comuna","—") if hasattr(pac_info, "get") else "—",
                "especialidad": esp_asig, "medico": med_sel,
                "fecha": fecha_sel, "hora": hora_sel,
                "estado": "Confirmada", "urgencia": "Media",
                "causa_ausencia": "", "contacto_valido": True,
                "es_ges": False, "patologia_ges": "",
                "fecha_diagnostico_ges": "", "fecha_oportunidad_ges": "",
                "riesgo_inasistencia": "Bajo"
            }
            st.session_state.citas = pd.concat(
                [st.session_state.citas, pd.DataFrame([nueva_cita])], ignore_index=True)
            # Simular respuesta automatica del paciente (60% confirma, 20% cancela, 20% sin respuesta)
            respuesta_sim = random.choices(
                ["Confirmo", "Cancelo", "Sin respuesta"],
                weights=[60, 20, 20]
            )[0]
            id_nueva = st.session_state.citas.iloc[-1]["id_cita"]
            if respuesta_sim == "Confirmo":
                st.session_state.citas.loc[st.session_state.citas["id_cita"]==id_nueva,"estado"] = "Confirmada"
            elif respuesta_sim == "Cancelo":
                st.session_state.citas.loc[st.session_state.citas["id_cita"]==id_nueva,"estado"] = "Cancelada"
            sync_agenda()
            st.session_state["ultima_asignacion"] = {
                "paciente": pac_sel,
                "medico": med_sel,
                "dia": dia_label,
                "hora": hora_sel,
                "respuesta": respuesta_sim
            }
            st.rerun()

        # Mostrar resultado de asignacion
        if st.session_state.get("ultima_asignacion"):
            asig = st.session_state["ultima_asignacion"]
            respuesta_asig = asig.get("respuesta")

            st.markdown(f"""
            <div style="background:#e8f5e9;border-left:4px solid #34a853;border-radius:8px;padding:14px 18px;margin:8px 0;">
                <b style="color:#1a3a6b;">Notificacion enviada via SMS/WhatsApp a {asig['paciente']}:</b><br>
                <span style="font-size:13px;color:#444;font-style:italic;">
                "Estimado/a {asig['paciente']}, tiene una nueva cita medica asignada:<br>
                📅 {asig['dia']} a las {asig['hora']} hrs — 👨‍⚕️ {asig['medico']} — 🏥 Hospital San Gabriel"
                </span>
            </div>
            """, unsafe_allow_html=True)

            if respuesta_asig == "Confirmo":
                st.success(f"{asig['paciente']} confirmo automaticamente su nueva cita via mensaje.")
            elif respuesta_asig == "Cancelo":
                st.warning(f"{asig['paciente']} cancelo via mensaje. El cupo fue liberado.")
            else:
                st.info(f"{asig['paciente']} no respondio. El OIRS debera contactarlo manualmente.")

            if st.button("Cerrar", key="cerrar_asig"):
                st.session_state["ultima_asignacion"] = None
                st.rerun()
    else:
        st.warning(f"{med_sel} no tiene horas disponibles en los proximos 30 dias.")

# ─────────────────────────────────────────────
# REPORTES
# ─────────────────────────────────────────────
elif modulo == "reportes":
    st.markdown("<div style='padding:24px 8px;'>", unsafe_allow_html=True)
    st.markdown("<div class='hsg-section-title'>Reportes de Ausentismo</div>", unsafe_allow_html=True)
    st.markdown("<div class='hsg-section-sub'>Analisis estadistico basado en encuesta a pacientes ausentes (n=400)</div>", unsafe_allow_html=True)

    ausentes=df_citas[df_citas["estado"]=="Ausente"]
    total=len(df_citas); tasa=round(len(ausentes)/total*100,1) if total>0 else 0
    c1,c2,c3=st.columns(3)
    c1.metric("Total citas registradas", 2000)
    c2.metric("Total ausencias",len(ausentes))
    c3.metric("Tasa de ausentismo",f"{tasa}%")
    st.divider()

    causas_caso={"No sabia que tenia hora":92,"Olvido la cita":74,"Problemas de transporte":68,
                 "Trabajaba y no pudo":51,"Enfermedad intercurrente":46,
                 "Contacto invalido":39,"Error de agenda":20,"Otros":10}
    df_c2=pd.DataFrame(list(causas_caso.items()),columns=["Causa","Frecuencia"])
    df_c2=df_c2.sort_values("Frecuencia",ascending=False)
    df_c2["% acumulado"]=(df_c2["Frecuencia"].cumsum()/df_c2["Frecuencia"].sum()*100).round(1)

    col_a,col_b=st.columns(2)
    with col_a:
        st.markdown("**Diagrama de Pareto — Causas de ausentismo**")
        st.caption("Datos basados en encuesta real del Hospital San Gabriel (n=400 pacientes ausentes). Las causas 'No sabia que tenia cita' y 'Olvido la cita' representan el 40% del ausentismo y son directamente abordables con el sistema de confirmacion automatica.")
        fig=go.Figure()
        fig.add_bar(x=df_c2["Causa"],y=df_c2["Frecuencia"],name="Frecuencia",marker_color="#1a73e8")
        fig.add_scatter(x=df_c2["Causa"],y=df_c2["% acumulado"],name="% acumulado",
                        yaxis="y2",line=dict(color="#ea4335",width=2),mode="lines+markers")
        fig.update_layout(yaxis=dict(title="Frecuencia"),
                          yaxis2=dict(title="% acumulado",overlaying="y",side="right",range=[0,110]),
                          legend=dict(orientation="h",y=-0.25),
                          margin=dict(l=0,r=0,t=10,b=0),height=360,
                          plot_bgcolor="white",paper_bgcolor="white")
        st.plotly_chart(fig,use_container_width=True)
    with col_b:
        st.markdown("**Tasa de ausentismo por especialidad**")
        ae=df_citas.groupby("especialidad").apply(
            lambda x: round(len(x[x["estado"]=="Ausente"])/len(x)*100,1)).reset_index()
        ae.columns=["Especialidad","Tasa (%)"]
        ae=ae.sort_values("Tasa (%)",ascending=True)
        fig3=px.bar(ae,x="Tasa (%)",y="Especialidad",orientation="h",
                    color="Tasa (%)",color_continuous_scale=["#e6f4ea","#ea4335"],text="Tasa (%)")
        fig3.update_traces(texttemplate="%{text}%",textposition="outside")
        fig3.update_layout(margin=dict(l=0,r=40,t=10,b=0),height=360,
                           coloraxis_showscale=False,plot_bgcolor="white",paper_bgcolor="white",
                           yaxis=dict(tickfont=dict(size=13,color="#1a3a6b")))
        st.plotly_chart(fig3,use_container_width=True)

    sc=df_citas[(df_citas["estado"]=="Ausente")&(~df_citas["contacto_valido"])]
    pct=round(len(sc)/len(ausentes)*100) if len(ausentes)>0 else 0
    st.info(f"De los {len(ausentes)} pacientes ausentes, {len(sc)} ({pct}%) tenian datos de contacto invalidos.")
    csv=df_citas.to_csv(index=False).encode("utf-8")
    # Proyeccion antes/despues
    st.divider()
    st.markdown("**Proyeccion de impacto del sistema de confirmacion automatica**")
    st.caption("Estimacion basada en literatura sobre sistemas de confirmacion proactiva en hospitales publicos.")

    tasa_actual = round(len(ausentes)/total*100,1) if total>0 else 10.8
    tasa_proyectada = round(tasa_actual * 0.65, 1)
    olvido_pct = round((74+73)/400*100, 1)

    col_p1, col_p2, col_p3, col_p4 = st.columns(4)
    col_p1.metric("Tasa ausentismo actual", f"{tasa_actual}%")
    col_p2.metric("Tasa proyectada con sistema", f"{tasa_proyectada}%", delta=f"-{round(tasa_actual-tasa_proyectada,1)}%", delta_color="inverse")
    col_p3.metric("Causas abordables por sistema", f"{olvido_pct}%")
    col_p4.metric("Cupos recuperables al mes", f"~{round((tasa_actual-tasa_proyectada)/100*(total/3))}")

    import plotly.graph_objects as go
    col_chart, col_empty = st.columns([1,1])
    with col_chart:
        fig_comp = go.Figure()
        fig_comp.add_trace(go.Bar(
            x=["Sin sistema\n(actual)", "Con sistema\n(proyectado)"],
            y=[tasa_actual, tasa_proyectada],
            marker_color=["#ea4335","#34a853"],
            text=[f"{tasa_actual}%", f"{tasa_proyectada}%"],
            textposition="outside",
            width=0.4
        ))
        fig_comp.update_layout(
            title="Tasa de ausentismo: antes vs despues",
            yaxis_title="Tasa (%)", height=300,
            plot_bgcolor="white", paper_bgcolor="white",
            margin=dict(l=0,r=0,t=40,b=0),
            yaxis=dict(range=[0, tasa_actual*1.6])
        )
        st.plotly_chart(fig_comp, use_container_width=True)
    st.caption("*Proyeccion estimada con reduccion del 35% del ausentismo, consistente con estudios de confirmacion proactiva en atencion secundaria.")
    st.divider()
    st.download_button("Descargar base de datos (CSV)",csv,"citas_hsg.csv","text/csv")

# ─────────────────────────────────────────────
# AGENDA PROXIMA SEMANA
# ─────────────────────────────────────────────
elif modulo == "agenda_semana":
    st.markdown("<div style='padding:24px 8px;'>", unsafe_allow_html=True)
    st.markdown("<div class='hsg-section-title'>Agenda de Confirmaciones</div>", unsafe_allow_html=True)
    st.markdown("<div class='hsg-section-sub'>Selecciona cualquier semana de los proximos 90 dias para gestionar confirmaciones proactivas</div>", unsafe_allow_html=True)

    # Selector de semana - proximas 13 semanas (90 dias)
    hoy_ag = datetime.today()
    semanas_opciones = []
    for i in range(13):
        lunes_op = hoy_ag + timedelta(days=(7-hoy_ag.weekday())%7 + 7*i)
        if i == 0 and (7-hoy_ag.weekday())%7 == 0:
            lunes_op = hoy_ag + timedelta(days=7)
        lunes_op = lunes_op.replace(hour=0,minute=0,second=0,microsecond=0)
        viernes_op = lunes_op + timedelta(days=4)
        label = f"Semana {i+1} — {lunes_op.strftime('%d/%m')} al {viernes_op.strftime('%d/%m/%Y')}"
        semanas_opciones.append((label, lunes_op))

    semana_sel_label = st.selectbox("Seleccionar semana a gestionar",
        [s[0] for s in semanas_opciones], key="semana_agenda_prox")
    lunes_prox = dict(semanas_opciones)[semana_sel_label]
    viernes_prox = lunes_prox + timedelta(days=4)

    fechas_prox = [(lunes_prox + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(5)]
    dias_nombres = ["Lunes","Martes","Miercoles","Jueves","Viernes"]

    st.markdown(f"""
    <div style="background:#1a3a6b;border-radius:10px;padding:16px 24px;margin-bottom:20px;display:flex;justify-content:space-between;align-items:center;">
        <div>
            <b style="color:#ffffff;font-size:13px;opacity:0.75;text-transform:uppercase;letter-spacing:1px;">Semana a confirmar</b><br>
            <b style="color:#ffffff;font-size:20px;font-weight:700;">{f"{lunes_prox.day} de {MESES_ES[lunes_prox.month]}"} al {f"{viernes_prox.day} de {MESES_ES[viernes_prox.month]} de {viernes_prox.year}"}</b>
        </div>
        <div style="text-align:right;">
            <b style="color:#ffffff;font-size:13px;">Gestionar antes del viernes</b><br>
            <b style="color:#ffffff;font-size:18px;">{hoy_ag.strftime('%d/%m/%Y')}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Filtrar citas de la semana proxima
    riesgo_orden = {"Alto":0,"Medio":1,"Bajo":2}
    citas_prox = df_citas[(df_citas["fecha"].isin(fechas_prox)) & (df_citas["estado"].isin(["Pendiente","Confirmada"]))].copy()
    if "riesgo_inasistencia" in citas_prox.columns:
        citas_prox["riesgo_orden"] = citas_prox["riesgo_inasistencia"].map(riesgo_orden)
        citas_prox = citas_prox.sort_values(["riesgo_orden","hora"])
    citas_prox["dia_semana"] = citas_prox["fecha"].apply(
        lambda f: dias_nombres[datetime.strptime(f, "%Y-%m-%d").weekday()]
    )
    citas_prox["fecha_display"] = citas_prox["fecha"].apply(
        lambda f: datetime.strptime(f, "%Y-%m-%d").strftime("%d de %B de %Y")
    )

    # Metricas
    total_prox   = len(citas_prox)
    confirmadas  = len(citas_prox[citas_prox["estado"]=="Confirmada"])
    pendientes   = len(citas_prox[citas_prox["estado"]=="Pendiente"])
    sin_contacto = len(citas_prox[~citas_prox["contacto_valido"]])

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total citas proxima semana", total_prox)
    c2.metric("Ya confirmadas", confirmadas)
    c3.metric("Pendientes de llamar", pendientes)
    c4.metric("Sin contacto valido", sin_contacto, delta_color="inverse", delta=f"-{sin_contacto}")

    st.divider()

    # Tabs por dia de la semana
    tabs = st.tabs([f"{dias_nombres[i]} {(lunes_prox+timedelta(days=i)).strftime('%d/%m')}" for i in range(5)])

    for i, tab in enumerate(tabs):
        with tab:
            fecha_tab = fechas_prox[i]
            citas_dia = citas_prox[citas_prox["fecha"]==fecha_tab].sort_values("hora")

            if len(citas_dia) == 0:
                st.info(f"No hay citas programadas para este dia.")
                continue

            st.caption(f"{len(citas_dia)} paciente(s) con hora este dia")

            for _, row in citas_dia.iterrows():
                estado  = row["estado"]
                clase   = estado.lower()
                urgencia = row.get("urgencia","Media")
                urgencia = urgencia if urgencia in ["Alta","Media","Baja"] else "Media"
                urg_clase = urgencia.lower()
                contacto_color = "#137333" if row["contacto_valido"] else "#c5221f"
                contacto_txt   = "Valido" if row["contacto_valido"] else "Invalido"
                telefono = row["telefono"]

                st.markdown(f"""
                <div class="cita-card {clase}" style="margin-bottom:8px;">
                    <div class="cita-card-header">
                        <div style="display:flex;align-items:center;gap:12px;">
                            <div style="font-size:18px;font-weight:800;color:#1a3a6b;min-width:50px;">{row['hora']}</div>
                            <div class="cita-nombre">{row['nombre_paciente']}</div>
                        </div>
                        <div class="cita-badges">
                            <span class="badge-{clase}">{estado}</span>
                        </div>
                    </div>
                    <div style="display:flex;gap:32px;flex-wrap:wrap;margin-top:6px;">
                        <div class="cita-info"><b>Especialidad:</b> {row['especialidad']}</div>
                        <div class="cita-info"><b>Medico:</b> {row.get('medico','—')}</div>
                        <div class="cita-info"><b>Comuna:</b> {row['comuna']}</div>
                        <div class="cita-info"><b>Edad:</b> {row['edad']} años</div>
                        <div class="cita-info"><b>Telefono:</b> 
                            <span style="color:{contacto_color};font-weight:700;">{telefono}</span>
                            &nbsp;<span style="font-size:11px;color:{contacto_color};">({contacto_txt})</span>
                        </div>
                        <div class="cita-info"><b>ID:</b> {row['id_cita']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Acciones rapidas de confirmacion
                ba, bb, bc, bd = st.columns([1,1,1,1])
                if ba.button("Confirmar", key=f"aps_conf_{row['id_cita']}"):
                    st.session_state.citas.loc[st.session_state.citas["id_cita"]==row["id_cita"],"estado"]="Confirmada"
                    medico=row.get("medico",""); fecha=row["fecha"]; hora=row["hora"]
                    if medico in st.session_state.agenda:
                        if fecha not in st.session_state.agenda[medico]:
                            st.session_state.agenda[medico][fecha]={h:None for h in HORARIOS}
                        st.session_state.agenda[medico][fecha][hora]=row["nombre_paciente"]
                    st.success(f"{row['nombre_paciente']} confirmado para el {row['hora']} hrs.")
                    st.rerun()
                if bb.button("Cancelar cupo", key=f"aps_canc_{row['id_cita']}"):
                    st.session_state.citas.loc[st.session_state.citas["id_cita"]==row["id_cita"],"estado"]="Cancelada"
                    medico=row.get("medico",""); fecha=row["fecha"]; hora=row["hora"]
                    if medico in st.session_state.agenda:
                        if fecha in st.session_state.agenda.get(medico,{}):
                            st.session_state.agenda[medico][fecha][hora]=None
                    st.warning(f"Cupo de {row['nombre_paciente']} liberado.")
                    st.rerun()
                if bc.button("No contesta", key=f"aps_nc_{row['id_cita']}"):
                    st.info(f"Registrado: {row['nombre_paciente']} no contesta. Intentar nuevamente.")
                    st.rerun()
                if bd.button("Enviar mensaje", key=f"aps_msg_{row['id_cita']}"):
                    if row["contacto_valido"]:
                        fecha_msg = fecha_es(datetime.strptime(row['fecha'], '%Y-%m-%d'))
                        msg = f"Estimado/a {row['nombre_paciente']}, le recordamos su cita el {fecha_msg} a las {row['hora']} hrs con {row.get('medico','su medico')} en {row['especialidad']}. Responda 1 para CONFIRMAR o 2 para CANCELAR. Hospital San Gabriel."
                        st.session_state[f"msg_ind_{row['id_cita']}"] = msg
                        st.rerun()
                    else:
                        st.error(f"Contacto invalido — no se puede enviar mensaje a {row['nombre_paciente']}.")

                if st.session_state.get(f"msg_ind_{row['id_cita']}"):
                    msg_txt = st.session_state[f"msg_ind_{row['id_cita']}"]
                    st.markdown(f"""
                    <div style="background:#e8f5e9;border-left:4px solid #34a853;border-radius:8px;
                                padding:10px 14px;margin:4px 0;font-size:12px;color:#444;">
                        <b style="color:#137333;">Mensaje enviado:</b> {msg_txt}
                    </div>
                    """, unsafe_allow_html=True)
                    col_m1, col_m2, col_m3 = st.columns([1,1,3])
                    if col_m1.button("Confirmo", key=f"msg_ind_conf_{row['id_cita']}", type="primary"):
                        st.session_state.citas.loc[st.session_state.citas["id_cita"]==row["id_cita"],"estado"]="Confirmada"
                        st.session_state.pop(f"msg_ind_{row['id_cita']}", None)
                        sync_agenda()
                        st.rerun()
                    if col_m2.button("Cancelo", key=f"msg_ind_canc_{row['id_cita']}"):
                        st.session_state.citas.loc[st.session_state.citas["id_cita"]==row["id_cita"],"estado"]="Cancelada"
                        st.session_state.pop(f"msg_ind_{row['id_cita']}", None)
                        sync_agenda()
                        st.rerun()

                st.markdown("<hr style='margin:8px 0;border-color:#f0f0f0;'>", unsafe_allow_html=True)

    st.divider()

    # ── CONFIRMACION AUTOMATICA ──
    st.markdown("### Confirmacion automatica de citas")
    st.caption("Simula el envio de mensajes automaticos (SMS/WhatsApp) a los pacientes pendientes de confirmar.")

    pendientes_auto = citas_prox[citas_prox["estado"]=="Pendiente"].copy()
    con_contacto    = pendientes_auto[pendientes_auto["contacto_valido"]==True]
    sin_contacto_auto = pendientes_auto[pendientes_auto["contacto_valido"]==False]

    col_auto1, col_auto2, col_auto3 = st.columns(3)
    col_auto1.metric("Pendientes de confirmar", len(pendientes_auto))
    col_auto2.metric("Con contacto valido", len(con_contacto), delta=f"{len(con_contacto)} mensajes listos")
    col_auto3.metric("Sin contacto valido", len(sin_contacto_auto), delta_color="inverse", delta=f"-{len(sin_contacto_auto)} requieren llamada")

    # Selector de tipo de mensaje
    tipo_msg = st.selectbox("Tipo de mensaje", 
        ["SMS", "WhatsApp", "Ambos (SMS + WhatsApp)"], key="tipo_msg")
    
    # Preview del mensaje
    st.markdown("**Vista previa del mensaje:**")
    if len(con_contacto) > 0:
        ejemplo = con_contacto.iloc[0]
        fecha_ej = fecha_es(datetime.strptime(ejemplo['fecha'], '%Y-%m-%d'))
        st.markdown(f"""
        <div style="background:#e8f5e9;border-left:4px solid #34a853;border-radius:8px;padding:16px 20px;font-size:13px;color:#1a3a6b;max-width:500px;">
            <b>Hospital San Gabriel</b><br><br>
            Estimado/a <b>{ejemplo['nombre_paciente']}</b>,<br><br>
            Le recordamos que tiene una cita medica programada:<br>
            📅 <b>Fecha:</b> {fecha_ej}<br>
            🕐 <b>Hora:</b> {ejemplo['hora']} hrs<br>
            👨‍⚕️ <b>Medico:</b> {ejemplo.get('medico','—')}<br>
            🏥 <b>Especialidad:</b> {ejemplo['especialidad']}<br><br>
            Por favor confirme su asistencia respondiendo:<br>
            <b>1</b> para CONFIRMAR &nbsp;|&nbsp; <b>2</b> para CANCELAR<br><br>
            <i>Hospital San Gabriel — Red Asistencial Sur</i>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    # Inicializar estado de envios
    if "envios_realizados" not in st.session_state:
        st.session_state.envios_realizados = {}

    col_btn1, col_btn2 = st.columns([1,3])
    
    col_sim = st.columns([1,1,2])[1]
    if "simulacion_activa" not in st.session_state:
        st.session_state.simulacion_activa = False

    if col_btn1.button("Enviar mensajes automaticos", type="primary",
                        disabled=len(con_contacto)==0):
        # Simular envio con mensaje personalizado por paciente
        enviados = 0
        fallidos = 0
        for _, row in con_contacto.iterrows():
            fecha_msg = fecha_es(datetime.strptime(row['fecha'], '%Y-%m-%d'))
            mensaje_personalizado = f"""Hospital San Gabriel
Estimado/a {row['nombre_paciente']},
Le recordamos su cita medica:
Fecha: {fecha_msg}
Hora: {row['hora']} hrs
Medico: {row.get('medico','—')}
Especialidad: {row['especialidad']}
Responda 1 para CONFIRMAR o 2 para CANCELAR.
Hospital San Gabriel - Red Asistencial Sur"""
            st.session_state.envios_realizados[row["id_cita"]] = {
                "estado": "Enviado",
                "tipo": tipo_msg,
                "hora_envio": datetime.now().strftime("%H:%M"),
                "telefono": row["telefono"],
                "mensaje": mensaje_personalizado
            }
            enviados += 1
        for _, row in sin_contacto_auto.iterrows():
            st.session_state.envios_realizados[row["id_cita"]] = {
                "estado": "Fallido",
                "tipo": tipo_msg,
                "hora_envio": datetime.now().strftime("%H:%M"),
                "telefono": row["telefono"],
                "mensaje": ""
            }
            fallidos += 1
        st.success(f"{enviados} mensajes personalizados enviados via {tipo_msg}.")
        if fallidos > 0:
            st.warning(f"{fallidos} mensajes fallidos por contacto invalido — requieren llamada manual.")
        st.rerun()

    # Boton simular respuestas automaticas
    if st.session_state.envios_realizados:
        enviados_ids = [k for k,v in st.session_state.envios_realizados.items() if v["estado"]=="Enviado"]
        sin_resp_ids = [k for k in enviados_ids if k not in st.session_state.get("respuestas_pacientes",{})]

        if len(sin_resp_ids) > 0:
            st.markdown("")
            if st.button(f"Simular respuestas entrantes ({len(sin_resp_ids)} pendientes)", type="secondary"):
                if "respuestas_pacientes" not in st.session_state:
                    st.session_state.respuestas_pacientes = {}
                for id_cita in sin_resp_ids:
                    # 60% confirma, 20% cancela, 20% no responde
                    resultado = random.choices(
                        ["Confirmo", "Cancelo", "Sin respuesta"],
                        weights=[60, 20, 20]
                    )[0]
                    st.session_state.respuestas_pacientes[id_cita] = resultado
                    if resultado == "Confirmo":
                        st.session_state.citas.loc[
                            st.session_state.citas["id_cita"]==id_cita,"estado"] = "Confirmada"
                    elif resultado == "Cancelo":
                        st.session_state.citas.loc[
                            st.session_state.citas["id_cita"]==id_cita,"estado"] = "Cancelada"
                sync_agenda()
                confirmados_sim = len([r for r in st.session_state.respuestas_pacientes.values() if r=="Confirmo"])
                cancelados_sim  = len([r for r in st.session_state.respuestas_pacientes.values() if r=="Cancelo"])
                sin_resp_sim    = len([r for r in st.session_state.respuestas_pacientes.values() if r=="Sin respuesta"])
                st.success(f"Respuestas simuladas: {confirmados_sim} confirmaron, {cancelados_sim} cancelaron, {sin_resp_sim} no respondieron.")
                st.rerun()

    # Mostrar registro de envios y respuestas
    if st.session_state.envios_realizados:
        st.markdown("**Bandeja de respuestas — registra la respuesta recibida por cada paciente:**")

        # Inicializar respuestas
        if "respuestas_pacientes" not in st.session_state:
            st.session_state.respuestas_pacientes = {}

        # Mostrar TODOS los cupos pendientes de asignar
        if st.session_state.get("cupos_liberados") and len(st.session_state.cupos_liberados) > 0:
            st.markdown("---")
            st.markdown(f"**{len(st.session_state.cupos_liberados)} cupo(s) liberado(s) esperando asignacion:**")
            for idx_cupo, info_cupo_top in enumerate(st.session_state.cupos_liberados):
                st.warning(f"Cupo {idx_cupo+1}: **{info_cupo_top['especialidad']}** — {info_cupo_top['fecha']} {info_cupo_top['hora']} hrs (de {info_cupo_top['paciente_original']})")
                st.info(f"Siguiente en lista de espera: **{info_cupo_top['siguiente_nombre']}** (Prioridad {info_cupo_top['siguiente_prioridad']})")
                col_top1, col_top2 = st.columns([1,3])
                if col_top1.button(f"Asignar a {info_cupo_top['siguiente_nombre']}", key=f"top_asig_{idx_cupo}", type="primary"):
                    id_c_top = info_cupo_top["id_cita"]
                    st.session_state.citas.loc[st.session_state.citas["id_cita"]==id_c_top,"estado"]="Confirmada"
                    st.session_state.citas.loc[st.session_state.citas["id_cita"]==id_c_top,"nombre_paciente"]=info_cupo_top["siguiente_nombre"]
                    idx_top = st.session_state.espera[st.session_state.espera["nombre"]==info_cupo_top["siguiente_nombre"]].index
                    if len(idx_top)>0:
                        st.session_state.espera.loc[idx_top[0],"estado_espera"]="Asignado"
                    sync_agenda()
                    st.session_state.cupos_liberados.pop(idx_cupo)
                    st.success(f"Cupo asignado a {info_cupo_top['siguiente_nombre']}.")
                    st.rerun()
                if col_top2.button("Mantener cupo libre", key=f"top_keep_{idx_cupo}"):
                    st.session_state.cupos_liberados.pop(idx_cupo)
                    st.rerun()
            st.markdown("---")

        for id_cita, info in st.session_state.envios_realizados.items():
            cita_row = df_citas[df_citas["id_cita"]==id_cita]
            if len(cita_row) == 0:
                continue
            row = cita_row.iloc[0]
            respuesta_actual = st.session_state.respuestas_pacientes.get(id_cita, "Sin respuesta")
            estado_envio = info["estado"]

            # Color segun respuesta
            if respuesta_actual == "Confirmo":
                border_color = "#34a853"; bg_color = "#f0faf0"
            elif respuesta_actual == "Cancelo":
                border_color = "#ea4335"; bg_color = "#fff5f5"
            elif estado_envio == "Fallido":
                border_color = "#9aa0a6"; bg_color = "#f8f9fa"
            else:
                border_color = "#f9ab00"; bg_color = "#fffdf0"

            fecha_display_msg = fecha_es(datetime.strptime(row['fecha'], '%Y-%m-%d')) if row['fecha'] else row['fecha']
            msg_preview = info.get('mensaje','').replace('\n','<br>')
            st.markdown(f"""
            <div style="background:{bg_color};border-left:4px solid {border_color};
                        border-radius:8px;padding:12px 16px;margin-bottom:8px;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                    <div>
                        <b style="font-size:14px;color:#1a3a6b;">{row['nombre_paciente']}</b>
                        <span style="font-size:12px;color:#666;margin-left:12px;">{row['especialidad']} — {fecha_display_msg} {row['hora']} hrs</span>
                    </div>
                    <div style="font-size:12px;color:#666;">
                        {info['tipo']} → {info['telefono']} — {info['hora_envio']}
                        &nbsp;|&nbsp;
                        <b style="color:{'#34a853' if estado_envio=='Enviado' else '#c5221f'};">
                            {'Enviado' if estado_envio=='Enviado' else 'Fallido — llamar manualmente'}
                        </b>
                    </div>
                </div>
                {f'<div style="background:#f8f9fa;border-radius:6px;padding:8px 12px;font-size:12px;color:#444;max-width:500px;">{msg_preview}</div>' if msg_preview else ""}
            </div>
            """, unsafe_allow_html=True)

            if estado_envio == "Enviado":
                col_r1, col_r2, col_r3, col_r4 = st.columns([1,1,1,2])
                if col_r1.button("1 - Confirmo", key=f"resp_conf_{id_cita}",
                                  type="primary" if respuesta_actual=="Sin respuesta" else "secondary"):
                    st.session_state.respuestas_pacientes[id_cita] = "Confirmo"
                    st.session_state.citas.loc[st.session_state.citas["id_cita"]==id_cita,"estado"] = "Confirmada"
                    sync_agenda()
                    st.success(f"{row['nombre_paciente']} confirmo su asistencia via {info['tipo']}.")
                    st.rerun()
                if col_r2.button("2 - Cancelo", key=f"resp_canc_{id_cita}"):
                    st.session_state.respuestas_pacientes[id_cita] = "Cancelo"
                    st.session_state.citas.loc[st.session_state.citas["id_cita"]==id_cita,"estado"] = "Cancelada"
                    sync_agenda()
                    # Asignar automaticamente al siguiente en lista de espera
                    esp_sms = row["especialidad"]
                    sig_sms = st.session_state.espera[
                        (st.session_state.espera["especialidad"]==esp_sms) &
                        (st.session_state.espera["estado_espera"]=="Esperando")
                    ].sort_values("prioridad", key=lambda x: x.map({"Alta":0,"Media":1,"Baja":2}))
                    if len(sig_sms)>0:
                        sig = sig_sms.iloc[0]
                        # Agregar a lista de cupos pendientes
                        if "cupos_liberados" not in st.session_state:
                            st.session_state.cupos_liberados = []
                        # Verificar que no este ya en la lista
                        ids_pendientes = [c["id_cita"] for c in st.session_state.cupos_liberados]
                        if id_cita not in ids_pendientes:
                            st.session_state.cupos_liberados.append({
                                "id_cita": id_cita,
                                "especialidad": esp_sms,
                                "siguiente_nombre": sig["nombre"],
                                "siguiente_prioridad": sig["prioridad"],
                                "fecha": row["fecha"],
                                "hora": row["hora"],
                                "paciente_original": row["nombre_paciente"]
                            })
                        st.warning(f"{row['nombre_paciente']} cancelo via {info['tipo']}.")
                    else:
                        st.warning(f"{row['nombre_paciente']} cancelo. No hay pacientes en espera para {esp_sms}.")
                    st.rerun()
                if col_r3.button("Sin respuesta", key=f"resp_nr_{id_cita}"):
                    st.session_state.respuestas_pacientes[id_cita] = "Sin respuesta"
                    st.info(f"{row['nombre_paciente']} no respondio. Intentar llamada manual.")
                    st.rerun()
                # Mostrar respuesta actual
                if respuesta_actual != "Sin respuesta":
                    col_r4.markdown(f"**Respuesta:** {respuesta_actual}", unsafe_allow_html=False)
            else:
                st.caption("Requiere llamada manual — contacto invalido")

            # Mostrar propuesta de asignacion si este cupo fue liberado via SMS
            if st.session_state.get("cupo_liberado") and st.session_state["cupo_liberado"].get("id_cita") == id_cita:
                info_cupo = st.session_state["cupo_liberado"]
                st.info(f"Siguiente en lista de espera: **{info_cupo['siguiente_nombre']}** (Prioridad {info_cupo['siguiente_prioridad']})")
                col_sa1, col_sa2 = st.columns([1,3])
                if col_sa1.button(f"Asignar a {info_cupo['siguiente_nombre']}", key=f"sms_asig_{id_cita}", type="primary"):
                    st.session_state.citas.loc[st.session_state.citas["id_cita"]==id_cita,"estado"]="Confirmada"
                    st.session_state.citas.loc[st.session_state.citas["id_cita"]==id_cita,"nombre_paciente"]=info_cupo["siguiente_nombre"]
                    idx_esp2 = st.session_state.espera[st.session_state.espera["nombre"]==info_cupo["siguiente_nombre"]].index
                    if len(idx_esp2)>0:
                        st.session_state.espera.loc[idx_esp2[0],"estado_espera"]="Asignado"
                    sync_agenda()
                    st.session_state["cupo_liberado"] = None
                    st.success(f"Cupo asignado a {info_cupo['siguiente_nombre']}.")
                    st.rerun()
                if col_sa2.button("Mantener cupo libre", key=f"sms_keep_{id_cita}"):
                    st.session_state["cupo_liberado"] = None
                    st.rerun()

            st.markdown("<hr style='margin:4px 0;border-color:#f0f0f0;'>", unsafe_allow_html=True)

        # Resumen de respuestas
        total_env = len([i for i in st.session_state.envios_realizados.values() if i["estado"]=="Enviado"])
        confirmados_resp = len([r for r in st.session_state.respuestas_pacientes.values() if r=="Confirmo"])
        cancelados_resp  = len([r for r in st.session_state.respuestas_pacientes.values() if r=="Cancelo"])
        sin_resp = total_env - confirmados_resp - cancelados_resp

        st.divider()
        st.markdown("**Resumen de respuestas recibidas:**")
        cr1, cr2, cr3 = st.columns(3)
        cr1.metric("Confirmaron", confirmados_resp)
        cr2.metric("Cancelaron", cancelados_resp)
        cr3.metric("Sin respuesta aun", sin_resp)

        # Exportar
        registros = []
        for id_cita, info in st.session_state.envios_realizados.items():
            cita_row = df_citas[df_citas["id_cita"]==id_cita]
            if len(cita_row) > 0:
                row = cita_row.iloc[0]
                registros.append({
                    "Paciente": row["nombre_paciente"],
                    "Telefono": info["telefono"],
                    "Canal": info["tipo"],
                    "Estado envio": info["estado"],
                    "Respuesta": st.session_state.respuestas_pacientes.get(id_cita, "Sin respuesta"),
                    "Hora envio": info["hora_envio"],
                    "Especialidad": row["especialidad"],
                    "Fecha cita": row["fecha"]
                })
        if registros:
            csv_reg = pd.DataFrame(registros).to_csv(index=False).encode("utf-8")
            st.download_button("Descargar registro completo (CSV)",
                             csv_reg, "registro_envios.csv", "text/csv")

    st.divider()

    # Resumen de llamadas pendientes
    st.markdown("**Pacientes que requieren llamada manual (contacto invalido)**")
    pendientes_df = citas_prox[(citas_prox["estado"]=="Pendiente") & (citas_prox["contacto_valido"]==False)][
        ["nombre_paciente","especialidad","fecha_display","hora","telefono","contacto_valido","urgencia"]
    ].copy()
    pendientes_df = pendientes_df.sort_values(["urgencia","fecha_display"], 
        key=lambda col: col.map({"Alta":0,"Media":1,"Baja":2}) if col.name=="urgencia" else col)
    pendientes_df.columns = ["Paciente","Especialidad","Fecha","Hora","Telefono","Contacto valido","Urgencia"]
    pendientes_df["Contacto valido"] = pendientes_df["Contacto valido"].map({True:"Si",False:"No"})

    if len(pendientes_df) > 0:
        st.dataframe(pendientes_df, use_container_width=True, hide_index=True)
        csv_pend = pendientes_df.to_csv(index=False).encode("utf-8")
        st.download_button("Descargar lista de llamadas (CSV)", csv_pend, "llamadas_proxima_semana.csv","text/csv")
    else:
        st.success("Todos los pacientes de la proxima semana ya tienen su cita confirmada.")



# ─────────────────────────────────────────────
# MODULO GES
# ─────────────────────────────────────────────
elif modulo == "ges":
    st.markdown("<div style='padding:24px 8px;'>", unsafe_allow_html=True)
    st.markdown("<div class='hsg-section-title'>Pacientes GES</div>", unsafe_allow_html=True)
    st.markdown("<div class='hsg-section-sub'>Garantias Explicitas en Salud — seguimiento de oportunidades y plazos garantizados — proximos 90 dias</div>", unsafe_allow_html=True)

    # Filtrar pacientes GES
    citas_ges = df_citas[df_citas["es_ges"]==True].copy() if "es_ges" in df_citas.columns else pd.DataFrame()

    if len(citas_ges) == 0:
        st.info("No hay pacientes GES registrados.")
    else:
        hoy_str = datetime.today().strftime("%Y-%m-%d")
        citas_ges["estado_oportunidad"] = citas_ges["fecha_oportunidad_ges"].apply(
            lambda f: "Vencida" if f < hoy_str else
                      "Urgente" if (datetime.strptime(f,"%Y-%m-%d")-datetime.today()).days <= 15 else "Vigente"
        )

        # Metricas
        total_ges   = len(citas_ges)
        vencidas    = len(citas_ges[citas_ges["estado_oportunidad"]=="Vencida"])
        urgentes    = len(citas_ges[citas_ges["estado_oportunidad"]=="Urgente"])
        vigentes    = len(citas_ges[citas_ges["estado_oportunidad"]=="Vigente"])

        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Total pacientes GES", total_ges)
        c2.metric("Oportunidad vencida", vencidas, delta_color="inverse", delta=f"-{vencidas}" if vencidas>0 else "0")
        c3.metric("Proximos a vencer (15 dias)", urgentes, delta_color="inverse", delta=f"-{urgentes}" if urgentes>0 else "0")
        c4.metric("Vigentes", vigentes)

        st.divider()

        # Filtros
        col_f1, col_f2, col_f3 = st.columns(3)
        filtro_ges_estado = col_f1.selectbox("Estado oportunidad", ["Todos","Vencida","Urgente","Vigente"], key="ges_estado")
        filtro_ges_pat    = col_f2.selectbox("Patologia", ["Todas"]+sorted(citas_ges["patologia_ges"].unique().tolist()), key="ges_pat")
        filtro_ges_esp    = col_f3.selectbox("Especialidad", ["Todas"]+sorted(citas_ges["especialidad"].unique().tolist()), key="ges_esp")

        ges_filtradas = citas_ges.copy()
        if filtro_ges_estado != "Todos":
            ges_filtradas = ges_filtradas[ges_filtradas["estado_oportunidad"]==filtro_ges_estado]
        if filtro_ges_pat != "Todas":
            ges_filtradas = ges_filtradas[ges_filtradas["patologia_ges"]==filtro_ges_pat]
        if filtro_ges_esp != "Todas":
            ges_filtradas = ges_filtradas[ges_filtradas["especialidad"]==filtro_ges_esp]
        
        # Incluir citas GES canceladas recientemente que tienen cupo pendiente
        if st.session_state.get("cupos_liberados"):
            ids_pendientes = [c["id_cita"] for c in st.session_state.cupos_liberados]
            canceladas_ges = citas_ges[
                (citas_ges["id_cita"].isin(ids_pendientes)) & 
                (~citas_ges["id_cita"].isin(ges_filtradas["id_cita"]))
            ]
            if len(canceladas_ges) > 0:
                ges_filtradas = pd.concat([canceladas_ges, ges_filtradas], ignore_index=True)

        # Ordenar: vencidas primero, luego urgentes, luego vigentes
        orden_map = {"Vencida":0,"Urgente":1,"Vigente":2}
        ges_filtradas["orden"] = ges_filtradas["estado_oportunidad"].map(orden_map)
        ges_filtradas = ges_filtradas.sort_values("orden")

        st.caption(f"{len(ges_filtradas)} paciente(s) GES encontrados")

        if len(ges_filtradas) == 0:
            st.info("No se encontraron pacientes GES con los filtros seleccionados. Prueba cambiando los filtros.")
        
        for _, row in ges_filtradas.iterrows():
            est_op = row["estado_oportunidad"]
            clase_card = est_op.lower()
            
            if est_op == "Vencida":
                badge_html = "<span class='badge-ges-vencida'>OPORTUNIDAD VENCIDA</span>"
                dias_txt = f"Vencio hace {abs((datetime.strptime(row['fecha_oportunidad_ges'],'%Y-%m-%d')-datetime.today()).days)} dias"
                color_dias = "#7b0000"
            elif est_op == "Urgente":
                dias_rest = (datetime.strptime(row['fecha_oportunidad_ges'],'%Y-%m-%d')-datetime.today()).days
                badge_html = f"<span class='badge-ges-urgente'>URGENTE — {dias_rest} dias restantes</span>"
                dias_txt = f"Vence en {dias_rest} dias"
                color_dias = "#ea4335"
            else:
                dias_rest = (datetime.strptime(row['fecha_oportunidad_ges'],'%Y-%m-%d')-datetime.today()).days
                badge_html = f"<span class='badge-ges-ok'>VIGENTE — {dias_rest} dias restantes</span>"
                dias_txt = f"Vence en {dias_rest} dias"
                color_dias = "#137333"

            estado_cita = row["estado"]
            clase_estado = estado_cita.lower()

            st.markdown(f"""
            <div class="ges-card {clase_card}">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
                    <div style="font-size:15px;font-weight:700;color:#1a3a6b;">{row['nombre_paciente']}</div>
                    <div style="display:flex;gap:8px;align-items:center;">
                        {badge_html}
                        <span class="badge-{clase_estado}">{estado_cita}</span>
                    </div>
                </div>
                <div style="display:flex;gap:32px;flex-wrap:wrap;">
                    <div class="cita-info"><b>Patologia GES:</b> <span style="color:#1a73e8;font-weight:600;">{row['patologia_ges']}</span></div>
                    <div class="cita-info"><b>Especialidad:</b> {row['especialidad']}</div>
                    <div class="cita-info"><b>Medico:</b> {row.get('medico','—')}</div>
                    <div class="cita-info"><b>Fecha cita:</b> {fecha_es(datetime.strptime(row['fecha'],"%Y-%m-%d"))} — {row['hora']} hrs</div>
                    <div class="cita-info"><b>Telefono:</b> {row['telefono']}</div>
                    <div class="cita-info"><b>Diagnostico GES:</b> {fecha_es(datetime.strptime(row['fecha_diagnostico_ges'],"%Y-%m-%d"))}</div>
                    <div class="cita-info"><b>Oportunidad:</b> <span style="color:{color_dias};font-weight:700;">{fecha_es(datetime.strptime(row['fecha_oportunidad_ges'],"%Y-%m-%d"))} — {dias_txt}</span></div>
                    <div class="cita-info"><b>RUT:</b> {row['rut']}</div>
                    <div class="cita-info"><b>ID:</b> {row['id_cita']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            ba, bb, bc = st.columns([1,1,1])
            if ba.button("Confirmar asistencia", key=f"ges_conf_{row['id_cita']}"):
                st.session_state.citas.loc[st.session_state.citas["id_cita"]==row["id_cita"],"estado"]="Confirmada"
                sync_agenda()
                st.success(f"Cita GES de {row['nombre_paciente']} confirmada.")
                st.rerun()
            if bb.button("Cancelar cupo", key=f"ges_canc_{row['id_cita']}"):
                st.session_state.citas.loc[st.session_state.citas["id_cita"]==row["id_cita"],"estado"]="Cancelada"
                sync_agenda()
                esp_ges = row["especialidad"]
                sig_ges = st.session_state.espera[
                    (st.session_state.espera["especialidad"]==esp_ges) &
                    (st.session_state.espera["estado_espera"]=="Esperando")
                ].sort_values("prioridad", key=lambda x: x.map({"Alta":0,"Media":1,"Baja":2}))
                if "cupos_liberados" not in st.session_state:
                    st.session_state.cupos_liberados = []
                if len(sig_ges)>0:
                    sig = sig_ges.iloc[0]
                    ids_pend = [c["id_cita"] for c in st.session_state.cupos_liberados]
                    if row["id_cita"] not in ids_pend:
                        st.session_state.cupos_liberados.append({
                            "id_cita": row["id_cita"],
                            "especialidad": esp_ges,
                            "siguiente_nombre": sig["nombre"],
                            "siguiente_prioridad": sig["prioridad"],
                            "fecha": row["fecha"],
                            "hora": row["hora"],
                            "paciente_original": row["nombre_paciente"]
                        })
                    st.session_state["ges_mostrar_asig"] = row["id_cita"]
                st.rerun()

            # Mostrar propuesta justo debajo del paciente cancelado
            if st.session_state.get("cupos_liberados"):
                for idx_cg, info_cupo in enumerate(st.session_state.cupos_liberados):
                    if info_cupo.get("id_cita") == row["id_cita"]:
                        st.markdown(f"""
                        <div style="background:#fff8e1;border-left:4px solid #f9ab00;border-radius:8px;
                                    padding:14px 18px;margin:8px 0;">
                            <b style="color:#1a3a6b;">Cupo liberado — {info_cupo['especialidad']} · {info_cupo['fecha']} {info_cupo['hora']} hrs</b><br>
                            <span style="color:#444;font-size:13px;">Siguiente en lista de espera: 
                            <b>{info_cupo['siguiente_nombre']}</b> (Prioridad {info_cupo['siguiente_prioridad']})</span>
                        </div>
                        """, unsafe_allow_html=True)
                        col_g1, col_g2 = st.columns([1,3])
                        if col_g1.button(f"Asignar a {info_cupo['siguiente_nombre']}", key=f"ges_auto_asig_{row['id_cita']}", type="primary"):
                            st.session_state.citas.loc[st.session_state.citas["id_cita"]==row["id_cita"],"estado"]="Confirmada"
                            st.session_state.citas.loc[st.session_state.citas["id_cita"]==row["id_cita"],"nombre_paciente"]=info_cupo["siguiente_nombre"]
                            idx_esp = st.session_state.espera[st.session_state.espera["nombre"]==info_cupo["siguiente_nombre"]].index
                            if len(idx_esp)>0:
                                st.session_state.espera.loc[idx_esp[0],"estado_espera"]="Asignado"
                            sync_agenda()
                            st.session_state.cupos_liberados.pop(idx_cg)
                            st.success(f"Cupo GES asignado a {info_cupo['siguiente_nombre']}.")
                            st.rerun()
                        if col_g2.button("Mantener cupo libre", key=f"ges_keep_{row['id_cita']}"):
                            st.session_state.cupos_liberados.pop(idx_cg)
                            st.rerun()
                        break

        if bc.button("Registrar ausencia", key=f"ges_aus_{row['id_cita']}"):
            st.session_state.citas.loc[st.session_state.citas["id_cita"]==row["id_cita"],"estado"]="Ausente"
            sync_agenda()
            st.error(f"Ausencia GES registrada para {row['nombre_paciente']}.")
            st.rerun()
        st.markdown("<hr>", unsafe_allow_html=True)

        # Grafico por patologia
        st.divider()
        st.markdown("**Distribucion de pacientes GES por patologia**")
        ges_pat = citas_ges.groupby(["patologia_ges","estado_oportunidad"]).size().reset_index(name="cantidad")
        fig_ges = px.bar(ges_pat, x="cantidad", y="patologia_ges", color="estado_oportunidad",
                         orientation="h", barmode="stack",
                         color_discrete_map={"Vencida":"#7b0000","Urgente":"#ea4335","Vigente":"#1a73e8"})
        fig_ges.update_layout(margin=dict(l=0,r=0,t=10,b=0), height=350,
                              plot_bgcolor="white", paper_bgcolor="white",
                              legend=dict(orientation="h",y=-0.2),
                              xaxis_title="Cantidad", yaxis_title="")
        st.plotly_chart(fig_ges, use_container_width=True)
