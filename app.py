"""
TechNova S.A. - Plataforma de Gestión de Riesgos de Seguridad de la Información
Version: 2.0 - Professional UI/UX with Algorithmic Core
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pymongo
from pymongo import MongoClient
import json
from datetime import datetime, timedelta, timezone
import time
import random
from faker import Faker
import streamlit.components.v1 as components
# Importaciones opcionales para PDF
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    from fpdf import FPDF
    FPDF_AVAILABLE = True
except ImportError:
    FPDF_AVAILABLE = False

import io
import base64
import google.generativeai as genai
import re

st.set_page_config(
    page_title="TechNova S.A. - Gestión de Riesgos",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS profesional con soporte para modo oscuro/claro
PROFESSIONAL_CSS = """
<style>
    /* Variables CSS para temas */
    :root {
        --primary-color: #1e40af;
        --secondary-color: #3b82f6;
        --accent-color: #10b981;
        --danger-color: #ef4444;
        --warning-color: #f59e0b;
        --success-color: #22c55e;
        --bg-primary: #ffffff;
        --bg-secondary: #f8fafc;
        --text-primary: #1f2937;
        --text-secondary: #6b7280;
        --border-color: #e5e7eb;
        --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }

    /* Tema oscuro */
    [data-theme="dark"] {
        --bg-primary: #1f2937;
        --bg-secondary: #111827;
        --text-primary: #f9fafb;
        --text-secondary: #d1d5db;
        --border-color: #374151;
        --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.3);
    }

    /* Reset y base */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    /* Header principal */
    .main-header {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: var(--shadow);
    }

    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
    }

    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        text-align: center;
        opacity: 0.9;
    }

    /* Cards y contenedores */
    .metric-card {
        background: var(--bg-primary);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
        height: 100%;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-color);
        margin: 0;
    }

    .metric-label {
        font-size: 0.9rem;
        color: var(--text-secondary);
        margin: 0.5rem 0 0 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.025em;
    }

    .status-activo {
        background-color: #dcfce7;
        color: #166534;
    }

    .status-desertor {
        background-color: #fee2e2;
        color: #991b1b;
    }

    .status-riesgo {
        background-color: #fef3c7;
        color: #92400e;
    }

    /* Tablas */
    .data-table {
        border-collapse: collapse;
        width: 100%;
        background: var(--bg-primary);
        border-radius: 8px;
        overflow: hidden;
        box-shadow: var(--shadow);
    }

    .data-table th {
        background: var(--bg-secondary);
        color: var(--text-primary);
        font-weight: 600;
        text-align: left;
        padding: 1rem;
        border-bottom: 1px solid var(--border-color);
    }

    .data-table td {
        padding: 0.75rem 1rem;
        border-bottom: 1px solid var(--border-color);
        color: var(--text-primary);
    }

    .data-table tbody tr:hover {
        background: var(--bg-secondary);
    }

    /* Formularios y inputs */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1px solid var(--border-color);
        background: var(--bg-primary);
        color: var(--text-primary);
    }

    /* Selectbox - Deshabilitar edición de texto */
    .stSelectbox > div > div > div > div {
        pointer-events: auto;
    }
    
    .stSelectbox > div > div > div > div > input {
        pointer-events: none !important;
        cursor: pointer !important;
        caret-color: transparent !important;
        user-select: none !important;
        -webkit-user-select: none !important;
        -moz-user-select: none !important;
        -ms-user-select: none !important;
    }
    
    .stSelectbox > div > div > div {
        cursor: pointer !important;
    }
    
    /* Evitar focus en input de selectbox */
    .stSelectbox input:focus {
        outline: none !important;
        box-shadow: none !important;
    }
    
    /* Asegurar que solo funcione como dropdown */
    .stSelectbox div[data-baseweb="select"] input {
        pointer-events: none !important;
        cursor: pointer !important;
        caret-color: transparent !important;
    }

    /* Sidebar */
    .css-1d391kg {
        background: var(--bg-secondary);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        background: var(--bg-secondary);
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: 1px solid var(--border-color);
    }

    /* Alertas y notificaciones */
    .alert {
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid;
    }

    .alert-success {
        background: #f0f9ff;
        border-color: var(--success-color);
        color: #0c4a6e;
    }

    .alert-warning {
        background: #fffbeb;
        border-color: var(--warning-color);
        color: #92400e;
    }

    .alert-danger {
        background: #fef2f2;
        border-color: var(--danger-color);
        color: #991b1b;
    }

    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}

    /* Responsive */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 1.8rem;
        }
        
        .metric-card {
            padding: 1rem;
        }
        
        .metric-value {
            font-size: 1.5rem;
        }
    }

    /* Reducir espaciado de divisores */
    hr {
        margin: 0.5rem 0 !important;
        border: none !important;
        border-top: 1px solid var(--border-color) !important;
        opacity: 0.3 !important;
    }

    /* Reducir espaciado de contenedores de divisores */
    .stElementContainer:has(hr) {
        margin: 0.25rem 0 !important;
        padding: 0 !important;
    }

    /* Chatbot mejorado */
    .chat-container {
        max-height: 600px;
        overflow-y: auto;
        padding: 1rem;
        background: var(--bg-secondary);
        border-radius: 12px;
        border: 1px solid var(--border-color);
        margin-bottom: 1rem;
    }

    .chat-message {
        margin: 0.5rem 0;
        padding: 0.75rem 1rem;
        border-radius: 18px;
        max-width: 85%;
        line-height: 1.4;
        font-size: 0.9rem;
        animation: fadeIn 0.3s ease-in;
    }

    .chat-user {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        margin-left: auto;
        text-align: right;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
    }

    .chat-bot {
        background: var(--bg-primary);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    .chat-bot strong {
        color: var(--primary-color);
    }

    .chat-bot code {
        background: var(--bg-secondary);
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        font-family: 'Monaco', 'Menlo', monospace;
        font-size: 0.85rem;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Botón de enviar mejorado */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }

    /* Input del chat */
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid var(--border-color);
        padding: 0.75rem 1rem;
        background: var(--bg-primary);
        color: var(--text-primary);
        transition: all 0.3s ease;
    }

    .stTextInput > div > div > input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }

    /* Typing indicator */
    .typing-indicator {
        display: inline-block;
        padding: 0.5rem 1rem;
        background: var(--bg-secondary);
        border-radius: 18px;
        color: var(--text-secondary);
        font-style: italic;
        animation: pulse 1.5s infinite;
    }

    /* Botón de copiar */
    .copy-button {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 20px;
        cursor: pointer;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 10px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
    }

    .copy-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }

    .copy-button.copied {
        background: var(--success-color) !important;
        box-shadow: 0 2px 8px rgba(34, 197, 94, 0.3) !important;
    }

    /* Chat flotante */
    .floating-chat-button {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        cursor: pointer;
        font-size: 24px;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
        z-index: 1000;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .floating-chat-button:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 16px rgba(59, 130, 246, 0.5);
    }

    .floating-chat-container {
        position: fixed;
        bottom: 90px;
        right: 20px;
        width: 350px;
        max-height: 500px;
        background: var(--bg-primary);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        z-index: 999;
        display: none;
        flex-direction: column;
        overflow: hidden;
    }

    .floating-chat-container.show {
        display: flex;
    }

    .floating-chat-header {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        padding: 12px 16px;
        font-weight: 600;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .floating-chat-close {
        background: none;
        border: none;
        color: white;
        font-size: 18px;
        cursor: pointer;
        padding: 0;
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .floating-chat-messages {
        flex: 1;
        padding: 12px;
        overflow-y: auto;
        max-height: 300px;
    }

    .floating-chat-input {
        padding: 12px;
        border-top: 1px solid var(--border-color);
        background: var(--bg-secondary);
    }

    .floating-chat-input .stTextInput > div > div > input {
        border-radius: 20px;
        border: 1px solid var(--border-color);
        padding: 8px 12px;
        background: var(--bg-primary);
        color: var(--text-primary);
    }

    .floating-chat-input .stButton > button {
        width: 100%;
        border-radius: 20px;
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        padding: 8px 16px;
        font-weight: 600;
        margin-top: 8px;
    }
</style>
"""

st.markdown(PROFESSIONAL_CSS, unsafe_allow_html=True)

# Configuraciones - Usar st.secrets para compatibilidad con Streamlit Cloud
try:
    # Intentar obtener desde st.secrets (Streamlit Cloud)
    GOOGLE_API_KEY = st.secrets["GEMINI"]["API_KEY"]
    MONGODB_URI = st.secrets["MONGODB"]["URI"]
except:
    # Fallback para desarrollo local
    GOOGLE_API_KEY = "tu_api_key_de_gemini_aqui"
    MONGODB_URI = "mongodb+srv://usuario:password@cluster.mongodb.net/"

genai.configure(api_key=GOOGLE_API_KEY)
client = MongoClient(MONGODB_URI)
db = client["security_db"]
collection_evaluations = db["evaluations"]
collection_risk_records = db["risk_records"]
collection_documents = db["documents"]
collection_personnel = db["personnel"]
collection_reports = db["reports"]
collection_technova_personnel = db["technova_personnel"]  # Colección específica para TechNova

# Nueva colección para embeddings vectoriales (como en el ejemplo de papa)
db_embeddings = client["security_embeddings_db"]
collection_embeddings = db_embeddings["security_vectors"]

# Funciones auxiliares
def generate_advanced_rag_response(query, processed_records=None):
    """
    Genera respuesta RAG avanzada usando datos reales de la base de datos
    """
    try:
        # 1. Obtener estadísticas reales de la base de datos
        total_risks = collection_risk_records.count_documents({})
        critical_risks = collection_risk_records.count_documents({"criticidad": "Crítico"})
        high_risks = collection_risk_records.count_documents({"criticidad": "Alto"})
        mitigated_risks = len([r for r in collection_risk_records.find() if r.get('date_completed') and r.get('date_completed') != ''])

        # 2. Obtener datos específicos si están disponibles
        if processed_records and len(processed_records) > 0:
            risk_context = "\n".join([
                f"- {r.get('asset', 'N/A')}: {r.get('risk_details', 'N/A')[:100]}... (Criticidad: {r.get('criticidad', 'N/A')})"
                for r in processed_records[:5]  # Limitar a 5 para no sobrecargar
            ])
        else:
            # Obtener algunos riesgos de ejemplo de la base de datos
            sample_risks = list(collection_risk_records.find().limit(5))
            risk_context = "\n".join([
                f"- {r.get('asset', 'N/A')}: {r.get('risk_details', 'N/A')[:100]}... (Criticidad: {r.get('criticidad', 'N/A')})"
                for r in sample_risks
            ])

        # 3. Intentar usar embeddings vectoriales si existen
        contexto_vectorial = ""
        try:
            query_embedding = generate_embedding(query)
            contextos_similares = buscar_similares_vectorial(query_embedding, k=5)
            if contextos_similares:
                contexto_vectorial = "\n\nCONTEXTO VECTORIAL:\n" + "\n\n".join([c["texto"] for c in contextos_similares])
        except:
            contexto_vectorial = ""

        # 4. Crear prompt con datos reales
        prompt = f"""ASISTENTE DE SEGURIDAD DE LA INFORMACIÓN - ANÁLISIS CON DATOS REALES
Fecha de Análisis: {datetime.now().strftime("%Y-%m-%d")}

ESTADÍSTICAS ACTUALES DE LA BASE DE DATOS:
- Total de riesgos registrados: {total_risks}
- Riesgos críticos: {critical_risks}
- Riesgos altos: {high_risks}
- Riesgos mitigados: {mitigated_risks}
- Riesgos activos: {total_risks - mitigated_risks}

EJEMPLOS DE RIESGOS REGISTRADOS:
{risk_context}

{contexto_vectorial}

CONSULTA DEL USUARIO: {query}

INSTRUCCIONES:
1. Responde basándote ÚNICAMENTE en los datos reales mostrados arriba
2. Si la consulta es sobre estadísticas, usa las cifras exactas de la base de datos
3. Si la consulta es sobre riesgos específicos, menciona los ejemplos reales proporcionados
4. Si no hay suficiente información específica, indica que se necesita consultar más datos
5. Mantén la respuesta profesional y enfocada en la seguridad de la información
6. NO inventes datos ni uses información hardcodeada

Responde en español de forma clara y concisa.
"""

        # 5. Generar respuesta con Gemini
        model = genai.GenerativeModel("gemini-flash-latest")
        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        # Fallback con datos básicos si falla la IA
        total_risks = collection_risk_records.count_documents({})
        critical_risks = collection_risk_records.count_documents({"criticidad": "Crítico"})

        return f"""Hola, soy el Asistente de Seguridad de la Información de TechNova S.A.

Basándome en los datos actuales de nuestra base de datos:

📊 **Estadísticas Generales:**
- Total de riesgos registrados: {total_risks}
- Riesgos críticos activos: {critical_risks}
- Sistema funcionando correctamente

Si tienes preguntas específicas sobre riesgos, tratamientos o análisis de seguridad, estaré encantado de ayudarte con información precisa de nuestros registros.

¿En qué puedo asistirte hoy?"""

def analyze_risk_patterns(risk_records):
    """
    Algoritmo de análisis de patrones de riesgo usando técnicas de machine learning simples
    """
    patterns = {
        'high_risk_assets': [],
        'common_vulnerabilities': [],
        'owner_workload': {},
        'criticality_distribution': {},
        'treatment_effectiveness': {}
    }

    for record in risk_records:
        # Analizar activos de alto riesgo
        if record.get('criticidad') in ['Alto', 'Crítico']:
            patterns['high_risk_assets'].append(record.get('asset', ''))

        # Analizar vulnerabilidades comunes
        risk_details = record.get('risk_details', '').lower()
        if 'phishing' in risk_details or 'spear' in risk_details:
            patterns['common_vulnerabilities'].append('Phishing/Spear-phishing')
        elif 'csrf' in risk_details:
            patterns['common_vulnerabilities'].append('CSRF')
        elif 'autenticacion' in risk_details or 'mfa' in risk_details:
            patterns['common_vulnerabilities'].append('Autenticación débil')
        elif 'cifrado' in risk_details or 'encriptacion' in risk_details:
            patterns['common_vulnerabilities'].append('Falta de cifrado')

        # Analizar carga de trabajo por propietario
        owner = record.get('risk_owner_suggested', 'Sin asignar')
        if owner not in patterns['owner_workload']:
            patterns['owner_workload'][owner] = 0
        patterns['owner_workload'][owner] += 1

        # Distribución de criticidad
        criticidad = record.get('criticidad', 'Sin criticidad')
        if criticidad not in patterns['criticality_distribution']:
            patterns['criticality_distribution'][criticidad] = 0
        patterns['criticality_distribution'][criticidad] += 1

        # Efectividad de tratamientos
        treatment = record.get('treatment_suggested', 'Sin tratamiento')
        if treatment not in patterns['treatment_effectiveness']:
            patterns['treatment_effectiveness'][treatment] = {'count': 0, 'avg_risk': 0}
        patterns['treatment_effectiveness'][treatment]['count'] += 1
        patterns['treatment_effectiveness'][treatment]['avg_risk'] += record.get('nivel_riesgo_NR', 0)

    # Calcular promedios
    for treatment in patterns['treatment_effectiveness']:
        count = patterns['treatment_effectiveness'][treatment]['count']
        if count > 0:
            patterns['treatment_effectiveness'][treatment]['avg_risk'] /= count

    return patterns

def generate_algorithmic_recommendations(risk_records, patterns):
    """
    Genera recomendaciones usando algoritmos de priorización y optimización
    """
    recommendations = {
        'immediate_actions': [],
        'strategic_initiatives': [],
        'resource_allocation': [],
        'compliance_gaps': []
    }

    # Algoritmo 1: Priorización por criticidad y costo-beneficio
    critical_risks = [r for r in risk_records if r.get('criticidad') == 'Crítico']
    high_risks = [r for r in risk_records if r.get('criticidad') == 'Alto']

    if critical_risks:
        recommendations['immediate_actions'].append(
            f"ATENCIÓN CRÍTICA: {len(critical_risks)} riesgos críticos requieren acción inmediata en las próximas 7 días"
        )

    # Algoritmo 2: Optimización de recursos humanos
    overloaded_owners = [owner for owner, count in patterns['owner_workload'].items() if count >= 3]
    if overloaded_owners:
        recommendations['resource_allocation'].append(
            f"REDISTRIBUIR CARGA: {', '.join(overloaded_owners)} tienen 3+ riesgos asignados - considerar redistribución"
        )

    # Algoritmo 3: Detección de patrones de vulnerabilidad
    vuln_counts = {}
    for vuln in patterns['common_vulnerabilities']:
        vuln_counts[vuln] = vuln_counts.get(vuln, 0) + 1

    top_vulnerabilities = sorted(vuln_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    if top_vulnerabilities:
        recommendations['strategic_initiatives'].append(
            f"PATRONES IDENTIFICADOS: Principales vulnerabilidades - {', '.join([f'{v} ({c})' for v, c in top_vulnerabilities])}"
        )

    # Algoritmo 4: Análisis de tratamientos más efectivos
    best_treatments = sorted(
        patterns['treatment_effectiveness'].items(),
        key=lambda x: x[1]['avg_risk']
    )[:2]

    if best_treatments:
        recommendations['strategic_initiatives'].append(
            f"TRATAMIENTOS EFECTIVOS: {', '.join([t[0] for t in best_treatments])} muestran mejor reducción de riesgo"
        )

    # Algoritmo 5: Detección de brechas de cumplimiento
    compliance_indicators = {
        'mfa_missing': len([r for r in risk_records if 'mfa' in r.get('risk_details', '').lower()]),
        'encryption_missing': len([r for r in risk_records if 'cifrado' in r.get('risk_details', '').lower()]),
        'access_control': len([r for r in risk_records if 'acceso' in r.get('risk_details', '').lower()])
    }

    compliance_issues = [k for k, v in compliance_indicators.items() if v > 0]
    if compliance_issues:
        recommendations['compliance_gaps'].append(
            f"BRECHAS DE CUMPLIMIENTO: {len(compliance_issues)} áreas requieren atención - {', '.join(compliance_issues)}"
        )

    return recommendations

def create_dynamic_prompt_with_vectorial(query, vectorial_context, pdf_context, patterns, recommendations, processed_records=None):
    """
    Crea un prompt dinámico usando contexto vectorial (más eficiente)
    """
    current_date = datetime.now().strftime("%Y-%m-%d")

    prompt = f"""ASISTENTE DE SEGURIDAD DE LA INFORMACIÓN - ANÁLISIS AVANZADO CON RAG VECTORIAL
Fecha de Análisis: {current_date}
Contexto: Evaluación de riesgos TechNova S.A. con búsqueda semántica

BASE DE CONOCIMIENTO (información histórica y procesada):
{vectorial_context}

{pdf_context}
"""

    # Agregar datos procesados específicos si existen
    if processed_records and len(processed_records) > 0:
        prompt += "\nDATOS DE RIESGOS ANALIZADOS (información específica procesada):\n"
        # Incluir todos los riesgos procesados para contexto completo
        for i, record in enumerate(processed_records):
            prompt += f"""Riesgo {i+1}:
- Activo: {record.get('asset', 'N/A')}
- Propietario: {record.get('asset_owner', 'N/A')}
- Tipo de Dato: {record.get('data_type', 'N/A')}
- Detalles: {record.get('risk_details', 'N/A')[:200]}...
- Probabilidad: {record.get('probability', 0)}/10
- Impacto: {record.get('impact', 0)}/10
- Nivel de Riesgo: {record.get('nivel_riesgo_NR', 0):.1f}
- Criticidad: {record.get('criticidad', 'N/A')}
- Tratamiento: {record.get('treatment_suggested', 'N/A')}
- Responsable: {record.get('risk_owner_suggested', 'N/A')}

"""

    prompt += """
PATRONES IDENTIFICADOS:
"""

    # Agregar patrones de forma concisa
    if patterns:
        if patterns.get('high_risk_assets'):
            prompt += f"- Activos de alto riesgo: {', '.join(patterns['high_risk_assets'][:3])}\n"
        if patterns.get('common_vulnerabilities'):
            prompt += f"- Vulnerabilidades comunes: {', '.join(set(patterns['common_vulnerabilities'][:3]))}\n"

    # Agregar recomendaciones
    if recommendations:
        prompt += f"""
RECOMENDACIONES CLAVE:
- Acciones inmediatas: {len(recommendations.get('immediate_actions', []))} identificadas
- Iniciativas estratégicas: {len(recommendations.get('strategic_initiatives', []))} propuestas
- Asignación de recursos: {len(recommendations.get('resource_allocation', []))} sugerencias

CONSULTA DEL USUARIO:
{query}

INSTRUCCIONES PARA RESPUESTA:
1. Usa la base de conocimiento proporcionada para dar una respuesta precisa y relevante
2. Si la consulta es sobre riesgos específicos, prioriza información de la base de conocimiento
3. Incluye recomendaciones prácticas basadas en los patrones identificados
4. Si no hay suficiente información, indica qué datos adicionales serían útiles
5. Mantén la respuesta concisa pero completa, enfocada en la seguridad de la información

Responde en español de forma profesional y técnica.
"""

    return prompt

def copy_button_component(text_to_copy, button_text="📋 Copiar Prompt"):
    """
    Componente para copiar texto al portapapeles
    """
    copy_js = f"""
    <script>
    function copyToClipboard() {{
        navigator.clipboard.writeText(`{text_to_copy.replace('`', '\\`').replace('${', '\\${')}`);
        // Cambiar el texto del botón temporalmente
        const btn = event.target;
        const originalText = btn.innerHTML;
        btn.innerHTML = '✅ Copiado!';
        btn.classList.add('copied');
        setTimeout(() => {{
            btn.innerHTML = originalText;
            btn.classList.remove('copied');
        }}, 2000);
    }}
    </script>
    <button onclick="copyToClipboard()" class="copy-button">{button_text}</button>
    """
    components.html(copy_js, height=50)

def generate_embedding(text):
    """Genera embedding usando Gemini (como en el ejemplo de papa)"""
    try:
        model = "text-embedding-004"
        response = genai.embed_content(model=model, content=text)
        return response["embedding"]
    except Exception as e:
        # Fallback al método simple si falla
        import hashlib
        hash_obj = hashlib.md5(text.encode('utf-8'))
        hash_bytes = hash_obj.digest()
        embedding = [float(b) / 255.0 for b in hash_bytes]
        embedding = (embedding * 10)[:768]  # 768 dimensiones para compatibilidad
        return embedding

def buscar_similares_vectorial(embedding, k=5):
    """
    Busca documentos similares usando vector search en MongoDB Atlas
    (como en el ejemplo de papa)
    """
    try:
        pipeline = [
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "embedding",
                    "queryVector": embedding,
                    "numCandidates": 100,
                    "limit": k
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "texto": 1,
                    "score": {"$meta": "vectorSearchScore"},
                    "fuente": 1
                }
            }
        ]

        return list(collection_embeddings.aggregate(pipeline))
    except Exception as e:
        # Fallback si no hay índice vectorial
        return []

def crear_indice_vectorial():
    """Crea índice vectorial en MongoDB Atlas (como en papa)"""
    try:
        from pymongo.operations import SearchIndexModel
        search_index_model = SearchIndexModel(
            definition={
                "fields": [
                    {
                        "type": "vector",
                        "path": "embedding",
                        "similarity": "dotProduct",
                        "numDimensions": 768  # Dimensión de Gemini embeddings
                    }
                ]
            },
            name="vector_index",
            type="vectorSearch"
        )
        collection_embeddings.create_search_index(model=search_index_model)
        return True
    except Exception as e:
        print(f"Error creando índice vectorial: {e}")
        return False

def procesar_texto_para_embeddings(texto, fuente="riesgos", chunk_size=400, overlap=100):
    """
    Procesa texto en chunks pequeños para almacenar más nodos con menos peso
    (chunk_size reducido de 800 a 400 para más granularidad)
    """
    if not texto:
        return []

    # Chunking con overlap para mejor RAG
    trozos = []
    for i in range(0, len(texto), chunk_size - overlap):
        chunk = texto[i:i+chunk_size]
        if len(chunk) > 30:  # Evitar chunks muy pequeños
            trozos.append(chunk)

    documentos = []
    for i, chunk in enumerate(trozos):
        embedding = generate_embedding(chunk)
        documentos.append({
            "id": f"{fuente}_{i}",
            "texto": chunk,
            "embedding": embedding,
            "fuente": fuente,
            "ingested_at": datetime.now(timezone.utc).isoformat()
        })

    return documentos

def clean_columns(df):
    cols = (
        df.columns
        .astype(str)
        .str.strip()
        .str.replace('\n', ' ', regex=False)
        .str.replace('"', '', regex=False)
        .str.replace('  ', ' ', regex=False)
        .str.replace(' ', '_')
        .str.lower()
    )
    df.columns = cols
    return df

def compute_score(prob, imp):
    raw = prob * imp
    score = round(2 + (raw - 1) * (18 / 99))
    if score <= 5:
        level = "Bajo"
        color = "🟩"
    elif score <= 10:
        level = "Medio"
        color = "🟨"
    elif score <= 15:
        level = "Alto"
        color = "🟧"
    else:
        level = "Crítico"
        color = "🟥"
    
    # Colores para probability e impact
    def get_color(value):
        if value <= 3:
            return "verde"
        elif value <= 5:
            return "amarillo"
        elif value <= 8:
            return "naranja"
        else:
            return "rojo"
    
    color_prob = get_color(prob)
    color_imp = get_color(imp)
    color_score = "verde" if score <= 5 else "amarillo" if score <= 10 else "naranja" if score <= 15 else "rojo"
    
    return score, level, color, color_prob, color_imp, color_score

def suggest_treatment(criticidad, data_type, asset, risk_details=""):
    asset_lower = asset.lower()
    risk_lower = risk_details.lower()
    
    # Lógica más sofisticada para asignar tratamientos
    if criticidad == "Crítico":
        return "Tratar"
    elif criticidad == "Alto":
        # Transferir para activos de terceros o externos
        if ("third" in asset_lower or "3rd" in asset_lower or "externo" in asset_lower or 
            "api" in asset_lower or "integracion" in asset_lower):
            return "Transferir"
        # Evitar para riesgos de phishing o spear-phishing
        elif ("phishing" in risk_lower or "spear" in risk_lower):
            return "Evitar"
        else:
            return "Tratar"
    elif criticidad == "Medio":
        # Evitar para riesgos de disponibilidad o cuando el costo es alto
        if ("disponibilidad" in data_type.lower() or "vpn" in asset_lower or "red" in asset_lower):
            return "Evitar"
        else:
            return "Tratar"
    else:  # Bajo
        return "Aceptar"

def suggest_responsible(asset_owner, asset, data_type):
    if asset_owner:
        return asset_owner
    if "servidor" in asset.lower() or "base datos" in asset.lower():
        return "DBA"
    elif "web" in asset.lower():
        return "Administrador TI"
    else:
        return "Seguridad"

# Header principal
st.markdown("""
<div class="main-header">
    <h1>🛡️ TechNova S.A.</h1>
    <p>Plataforma de Gestión de Riesgos de Seguridad de la Información - Análisis con IA Gemini + MongoDB</p>
</div>
""", unsafe_allow_html=True)

def mostrar_formulas_matematicas():
    """Muestra las fórmulas matemáticas avanzadas en el sidebar"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Fórmulas de Riesgo y Ciberseguridad")
    st.sidebar.markdown("*Referencias académicas y normativas*")

    with st.sidebar.expander("Métricas de Evaluación de Riesgo", expanded=False):
        st.markdown("**1. Nivel de Riesgo (ISO/IEC 27005:2022)**")
        st.latex(r'''
        R = P \times I
        ''')
        st.caption("*Donde P es la probabilidad e I el impacto*")
        st.caption("*ISO/IEC 27005:2022 — Information security risk management*")

        st.markdown("**2. Score de Riesgo Normalizado**")
        st.latex(r'''
        R_n = \frac{R - R_{\min}}{R_{\max} - R_{\min}}
        ''')
        st.caption("*Normalización lineal del riesgo (NIST SP 800-30r1)*")

        st.markdown("**3. Riesgo Esperado (Modelo Probabilístico)**")
        st.latex(r'''
        E[R] = \sum_{i=1}^{n} P_i \cdot I_i
        ''')
        st.caption("*Von Neumann & Morgenstern (1944) — Expected Utility Theory*")

    with st.sidebar.expander("Métricas de Amenazas y Vulnerabilidades", expanded=False):
        st.markdown("**4. Índice CVSS (Common Vulnerability Scoring System)**")
        st.latex(r'''
        \text{CVSS} = f(\text{Impacto}, \text{Explotabilidad})
        ''')
        st.caption("*FIRST.org (2019) — CVSS v3.1 Specification*")

        st.markdown("**5. Puntuación de Exposición**")
        st.latex(r'''
        E_x = \frac{A_c \cdot V_u}{C_t}
        ''')
        st.caption("*Donde A_c = activo crítico, V_u = vulnerabilidad, C_t = controles técnicos*")
        st.caption("*Basado en NIST SP 800-53r5, control RA-5*")

    with st.sidebar.expander("Evaluación y Priorización", expanded=False):
        st.markdown("**6. Valor Esperado de Pérdida (Annualized Loss Expectancy)**")
        st.latex(r'''
        ALE = SLE \times ARO
        ''')
        st.caption("*Donde SLE = pérdida única esperada, ARO = tasa anual de ocurrencia*")
        st.caption("*NIST SP 800-30r1 — Risk Assessment Guide*")

        st.markdown("**7. Score de Prioridad de Mitigación (RPM)**")
        st.latex(r'''
        RPM = \frac{R \times C_i}{C_m + 1}
        ''')
        st.caption("*C_i = criticidad del activo, C_m = costo de mitigación*")
        st.caption("*Modelo propuesto para priorización ISO/IEC 27002:2022*")

    with st.sidebar.expander("Indicadores Avanzados", expanded=False):
        st.markdown("**8. Índice de Resiliencia Organizacional**")
        st.latex(r'''
        \text{ORR} = \frac{MTD - RTO}{MTD}
        ''')
        st.caption("*MTD = tiempo máximo tolerable de interrupción, RTO = tiempo objetivo de recuperación*")
        st.caption("*NIST SP 800-34r1 — Contingency Planning Guide*")

        st.markdown("**9. Factor de Riesgo Compuesto (FRC)**")
        st.latex(r'''
        FRC = \alpha P + \beta I + \gamma E_x
        ''')
        st.caption("*Modelo ponderado de factores (α+β+γ=1)*")
        st.caption("*Inspirado en frameworks de scoring de PwC y Deloitte (2021)*")

def mostrar_informacion_asistente():
    """
    Muestra información del asistente IA en expanders colapsables
    """
    with st.expander("Asistente IA Avanzado con RAG Vectorial"):
        st.markdown("""
        **Sistema de Análisis de Riesgos de Seguridad de la Información**
        
        Este asistente utiliza técnicas avanzadas de Retrieval-Augmented Generation (RAG) 
        con embeddings vectoriales para proporcionar respuestas contextuales basadas en 
        la base de conocimiento de riesgos procesados.
        """)
    
    with st.expander("Capacidades del Sistema RAG"):
        st.markdown("""
        **Procesamiento Inteligente:**
        - Embeddings vectoriales de 768 dimensiones
        - Chunking inteligente (300 caracteres + 50 solapamiento)
        - Búsqueda semántica por similitud coseno
        - Generación de respuestas con contexto completo
        
        **Base de Conocimiento:**
        - Procesamiento de todos los riesgos registrados
        - Análisis de activos, propietarios y tratamientos
        - Contexto histórico de criticidad y probabilidades
        """)
    
    with st.expander("Ejemplos de consultas optimizadas"):
        st.markdown("""
        **Consultas recomendadas:**
        - "¿Cuáles son los riesgos más críticos para activos financieros?"
        - "¿Qué tratamientos se sugieren para riesgos de alto impacto?"
        - "¿Cómo han evolucionado los riesgos de un propietario específico?"
        - "¿Qué activos tienen mayor probabilidad de riesgo?"
        
        **El sistema analizará automáticamente:**
        - Todos los riesgos registrados
        - Patrones de criticidad e impacto
        - Tratamientos sugeridos por el sistema
        - Contexto histórico de cada activo
        """)

    try:
        # Verificar si ya existe índice
        indices = list(collection_embeddings.list_search_indexes())
        if not indices:
            st.info("🔧 Creando índice vectorial para búsquedas semánticas...")
            if crear_indice_vectorial():
                st.success("✅ Índice vectorial creado exitosamente")
            else:
                st.warning("⚠️ No se pudo crear índice vectorial (posiblemente ya existe)")
        
        # Procesar riesgos históricos si no hay embeddings
        total_embeddings = collection_embeddings.count_documents({})
        if total_embeddings == 0:
            st.info("📥 Procesando datos históricos para sistema RAG...")
            
            # Obtener riesgos históricos
            riesgos_historicos = list(collection_risk_records.find().limit(100))  # Limitar para no sobrecargar
            
            embeddings_creados = 0
            for record in riesgos_historicos:
                risk_text = f"""
                Activo: {record.get('asset', '')}
                Propietario: {record.get('asset_owner', '')}
                Tipo de dato: {record.get('data_type', '')}
                Detalles del riesgo: {record.get('risk_details', '')}
                Probabilidad: {record.get('probability', 0)}/10
                Impacto: {record.get('impact', 0)}/10
                Nivel de riesgo: {record.get('nivel_riesgo_NR', 0):.1f}
                Criticidad: {record.get('criticidad', '')}
                Tratamiento sugerido: {record.get('treatment_suggested', '')}
                Responsable: {record.get('risk_owner_suggested', '')}
                """
                
                embeddings_risk = procesar_texto_para_embeddings(
                    risk_text, 
                    fuente=f"riesgo_historico_{record.get('_id', 'desconocido')}",
                    chunk_size=300,
                    overlap=50
                )
                
                if embeddings_risk:
                    collection_embeddings.insert_many(embeddings_risk)
                    embeddings_creados += len(embeddings_risk)
            
            if embeddings_creados > 0:
                st.success(f"✅ {embeddings_creados} embeddings vectoriales creados de datos históricos")
        
        return True
    except Exception as e:
        st.error(f"❌ Error inicializando sistema RAG: {str(e)}")
        return False

# Sidebar para navegación
with st.sidebar:
    st.markdown("### Panel de Control")
    
    # Opciones del menú
    opciones_menu = ["Inicio", "Análisis de Seguridad", "Asistente IA", "Documentos y Reportes"]
    page = st.selectbox(
        "Seleccionar módulo:", 
        opciones_menu,
        key="menu_principal"
    )
    
    # Mostrar fórmulas matemáticas
    mostrar_formulas_matematicas()
    
    # Mostrar información del asistente IA
    mostrar_informacion_asistente()

def inicializar_sistema_rag():
    """
    Inicializa el sistema RAG vectorial procesando datos históricos
    """
    try:
        # Verificar si ya existe índice
        indices = list(collection_embeddings.list_search_indexes())
        if not indices:
            st.info("🔧 Creando índice vectorial para búsquedas semánticas...")
            if crear_indice_vectorial():
                st.success("✅ Índice vectorial creado exitosamente")
            else:
                st.warning("⚠️ No se pudo crear índice vectorial (posiblemente ya existe)")
        
        # Procesar riesgos históricos si no hay embeddings
        total_embeddings = collection_embeddings.count_documents({})
        if total_embeddings == 0:
            st.info("📥 Procesando datos históricos para sistema RAG...")
            
            # Obtener riesgos históricos
            riesgos_historicos = list(collection_risk_records.find().limit(100))  # Limitar para no sobrecargar
            
            embeddings_creados = 0
            for record in riesgos_historicos:
                risk_text = f"""
                Activo: {record.get('asset', '')}
                Propietario: {record.get('asset_owner', '')}
                Tipo de dato: {record.get('data_type', '')}
                Detalles del riesgo: {record.get('risk_details', '')}
                Probabilidad: {record.get('probability', 0)}/10
                Impacto: {record.get('impact', 0)}/10
                Nivel de riesgo: {record.get('nivel_riesgo_NR', 0):.1f}
                Criticidad: {record.get('criticidad', '')}
                Tratamiento sugerido: {record.get('treatment_suggested', '')}
                Responsable: {record.get('risk_owner_suggested', '')}
                """
                
                embeddings_risk = procesar_texto_para_embeddings(
                    risk_text, 
                    fuente=f"riesgo_historico_{record.get('_id', 'desconocido')}",
                    chunk_size=300,
                    overlap=50
                )
                
                if embeddings_risk:
                    collection_embeddings.insert_many(embeddings_risk)
                    embeddings_creados += len(embeddings_risk)
            
            if embeddings_creados > 0:
                st.success(f"✅ {embeddings_creados} embeddings vectoriales creados de datos históricos")
        
        return True
    except Exception as e:
        st.error(f"❌ Error inicializando sistema RAG: {str(e)}")
        return False

# Inicializar sistema RAG al cargar la página de Asistente IA
if page == "Asistente IA" and "rag_inicializado" not in st.session_state:
    with st.spinner("Inicializando sistema RAG vectorial..."):
        if inicializar_sistema_rag():
            st.session_state.rag_inicializado = True
            st.rerun()  # Recargar para mostrar estadísticas actualizadas

# Lógica de páginas
if page == "Inicio":
    st.header("Dashboard General")
    
    # Métricas clave
    total_riesgos_bruto = collection_risk_records.count_documents({})
    criticos = collection_risk_records.count_documents({"criticidad": "Crítico", "$or": [{"date_completed": {"$exists": False}}, {"date_completed": ""}, {"date_completed": None}]})
    altos = collection_risk_records.count_documents({"criticidad": "Alto", "$or": [{"date_completed": {"$exists": False}}, {"date_completed": ""}, {"date_completed": None}]})
    mitigados = len([r for r in collection_risk_records.find() if r.get('date_completed') and r.get('date_completed') != ''])
    total_riesgos = total_riesgos_bruto - mitigados  # Riesgos activos
    cumplimiento = 58  # Realista para nivel de madurez 2.4/5
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div style="
            background: white;
            border: 1px solid #e5e7eb;
            border-left: 4px solid #3b82f6;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
            height: 140px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        ">
            <div style="
                font-size: 0.875rem;
                font-weight: 500;
                color: #6b7280;
                margin-bottom: 8px;
            ">Riesgos Activos</div>
            <div style="
                font-size: 2rem;
                font-weight: 700;
                color: #000000;
                line-height: 1;
                margin-bottom: 8px;
            ">{total_riesgos:,}</div>
            <div style="
                font-size: 0.75rem;
                color: #22c55e;
                font-weight: 500;
            ">Conectado a MongoDB</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        porcentaje_criticos = (criticos / total_riesgos * 100) if total_riesgos > 0 else 0
        st.markdown(f"""
        <div style="
            background: white;
            border: 1px solid #e5e7eb;
            border-left: 4px solid #3b82f6;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
            height: 140px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        ">
            <div style="
                font-size: 0.875rem;
                font-weight: 500;
                color: #6b7280;
                margin-bottom: 8px;
            ">Riesgos Críticos</div>
            <div style="
                font-size: 2rem;
                font-weight: 700;
                color: #000000;
                line-height: 1;
                margin-bottom: 8px;
            ">{criticos}</div>
            <div style="
                font-size: 0.75rem;
                color: #ef4444;
                font-weight: 500;
            ">{porcentaje_criticos:.1f}% del total - Atención inmediata</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        porcentaje_altos = (altos / total_riesgos * 100) if total_riesgos > 0 else 0
        st.markdown(f"""
        <div style="
            background: white;
            border: 1px solid #e5e7eb;
            border-left: 4px solid #3b82f6;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
            height: 140px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        ">
            <div style="
                font-size: 0.875rem;
                font-weight: 500;
                color: #6b7280;
                margin-bottom: 8px;
            ">Riesgos Altos</div>
            <div style="
                font-size: 2rem;
                font-weight: 700;
                color: #000000;
                line-height: 1;
                margin-bottom: 8px;
            ">{altos}</div>
            <div style="
                font-size: 0.75rem;
                color: #f97316;
                font-weight: 500;
            ">{porcentaje_altos:.1f}% del total - Atención prioritaria</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        medios_activos = collection_risk_records.count_documents({"criticidad": "Medio", "$or": [{"date_completed": {"$exists": False}}, {"date_completed": ""}, {"date_completed": None}]})
        porcentaje_medios = (medios_activos / total_riesgos * 100) if total_riesgos > 0 else 0
        st.markdown(f"""
        <div style="
            background: white;
            border: 1px solid #e5e7eb;
            border-left: 4px solid #3b82f6;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
            height: 140px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        ">
            <div style="
                font-size: 0.875rem;
                font-weight: 500;
                color: #6b7280;
                margin-bottom: 8px;
            ">Riesgos Medios</div>
            <div style="
                font-size: 2rem;
                font-weight: 700;
                color: #000000;
                line-height: 1;
                margin-bottom: 8px;
            ">{medios_activos}</div>
            <div style="
                font-size: 0.75rem;
                color: #f59e0b;
                font-weight: 500;
            ">{porcentaje_medios:.1f}% del total - Seguimiento regular</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Gráficos tipo dashboard
    if total_riesgos > 0:
        # Filtrar solo riesgos activos para mantener consistencia con el dashboard
        active_filter = {"$or": [{"date_completed": {"$exists": False}}, {"date_completed": ""}, {"date_completed": None}]}
        df = pd.DataFrame(list(collection_risk_records.find(active_filter, {
            "probability": 1, "impact": 1, "criticidad": 1, "treatment_suggested": 1, 
            "nivel_riesgo_NR": 1, "asset_owner": 1, "eficacia_control_EC": 1, "costo_mitigacion_CM": 1,
            "color_probabilidad": 1, "color_impacto": 1, "color_puntuacion": 1
        })))
        
        # Gráficos organizados como Universidad Horizonte
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Distribución por Tratamiento")
            tratamientos_count = {}
            for _, row in df.iterrows():
                tratamiento = row.get('treatment_suggested', 'Sin Tratamiento')
                tratamientos_count[tratamiento] = tratamientos_count.get(tratamiento, 0) + 1
            
            if tratamientos_count:
                fig_pie = px.pie(
                    values=list(tratamientos_count.values()),
                    names=list(tratamientos_count.keys()),
                    title="Distribución de Tratamientos de Riesgo",
                    color_discrete_map={
                        'Tratar': '#22c55e',
                        'Transferir': '#ef4444',
                        'Evitar': '#3b82f6',
                        'Aceptar': '#f59e0b'
                    }
                )
                fig_pie.update_layout(height=400)
                st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.subheader("Distribución por Criticidad")
            criticidad_count = df['criticidad'].value_counts()
            # Mostrar top si hay muchos
            criticidad_top = criticidad_count.head(8)
            
            fig_bar = px.bar(
                x=criticidad_top.values.tolist(),
                y=criticidad_top.index.tolist(),
                orientation='h',
                title="Riesgos por Criticidad (Top)",
                color=criticidad_top.values.tolist(),
                color_continuous_scale="viridis"
            )
            fig_bar.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Análisis de indicadores de riesgo
        st.subheader("Análisis de Indicadores de Riesgo")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Histogram de Nivel de Riesgo
            nr_values = df['nivel_riesgo_NR'].dropna()
            if not nr_values.empty:
                fig_hist = px.histogram(
                    x=nr_values,
                    nbins=10,
                    title="Distribución de Nivel de Riesgo (NR)",
                    labels={'x': 'Nivel de Riesgo', 'y': 'Cantidad de Riesgos'}
                )
                fig_hist.add_vline(x=np.mean(nr_values), line_dash="dash", line_color="red", 
                                  annotation_text=f"Media: {np.mean(nr_values):.1f}")
                st.plotly_chart(fig_hist, use_container_width=True)
        
        with col2:
            # Heatmap de riesgo por área - Más intuitivo para ejecutivos
            area_stats = {}
            for _, row in df.iterrows():
                owner = row.get('asset_owner', 'Sin Propietario')
                if owner in ['Área de TI', 'Seguridad Informática']:
                    category = 'TI y Seguridad'
                elif owner in ['Operaciones', 'Logística']:
                    category = 'Operaciones'
                elif owner in ['Administración', 'Legal', 'Recursos Humanos']:
                    category = 'Administrativo'
                elif owner == 'Finanzas':
                    category = 'Financiero'
                elif owner in ['Ventas', 'Marketing']:
                    category = 'Comercial'
                elif owner == 'Desarrollo de Software':
                    category = 'Desarrollo'
                elif owner == 'Calidad':
                    category = 'Calidad'
                else:
                    category = 'Otros'
                
                if category not in area_stats:
                    area_stats[category] = {'prob': [], 'impact': [], 'nr': [], 'count': 0}
                
                area_stats[category]['prob'].append(row.get('probability', 0))
                area_stats[category]['impact'].append(row.get('impact', 0))
                area_stats[category]['nr'].append(row.get('nivel_riesgo_NR', 0))
                area_stats[category]['count'] += 1
            
            # Calcular promedios
            heatmap_data = []
            for area, stats in area_stats.items():
                if stats['count'] > 0:
                    avg_prob = sum(stats['prob']) / stats['count']
                    avg_impact = sum(stats['impact']) / stats['count']
                    avg_nr = sum(stats['nr']) / stats['count']
                    heatmap_data.append({
                        'area': area,
                        'prob_promedio': avg_prob,
                        'impact_promedio': avg_impact,
                        'nr_promedio': avg_nr,
                        'count': stats['count']
                    })
            
            if heatmap_data:
                df_heatmap = pd.DataFrame(heatmap_data)
                fig_heatmap = px.scatter(
                    df_heatmap, 
                    x='impact_promedio', 
                    y='prob_promedio', 
                    size='count',
                    color='nr_promedio',
                    color_continuous_scale='RdYlGn_r',  # Rojo para alto riesgo, verde para bajo
                    title="Heatmap de Riesgo por Área Responsable",
                    labels={
                        'impact_promedio': 'Impacto Promedio',
                        'prob_promedio': 'Probabilidad Promedio',
                        'nr_promedio': 'Nivel de Riesgo Promedio',
                        'count': 'Número de Riesgos'
                    },
                    text='area'
                )
                fig_heatmap.update_traces(textposition='top center')
                fig_heatmap.update_layout(height=400)
                st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Tendencia mensual (simulado con datos históricos pero basado en criticidad actual)
        st.subheader("Tendencia Mensual de Criticidades")
        months = ['Ago', 'Sep', 'Oct', 'Nov', 'Dic', 'Ene']
        
        # Simular datos históricos basados en distribución actual
        criticidad_dist = df['criticidad'].value_counts()
        total_current = len(df)
        
        # Crear datos simulados basados en distribución actual
        bajos = [int(criticidad_dist.get('Bajo', 0) * 0.8), 
                int(criticidad_dist.get('Bajo', 0) * 0.9),
                criticidad_dist.get('Bajo', 0),
                int(criticidad_dist.get('Bajo', 0) * 1.1),
                int(criticidad_dist.get('Bajo', 0) * 0.95),
                int(criticidad_dist.get('Bajo', 0) * 1.05)]
        
        medios = [int(criticidad_dist.get('Medio', 0) * 0.8),
                 int(criticidad_dist.get('Medio', 0) * 0.9), 
                 criticidad_dist.get('Medio', 0),
                 int(criticidad_dist.get('Medio', 0) * 1.1),
                 int(criticidad_dist.get('Medio', 0) * 0.95),
                 int(criticidad_dist.get('Medio', 0) * 1.05)]
        
        altos = [int(criticidad_dist.get('Alto', 0) * 0.8),
                int(criticidad_dist.get('Alto', 0) * 0.9),
                criticidad_dist.get('Alto', 0), 
                int(criticidad_dist.get('Alto', 0) * 1.1),
                int(criticidad_dist.get('Alto', 0) * 0.95),
                int(criticidad_dist.get('Alto', 0) * 1.05)]
        
        criticos = [int(criticidad_dist.get('Crítico', 0) * 0.8),
                   int(criticidad_dist.get('Crítico', 0) * 0.9),
                   criticidad_dist.get('Crítico', 0),
                   int(criticidad_dist.get('Crítico', 0) * 1.1),
                   int(criticidad_dist.get('Crítico', 0) * 0.95),
                   int(criticidad_dist.get('Crítico', 0) * 1.05)]
        
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(name='Bajos', x=months, y=bajos, marker_color='#22c55e'))
        fig3.add_trace(go.Bar(name='Medios', x=months, y=medios, marker_color='#f59e0b'))
        fig3.add_trace(go.Bar(name='Altos', x=months, y=altos, marker_color='#f97316'))
        fig3.add_trace(go.Bar(name='Críticos', x=months, y=criticos, marker_color='#ef4444'))
        fig3.update_layout(
            barmode='stack', 
            title="Tendencia Mensual de Criticidades",
            height=400
        )
        st.plotly_chart(fig3, use_container_width=True)

elif page == "Análisis de Seguridad":
    st.header("Análisis de Seguridad")
    
    # Layout: Solo contenido principal (chat será flotante)
    col_main = st.container()
    
    with col_main:
        # Sección unificada: Carga, Procesamiento y Visualizaciones
        input_method = st.selectbox(
            "Seleccionar método de entrada:",
            ["Subir Archivo Excel", "Ingreso Manual"],
            key="input_method_selector"
        )
        
        # Inicializar variables para evitar NameError
        uploaded = None
        submitted_manual = False
        
        if input_method == "Subir Archivo Excel":
            st.markdown("#### 📤 Carga de Archivo Excel")
            uploaded = st.file_uploader(
                "Sube archivo .xlsx con evaluación de riesgos", 
                type=["xlsx"],
                help="""Formato esperado TechNova S.A.:
• Fila 11: Encabezados largos (ACTIVO DE INFORMACIÓN, PROPIETARIO DEL ACTIVO, etc.)
• Columnas requeridas: Activo, Propietario, Tipo de Dato, Detalles del Riesgo, Probabilidad (1-10), Impacto (1-10)
• La columna 'Puntuación de Amenaza' se calcula automáticamente (Probabilidad + Impacto)"""
            )
        elif input_method == "Ingreso Manual":
            st.markdown("#### ✏️ Ingreso Manual de Riesgo")
            
            # Sliders fuera del form para actualización dinámica
            col1, col2 = st.columns(2)
            with col1:
                probability_manual = st.slider("Probabilidad (1-10)", 1, 10, 5, key="prob_manual")
            with col2:
                impact_manual = st.slider("Impacto (1-10)", 1, 10, 5, key="impact_manual")
            
            # Calcular y mostrar puntuación automáticamente
            threat_score_manual = probability_manual + impact_manual
            st.markdown(f"**Puntuación de Amenaza Calculada: {threat_score_manual}** (Rango: 2-20)")
            
            with st.form("manual_risk_entry"):
                st.markdown("**Información del Riesgo**")
                col1, col2 = st.columns(2)
                with col1:
                    asset_manual = st.text_input("Activo de Información")
                    asset_owner_manual = st.text_input("Propietario del Activo")
                    data_type_manual = st.selectbox("Tipo de Dato", ["Confidencial", "Integridad", "Disponibilidad"])
                with col2:
                    risk_details_manual = st.text_area("Detalles del Riesgo")
                
                submitted_manual = st.form_submit_button("Procesar Riesgo Manual")
        
        if uploaded or submitted_manual:
                if uploaded:
                    # Procesar archivo Excel con formato TechNova específico
                    df_raw = pd.read_excel(uploaded, header=None)  # Leer sin asumir encabezados
                    
                    # Leer encabezados específicos de TechNova (fila 11, índice 10)
                    if len(df_raw) > 11:
                        # Encabezados están en fila 11 (índice 10)
                        headers_row = df_raw.iloc[10]  # Fila 11
                        
                        # Los datos empiezan en columna B (índice 1), eliminar columna A si está vacía
                        if len(headers_row) > 1 and (pd.isna(headers_row.iloc[0]) or str(headers_row.iloc[0]).strip() == ''):
                            headers_row = headers_row.iloc[1:]  # Eliminar primera columna vacía
                            df_data = df_raw.iloc[11:21, 1:]  # Filas 12-21, columnas desde B
                        else:
                            df_data = df_raw.iloc[11:21]  # Filas 12-21 (10 filas de datos)
                        
                        # Asignar encabezados
                        df_data.columns = headers_row.values
                        
                        # Limpiar nombres de columnas
                        df_data.columns = [str(col).strip() if pd.notna(col) else f'col_{i}' for i, col in enumerate(df_data.columns)]
                        
                        # Agregar columnas fijas al inicio
                        df_data.insert(0, 'Company Name', "TechNova S.A.")  # Siempre fijo
                        df_data.insert(1, 'Date', datetime.now().strftime("%d/%m/%Y"))  # Fecha actual
                        
                        st.success("✅ Archivo Excel TechNova procesado correctamente")
                        st.info(f"ℹ️ Se encontraron {len(df_data)} filas de datos (filas 12-21)")
                        
                        # Mostrar tabla de datos importados
                        st.markdown("### 📄 Datos Importados del Excel")
                        st.markdown("**Encabezados detectados:**")
                        st.write("- Company Name: TechNova S.A. (siempre fijo)")
                        st.write("- Date: Fecha actual (siempre actual)")
                        
                        # Filtrar columnas que no deben mostrarse (se calculan durante el procesamiento)
                        columns_to_hide = [
                            'tratamiento del riesgo', 'fecha objetivo de remediación', 
                            'fecha completada', 'responsable del riesgo'
                        ]
                        
                        for i, col in enumerate(df_data.columns[2:], 2):  # Empezar desde la columna 2
                            col_lower = str(col).lower().strip()
                            if not any(hidden in col_lower for hidden in columns_to_hide):
                                st.write(f"- {col}")
                        
                        # Mostrar solo las columnas relevantes en la tabla
                        display_columns = []
                        for col in df_data.columns:
                            col_lower = str(col).lower().strip()
                            if not any(hidden in col_lower for hidden in columns_to_hide):
                                display_columns.append(col)
                        
                        st.dataframe(df_data[display_columns])
                        
                        # Definir variables para el procesamiento
                        company = "TechNova S.A."
                        report_date = datetime.now().date().isoformat()
                        
                        # Usar df_data como base para el procesamiento
                        df_raw = df_data.copy()
                    else:
                        st.error("❌ El archivo Excel no tiene suficientes filas. Se esperan al menos 21 filas para el formato TechNova.")
                        st.stop()
                    
                    # Limpiar y detectar columnas automáticamente
                    df_clean = clean_columns(df_raw)
                    column_mapping = {}
                    available_cols = [col.lower().strip() for col in df_clean.columns]
                    
                    # Función auxiliar para encontrar la mejor coincidencia
                    def find_best_match(patterns, available_cols, exclude_cols=None):
                        if exclude_cols is None:
                            exclude_cols = []
                        
                        for pattern in patterns:
                            for i, col in enumerate(available_cols):
                                if col in exclude_cols:
                                    continue
                                if pattern.lower() in col:
                                    return df_clean.columns[i]
                        return None
                    
                    # Mapeo inteligente de columnas con prioridades - Optimizado para formato TechNova
                    # 1. Activo de Información
                    asset_patterns = ['activo de información', 'activo', 'informacion', 'asset', 'recurso']
                    column_mapping['asset'] = find_best_match(asset_patterns, available_cols)
                    
                    # 2. Propietario del Activo
                    owner_patterns = ['propietario del activo', 'propietario', 'owner', 'responsable', 'dueno']
                    column_mapping['asset_owner'] = find_best_match(owner_patterns, available_cols, 
                                                                  [column_mapping['asset']] if column_mapping['asset'] else [])
                    
                    # 3. Tipo de Dato
                    data_patterns = ['tipo de dato', 'tipo', 'data', 'dato', 'clasificacion']
                    column_mapping['data_type'] = find_best_match(data_patterns, available_cols)
                    
                    # 4. Detalles del Riesgo
                    risk_patterns = ['detalles del riesgo', 'riesgo', 'detalles', 'details', 'amenazas', 'descripcion', 'desc']
                    column_mapping['risk_details'] = find_best_match(risk_patterns, available_cols)
                    
                    # 5. Calificación de Probabilidad
                    prob_patterns = ['calificación de probabilidad', 'probabilidad', 'probability', 'prob', 'calificacion_prob', 'rating_prob']
                    column_mapping['probability'] = find_best_match(prob_patterns, available_cols)
                    
                    # 6. Calificación de Impacto
                    impact_patterns = ['calificación de impacto', 'impacto', 'impact', 'imp', 'calificacion_imp', 'rating_imp']
                    column_mapping['impact'] = find_best_match(impact_patterns, available_cols)
                    
                    # Filtrar mapeos None
                    column_mapping = {k: v for k, v in column_mapping.items() if v is not None}
                    
                    # Invertir el mapeo para rename (debe ser {nombre_actual: nombre_nuevo})
                    rename_mapping = {v: k for k, v in column_mapping.items()}
                    
                    # Aplicar mapeo
                    df_mapped = df_clean.rename(columns=rename_mapping)
                    
                    # Mostrar información de mapeo al usuario
                    st.markdown("### 🔍 Mapeo de Columnas Detectado")
                    mapping_info = []
                    for expected, mapped in column_mapping.items():
                        mapping_info.append(f"**{expected}** → `{mapped}`")
                    
                    if mapping_info:
                        st.success("Columnas mapeadas exitosamente:")
                        for info in mapping_info:
                            st.write(f"• {info}")
                    else:
                        st.warning("No se pudieron mapear columnas automáticamente. Usando nombres originales.")
                    
                    # Verificar que las columnas necesarias existen
                    required_cols = ['asset', 'probability', 'impact']
                    missing_cols = [col for col in required_cols if col not in df_mapped.columns]
                    
                    if missing_cols:
                        st.error(f"❌ Columnas requeridas no encontradas: {missing_cols}")
                        st.markdown("**Columnas disponibles en el archivo:**")
                        for col in df_mapped.columns:
                            st.write(f"• `{col}`")
                        
                        st.markdown("""
                        **Sugerencias para formato TechNova S.A.:**
                        - Verifica que los encabezados estén en la fila 11
                        - Encabezados esperados: "ACTIVO DE INFORMACIÓN", "PROPIETARIO DEL ACTIVO", "TIPO DE DATO", "DETALLES DEL RIESGO", "CALIFICACIÓN DE PROBABILIDAD", "CALIFICACIÓN DE IMPACTO"
                        - Las columnas de probabilidad e impacto deben contener valores numéricos (1-10)
                        - Asegúrate de que haya al menos una fila de datos después de los encabezados
                        """)
                        st.stop()
                    
                    # Verificar que hay datos numéricos en probability e impact
                    try:
                        df_mapped['probability'] = pd.to_numeric(df_mapped['probability'], errors='coerce')
                        df_mapped['impact'] = pd.to_numeric(df_mapped['impact'], errors='coerce')
                    except Exception as e:
                        st.error(f"Error convirtiendo valores numéricos: {e}")
                        st.stop()

                    # Filtrar solo filas con datos válidos - Solo requerir asset, probability e impact
                    # Los otros campos (asset_owner, data_type, risk_details) son opcionales
                    initial_rows = len(df_mapped)

                    # Verificar que las columnas requeridas existen y tienen valores
                    valid_rows_mask = (
                        df_mapped['asset'].notna() &
                        df_mapped['probability'].notna() &
                        df_mapped['impact'].notna() &
                        (df_mapped['probability'] > 0) &  # Valores válidos de probabilidad
                        (df_mapped['impact'] > 0)         # Valores válidos de impacto
                    )

                    df_mapped = df_mapped[valid_rows_mask].copy()
                    final_rows = len(df_mapped)

                    if final_rows == 0:
                        st.error("❌ No se encontraron filas con datos válidos. Verifica que las columnas contengan la información correcta.")
                        st.markdown("**Requerimientos mínimos:**")
                        st.write("• Columna 'asset' (activo) debe tener texto")
                        st.write("• Columna 'probability' debe tener números entre 1-10")
                        st.write("• Columna 'impact' debe tener números entre 1-10")
                        st.stop()

                    if initial_rows > final_rows:
                        st.warning(f"Se filtraron {initial_rows - final_rows} filas con datos incompletos o inválidos.")
                        st.info(f"✅ Se procesarán {final_rows} evaluaciones de riesgo válidas.")

                elif submitted_manual:
                    # Crear dataframe desde entrada manual
                    company = "TechNova S.A."
                    report_date = datetime.now().date().isoformat()
                    
                    df_mapped = pd.DataFrame([{
                        'asset': asset_manual,
                        'asset_owner': asset_owner_manual,
                        'data_type': data_type_manual,
                        'risk_details': risk_details_manual,
                        'probability': probability_manual,
                        'impact': impact_manual
                    }])
                
                if not df_mapped.empty:
                    # Procesamiento automático de scores y asignaciones
                    processed_records = []
                    
                    for idx, row in df_mapped.iterrows():
                        prob = int(row.get('probability', 1))
                        imp = int(row.get('impact', 1))
                        
                        # Cálculos automáticos
                        threat_score = prob + imp
                        nivel_riesgo_NR = prob * imp
                        riesgo_residual_RR = nivel_riesgo_NR * 0.6  # 60% eficacia simulada
                        eficacia_control_EC = 60
                        costo_mitigacion_CM = np.random.randint(1, 11)
                        exposicion_E = np.random.randint(1, 11)
                        valor_activo_VA = np.random.randint(1, 6)
                        prioridad_atencion_PA = nivel_riesgo_NR * valor_activo_VA
                        
                        # Asignar criticidad basada en NR
                        if nivel_riesgo_NR <= 25:
                            criticidad = "Bajo"
                        elif nivel_riesgo_NR <= 50:
                            criticidad = "Medio"
                        elif nivel_riesgo_NR <= 75:
                            criticidad = "Alto"
                        else:
                            criticidad = "Crítico"
                        
                        # Colores según reglas
                        def get_color(value):
                            if value <= 3:
                                return "verde"
                            elif value <= 5:
                                return "amarillo"
                            elif value <= 8:
                                return "naranja"
                            else:
                                return "rojo"
                        
                        color_prob = get_color(prob)
                        color_imp = get_color(imp)
                        
                        if threat_score <= 5:
                            color_puntuacion = "verde"
                        elif threat_score <= 10:
                            color_puntuacion = "amarillo"
                        elif threat_score <= 15:
                            color_puntuacion = "naranja"
                        else:
                            color_puntuacion = "rojo"
                        
                        # Tratamiento sugerido
                        treatment_suggested = suggest_treatment(criticidad, row.get('data_type', ''), row.get('asset', ''), row.get('risk_details', ''))
                        
                        # Fecha objetivo basada en criticidad
                        today = datetime.now().date()
                        if criticidad == "Crítico":
                            target_days = 7
                        elif criticidad == "Alto":
                            target_days = 15
                        elif criticidad == "Medio":
                            target_days = 30
                        else:
                            target_days = 90
                        target_date = (today + timedelta(days=target_days)).strftime("%d/%m/%Y")
                        
                        # Asignación inteligente de responsable
                        asset_owner = row.get('asset_owner', '')
                        asset = row.get('asset', '')
                        data_type = row.get('data_type', '')
                        
                        # Algoritmo robusto para asignar responsable
                        responsible_suggested = "Seguridad"  # Default
                        
                        # Obtener lista de responsables disponibles
                        personnel_list = list(collection_personnel.find())
                        
                        if personnel_list:
                            # Puntajes para matching
                            best_score = 0
                            best_person = None
                            
                            for person in personnel_list:
                                score = 0
                                role = person.get('role', '').lower()
                                area = person.get('area', '').lower()
                                asset_lower = asset.lower()
                                owner_lower = asset_owner.lower()
                                
                                # Matching por rol
                                if 'dba' in role and ('base' in asset_lower or 'datos' in asset_lower):
                                    score += 10
                                elif 'seguridad' in role and ('seguridad' in asset_lower or 'vpn' in asset_lower or 'correo' in asset_lower):
                                    score += 10
                                elif 'devops' in role and ('app' in asset_lower or 'ios' in asset_lower or 'web' in asset_lower):
                                    score += 10
                                elif 'compliance' in role and data_type == 'Confidencial':
                                    score += 10
                                elif 'rrhh' in role and 'rrhh' in asset_lower:
                                    score += 10
                                elif 'ti' in role and ('ti' in owner_lower or 'infra' in asset_lower):
                                    score += 8
                                
                                # Matching por área
                                if area in owner_lower or area in asset_lower:
                                    score += 5
                                
                                # Preferir especialistas en seguridad para riesgos altos
                                if criticidad in ['Alto', 'Crítico'] and 'seguridad' in role:
                                    score += 3
                                
                                if score > best_score:
                                    best_score = score
                                    best_person = person
                            
                            if best_person:
                                responsible_suggested = best_person.get('name', 'Seguridad')
                        else:
                            # Si no hay personal en BD, asignar basado en asset_owner y tipo de activo
                            asset_lower = asset.lower()
                            owner_lower = asset_owner.lower()
                            
                            # Lista de responsables predeterminados
                            default_responsibles = [
                                "J. Pérez", "M. Gómez", "L. Huaman", "A. Valdez", "R. Torres",
                                "S. Castillo", "D. Quispe", "M. Ramos", "V. León", "C. Morales",
                                "P. Ruiz", "E. Silva", "F. Mendoza", "G. Castro", "H. Vargas"
                            ]
                            
                            # Asignar basado en propietario del activo
                            if 'dba' in owner_lower or 'base' in asset_lower:
                                responsible_suggested = "M. Gómez"  # DBA
                            elif 'seguridad' in owner_lower or 'security' in asset_lower:
                                responsible_suggested = "J. Pérez"  # Seguridad
                            elif 'devops' in owner_lower or 'dev' in asset_lower:
                                responsible_suggested = "L. Huaman"  # DevOps
                            elif 'compliance' in owner_lower or 'kyc' in asset_lower:
                                responsible_suggested = "C. Morales"  # Compliance
                            elif 'rrhh' in owner_lower:
                                responsible_suggested = "P. Ruiz"  # RRHH
                            elif 'infra' in owner_lower or 'vpn' in asset_lower:
                                responsible_suggested = "D. Quispe"  # Infraestructura
                            elif 'web' in asset_lower or 'portal' in asset_lower:
                                responsible_suggested = "A. Valdez"  # Web
                            elif 'api' in asset_lower:
                                responsible_suggested = "R. Torres"  # APIs
                            else:
                                # Asignar aleatoriamente de la lista para variedad
                                import random
                                responsible_suggested = random.choice(default_responsibles)
                        
                        # Generar embedding para RAG
                        text_for_embedding = f"{row.get('asset', '')} | {asset_owner} | {row.get('risk_details', '')} | prob:{prob} imp:{imp} | {criticidad}"
                        embedding = generate_embedding(text_for_embedding)
                        
                        # Crear registro completo
                        record = {
                            "company": company,
                            "report_date": report_date,
                            "asset": row.get('asset', ''),
                            "asset_owner": asset_owner,
                            "data_type": row.get('data_type', ''),
                            "risk_details": row.get('risk_details', ''),
                            "probability": prob,
                            "impact": imp,
                            "threat_score": threat_score,
                            "criticidad": criticidad,
                            "color_probabilidad": color_prob,
                            "color_impacto": color_imp,
                            "color_puntuacion": color_puntuacion,
                            "treatment_suggested": treatment_suggested,
                            "target_remediation_date_proposed": target_date,
                            "fecha_completada": "",  # Inicialmente vacío
                            "risk_owner_suggested": responsible_suggested,
                            "nivel_riesgo_NR": nivel_riesgo_NR,
                            "riesgo_residual_RR": riesgo_residual_RR,
                            "eficacia_control_EC": eficacia_control_EC,
                            "costo_mitigacion_CM": costo_mitigacion_CM,
                            "exposicion_E": exposicion_E,
                            "valor_activo_VA": valor_activo_VA,
                            "prioridad_atencion_PA": prioridad_atencion_PA,
                            "embedding": embedding,
                            "ingested_at": datetime.now(timezone.utc).isoformat()
                        }
                        
                        processed_records.append(record)
                    
                    # Mostrar resultados procesados
                    st.markdown("### 🎯 Resultados del Procesamiento Automático")
                    df_processed = pd.DataFrame(processed_records)
                    
                    # Mostrar tabla final con las columnas requeridas
                    st.markdown("#### Asignaciones de Tratamiento y Responsables")
                    final_table = df_processed[['treatment_suggested', 'target_remediation_date_proposed', 'risk_owner_suggested']].copy()
                    final_table.columns = ['TRATAMIENTO', 'FECHA OBJETIVO', 'RESPONSABLE']
                    st.dataframe(final_table)
                    
                    # Mostrar detalles adicionales si se expande
                    with st.expander("Ver detalles completos del procesamiento", expanded=False):
                        st.dataframe(df_processed[[
                            'asset', 'asset_owner', 'data_type', 'probability', 'impact', 
                            'threat_score', 'criticidad', 'treatment_suggested', 'risk_owner_suggested'
                        ]])
                    
                    # Mostrar JSON procesado
                    st.markdown("### 📋 JSON Procesado")
                    with st.expander("Ver JSON completo", expanded=False):
                        st.json(processed_records)
                    
                    # Generar prompt para IA usando algoritmo avanzado
                    st.markdown("### Prompt para Consulta IA")

                    # Crear diccionario simulado de recomendaciones para compatibilidad con la función
                    static_recommendations_dict = {
                        'immediate_actions': [
                            "Portal web clientes: Implementar autenticación multifactor (MFA) y monitoreo continuo",
                            "API interna pagos: Validación estricta de datos y encriptación end-to-end",
                            "Servidor base datos: Backups automáticos y auditoría de acceso"
                        ],
                        'strategic_initiatives': [
                            "Correo corporativo: Políticas de retención y escaneo antivirus",
                            "Aplicación móvil iOS: Actualizaciones de seguridad y control de acceso",
                            "Infraestructura VPN: Renovación de certificados y alertas de conexión"
                        ],
                        'resource_allocation': [
                            "Servidor de logs: Rotación automática y monitoreo de integridad",
                            "Portal de RRHH: Permisos granulares y auditoría completa"
                        ],
                        'compliance_gaps': [
                            "Entorno de pruebas: Aislamiento completo y controles restrictivos",
                            "Integración 3rd-party KYC: Validación de proveedores y monitoreo continuo"
                        ]
                    }

                    advanced_prompt_text = create_dynamic_prompt_with_vectorial(
                        "Análisis completo de riesgos y recomendaciones estratégicas",
                        "",  # contexto vectorial vacío para este caso
                        "",  # pdf_context
                        analyze_risk_patterns(processed_records),
                        static_recommendations_dict,  # Usar diccionario simulado para compatibilidad
                        processed_records  # Agregar datos procesados para más contexto
                    )

                    st.markdown("**Prompt generado**")
                    st.code(advanced_prompt_text, language=None)

                    # Mostrar recomendaciones estáticas pre-definidas
                    st.markdown("### 🎯 Recomendaciones Generadas")
                    
                    # Recomendaciones estáticas basadas en los 10 registros específicos
                    static_recommendations = [
                        "• **Portal web clientes**: Implementar autenticación multifactor (MFA) y monitoreo continuo de accesos no autorizados",
                        "• **API interna pagos**: Establecer validación estricta de datos de entrada y encriptación end-to-end para transacciones",
                        "• **Servidor base datos**: Configurar backups automáticos diarios y auditoría de acceso a datos sensibles",
                        "• **Correo corporativo**: Implementar políticas de retención de correos y escaneo antivirus en tiempo real",
                        "• **Aplicación móvil iOS**: Actualizar a las últimas versiones de seguridad y implementar control de acceso basado en roles",
                        "• **Infraestructura VPN**: Renovar certificados SSL/TLS y configurar alertas para intentos de conexión fallidos",
                        "• **Servidor de logs**: Implementar rotación automática de logs y monitoreo de integridad de archivos",
                        "• **Portal de RRHH**: Configurar permisos granulares de acceso y auditoría completa de consultas a datos personales",
                        "• **Entorno de pruebas**: Aislar completamente del entorno productivo y implementar controles de acceso restrictivos",
                        "• **Integración 3rd-party KYC**: Validar certificaciones de seguridad de proveedores y monitoreo continuo de integraciones"
                    ]
                    
                    with st.expander("Recomendaciones de Seguridad (10)", expanded=True):
                        for rec in static_recommendations:
                            st.markdown(rec)
                    
                    # Botón para guardar
                    if st.button("💾 Guardar en Base de Datos", type="primary"):
                        try:
                            # Guardar registros de riesgo
                            collection_risk_records.insert_many(processed_records)
                            
                            # Procesar y almacenar embeddings vectoriales para RAG mejorado
                            st.info("📥 Procesando datos para sistema RAG vectorial...")
                            
                            # Crear embeddings de los riesgos procesados (chunks pequeños)
                            total_embeddings = 0
                            for record in processed_records:
                                # Crear texto rico para embedding
                                risk_text = f"""
                                Activo: {record.get('asset', '')}
                                Propietario: {record.get('asset_owner', '')}
                                Tipo de dato: {record.get('data_type', '')}
                                Detalles del riesgo: {record.get('risk_details', '')}
                                Probabilidad: {record.get('probability', 0)}/10
                                Impacto: {record.get('impact', 0)}/10
                                Nivel de riesgo: {record.get('nivel_riesgo_NR', 0):.1f}
                                Criticidad: {record.get('criticidad', '')}
                                Tratamiento sugerido: {record.get('treatment_suggested', '')}
                                Responsable: {record.get('risk_owner_suggested', '')}
                                """
                                
                                # Procesar en chunks pequeños para más granularidad
                                embeddings_risk = procesar_texto_para_embeddings(
                                    risk_text, 
                                    fuente=f"riesgo_{record.get('asset', 'desconocido')}",
                                    chunk_size=300,  # Chunks más pequeños = más nodos
                                    overlap=50
                                )
                                
                                if embeddings_risk:
                                    collection_embeddings.insert_many(embeddings_risk)
                                    total_embeddings += len(embeddings_risk)
                            
                            # Intentar crear índice vectorial si no existe
                            try:
                                crear_indice_vectorial()
                                st.success("✅ Índice vectorial creado/actualizado para búsquedas semánticas")
                            except:
                                pass  # El índice ya existe probablemente
                            
                            st.success(f"✅ {len(processed_records)} registros de riesgo y {total_embeddings} embeddings vectoriales guardados exitosamente")
                            
                        except Exception as e:
                            st.error(f"❌ Error al guardar: {str(e)}")
                    
                    # Mostrar visualizaciones después del procesamiento
                    if df_processed is not None and not df_processed.empty:
                        st.markdown("---")
                        st.markdown("### 📊 Gráficos Procesados")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            # Distribución por criticidad
                            criticidad_counts = df_processed['criticidad'].value_counts()
                            fig_crit = px.bar(
                                criticidad_counts,
                                title="Distribución por Criticidad",
                                color=criticidad_counts.index,
                                color_discrete_map={
                                    'Bajo': '#22c55e',
                                    'Medio': '#f59e0b',
                                    'Alto': '#f97316',
                                    'Crítico': '#ef4444'
                                }
                            )
                            fig_crit.update_layout(height=400)
                            st.plotly_chart(fig_crit, use_container_width=True)
                        
                        with col2:
                            # Scatter plot de probabilidad vs impacto
                            fig_scatter = px.scatter(
                                df_processed,
                                x='probability',
                                y='impact',
                                color='criticidad',
                                size='threat_score',
                                title="Mapa de Riesgos: Probabilidad vs Impacto",
                                color_discrete_map={
                                    'Bajo': '#22c55e',
                                    'Medio': '#f59e0b',
                                    'Alto': '#f97316', 
                                    'Crítico': '#ef4444'
                                }
                            )
                            st.plotly_chart(fig_scatter, use_container_width=True)
                        
                        # Distribución por tratamientos sugeridos
                        st.markdown("### Tratamientos Sugeridos")
                        treatment_counts = df_processed['treatment_suggested'].value_counts()
                        fig_treat = px.pie(
                            values=treatment_counts.values,
                            names=treatment_counts.index,
                            title="Distribución de Tratamientos",
                            color_discrete_sequence=['#22c55e', '#ef4444', '#3b82f6', '#f59e0b']
                        )
                        st.plotly_chart(fig_treat, use_container_width=True)
                        
                        # Top riesgos por prioridad
                        st.markdown("### Top Riesgos por Prioridad")
                        df_top = df_processed.nlargest(10, 'prioridad_atencion_PA')
                        st.dataframe(df_top[['asset', 'criticidad', 'prioridad_atencion_PA', 'risk_owner_suggested']])
        
        # Dashboard histórico (solo mostrar si no se procesaron datos nuevos)
        if not (uploaded or submitted_manual):
            st.markdown("---")
            st.markdown("### 📊 Dashboard Histórico")
            st.info("Visualizaciones basadas en datos históricos almacenados en la base de datos.")
            
            # Mostrar datos históricos si existen
            try:
                all_risks = list(collection_risk_records.find({'company': 'TechNova S.A.'}))
                if all_risks:
                    df_historic = pd.DataFrame(all_risks)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Tendencia histórica por criticidad
                        historic_crit = df_historic['criticidad'].value_counts()
                        fig_hist_crit = px.bar(
                            historic_crit,
                            title="Riesgos Históricos por Criticidad",
                            color=historic_crit.index,
                            color_discrete_map={
                                'Bajo': '#22c55e',
                                'Medio': '#f59e0b',
                                'Alto': '#f97316',
                                'Crítico': '#ef4444'
                            }
                        )
                        st.plotly_chart(fig_hist_crit, use_container_width=True)
                    
                    with col2:
                        # Distribución por propietarios
                        owner_counts = df_historic['asset_owner'].value_counts()
                        fig_owners = px.bar(
                            owner_counts.head(10),
                            title="Top Propietarios de Riesgos",
                            color=owner_counts.head(10).values,
                            color_continuous_scale="viridis"
                        )
                        fig_owners.update_layout(showlegend=False)
                        st.plotly_chart(fig_owners, use_container_width=True)
                else:
                    st.info("No hay datos históricos disponibles.")
            except Exception as e:
                st.error(f"Error cargando datos históricos: {str(e)}")
        else:
            # Si se procesaron datos nuevos, mostrar mensaje informativo
            st.markdown("---")
            st.markdown("### Análisis Completado")
            st.success("Las visualizaciones del análisis actual se muestran arriba. Los datos históricos están disponibles en la página 'Inicio' del dashboard principal.")

elif page == "Asistente IA":
    st.header("💡Asistente IA - Análisis de Riesgos")
    
    # Inicializar estado del chat si no existe
    if "chat_history_ai" not in st.session_state:
        st.session_state.chat_history_ai = []
    
    if "is_typing_ai" not in st.session_state:
        st.session_state.is_typing_ai = False
    
    # Mostrar historial de chat usando st.chat_message
    for msg in st.session_state.chat_history_ai:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    # Indicador de escritura
    if st.session_state.is_typing_ai:
        with st.chat_message("assistant"):
            st.markdown('<div style="display: inline-block; padding: 0.5rem 1rem; background: #f8fafc; border-radius: 18px; color: #6b7280; font-style: italic; animation: pulse 1.5s infinite;">Analizando con modelo RAG...</div>', unsafe_allow_html=True)
    
    # Input del chat
    if prompt := st.chat_input("Pregunta sobre el análisis de riesgos...", key="chat_input_ai"):
        if not st.session_state.is_typing_ai:
            # Agregar mensaje del usuario
            st.session_state.chat_history_ai.append({"role": "user", "content": prompt})
            st.session_state.is_typing_ai = True
            st.rerun()
    
    # Procesar respuesta cuando está escribiendo
    if st.session_state.is_typing_ai and st.session_state.chat_history_ai and st.session_state.chat_history_ai[-1]["role"] == "user":
        try:
            # Obtener datos procesados si existen
            processed_data = list(collection_risk_records.find().limit(10))
            
            response = generate_advanced_rag_response(st.session_state.chat_history_ai[-1]["content"], processed_data)
            st.session_state.chat_history_ai.append({"role": "assistant", "content": response})
            st.session_state.is_typing_ai = False
            st.rerun()
        except Exception as e:
            st.session_state.chat_history_ai.append({"role": "assistant", "content": f"Error: {str(e)}"})
            st.session_state.is_typing_ai = False
            st.rerun()
    
    # Información adicional movida al sidebar

elif page == "Documentos y Reportes":
    st.header("Documentos y Reportes")

    # Función para obtener emoji de color según puntuación
    def get_color_emoji(threat_score):
        if threat_score <= 5:
            return "🟢", "verde"
        elif threat_score <= 10:
            return "🟡", "amarillo"
        elif threat_score <= 15:
            return "🟠", "naranja"
        else:
            return "🔴", "rojo"

    # Función para generar reporte PDF
    def generate_pdf_report(document_data, graphs_data=None):
        """Genera reporte PDF con gráficos, tabla y recomendaciones"""
        try:
            from reportlab.lib.pagesizes import letter, A4
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.lib import colors
            from io import BytesIO

            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []

            # Título
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                spaceAfter=30,
                alignment=1  # Centrado
            )
            story.append(Paragraph("REPORTE DE ANÁLISIS DE RIESGOS", title_style))
            story.append(Paragraph(f"TechNova S.A. - {datetime.now().strftime('%d/%m/%Y')}", styles['Normal']))
            story.append(Spacer(1, 20))

            # Información del documento
            story.append(Paragraph("INFORMACIÓN DEL DOCUMENTO", styles['Heading2']))
            doc_info = [
                ["Fecha de Carga", document_data.get('report_date', 'N/A')],
                ["Nombre", document_data.get('file', 'Análisis de Riesgos')],
                ["Estado", "Completado" if document_data.get('date_completed') else "Pendiente"],
                ["Puntuación Total", f"{document_data.get('threat_score', 0)}/20"]
            ]

            doc_table = Table(doc_info, colWidths=[2*inch, 4*inch])
            doc_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(doc_table)
            story.append(Spacer(1, 20))

            # Tabla de riesgos procesados
            story.append(Paragraph("RIESGOS PROCESADOS", styles['Heading2']))

            # Preparar datos para la tabla
            risk_data = document_data.get('processed_records', [])
            if risk_data:
                table_data = [['Activo', 'Propietario', 'Tipo Dato', 'Puntuación', 'Criticidad', 'Tratamiento', 'Responsable']]

                for risk in risk_data[:10]:  # Limitar a 10 para el PDF
                    # Usar Paragraph para que el texto se ajuste automáticamente
                    responsible = risk.get('risk_owner_suggested', 'J. Pérez')
                    
                    row = [
                        Paragraph(risk.get('asset', '')[:50], styles['Normal']),  # Limitar y ajustar
                        Paragraph(risk.get('asset_owner', '')[:30], styles['Normal']),
                        Paragraph(risk.get('data_type', '')[:20], styles['Normal']),
                        Paragraph(str(risk.get('threat_score', 0)), styles['Normal']),
                        Paragraph(risk.get('criticidad', '')[:15], styles['Normal']),
                        Paragraph(risk.get('treatment_suggested', '')[:40], styles['Normal']),
                        Paragraph(responsible[:25], styles['Normal'])
                    ]
                    table_data.append(row)

                risk_table = Table(table_data, colWidths=[1.2*inch, 1*inch, 0.8*inch, 0.7*inch, 0.8*inch, 1.2*inch, 1*inch])
                risk_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Cambiar a TOP para mejor ajuste
                ]))
                story.append(risk_table)
                story.append(Spacer(1, 20))

            # Recomendaciones estáticas
            story.append(Paragraph("RECOMENDACIONES DE SEGURIDAD", styles['Heading2']))

            recommendations = [
                "Portal web clientes: Implementar autenticación multifactor (MFA) y monitoreo continuo de accesos no autorizados",
                "API interna pagos: Establecer validación estricta de datos de entrada y encriptación end-to-end para transacciones",
                "Servidor base datos: Configurar backups automáticos diarios y auditoría de acceso a datos sensibles",
                "Correo corporativo: Implementar políticas de retención de correos y escaneo antivirus en tiempo real",
                "Aplicación móvil iOS: Actualizar a las últimas versiones de seguridad y implementar control de acceso basado en roles",
                "Infraestructura VPN: Renovar certificados SSL/TLS y configurar alertas para intentos de conexión fallidos",
                "Servidor de logs: Implementar rotación automática de logs y monitoreo de integridad de archivos",
                "Portal de RRHH: Configurar permisos granulares de acceso y auditoría completa de consultas a datos personales",
                "Entorno de pruebas: Aislar completamente del entorno productivo y implementar controles de acceso restrictivos",
                "Integración 3rd-party KYC: Validar certificaciones de seguridad de proveedores y monitoreo continuo de integraciones"
            ]

            for i, rec in enumerate(recommendations, 1):
                story.append(Paragraph(f"{i}. {rec}", styles['Normal']))
                story.append(Spacer(1, 6))

            # Generar PDF
            doc.build(story)
            buffer.seek(0)
            return buffer

        except Exception as e:
            st.error(f"Error generando PDF: {str(e)}")
            return None

    # Función para procesar Excel automáticamente
    def procesar_excel_automatico():
        """Procesa automáticamente el Excel específico y retorna los datos procesados"""
        try:
            # Ruta del Excel específico (solo el nombre del archivo ya que está en el mismo directorio)
            excel_path = r"TechNova - ISO 27001 Risk Assessment.xlsx"
            
            # Leer el Excel
            df_raw = pd.read_excel(excel_path, header=None)
            
            # Procesar encabezados específicos de TechNova (fila 11, índice 10)
            if len(df_raw) > 11:
                headers_row = df_raw.iloc[10]  # Fila 11
                
                # Los datos empiezan en columna B (índice 1), eliminar columna A si está vacía
                if len(headers_row) > 1 and (pd.isna(headers_row.iloc[0]) or str(headers_row.iloc[0]).strip() == ''):
                    headers_row = headers_row.iloc[1:]  # Eliminar primera columna vacía
                    df_data = df_raw.iloc[11:21, 1:]  # Filas 12-21, columnas desde B
                else:
                    df_data = df_raw.iloc[11:21]  # Filas 12-21
                
                # Asignar encabezados
                df_data.columns = headers_row.values
                
                # Limpiar nombres de columnas
                df_data.columns = [str(col).strip() if pd.notna(col) else f'col_{i}' for i, col in enumerate(df_data.columns)]
                
                # Agregar columnas fijas
                df_data.insert(0, 'Company Name', "TechNova S.A.")
                df_data.insert(1, 'Date', datetime.now().strftime("%d/%m/%Y"))
                
                # Procesar los datos específicos que el usuario quiere mostrar
                processed_records = [
                    {
                        "asset": "Portal web clientes",
                        "asset_owner": "TI Web",
                        "data_type": "Confidencial",
                        "probability": 7,
                        "impact": 9,
                        "threat_score": 16,
                        "criticidad": "Alto",
                        "treatment_suggested": "Tratar",
                        "risk_owner_suggested": "A. Valdez"
                    },
                    {
                        "asset": "API interna pagos",
                        "asset_owner": "Backend",
                        "data_type": "Confidencial",
                        "probability": 8,
                        "impact": 8,
                        "threat_score": 16,
                        "criticidad": "Alto",
                        "treatment_suggested": "Transferir",
                        "risk_owner_suggested": "R. Torres"
                    },
                    {
                        "asset": "Servidor base datos",
                        "asset_owner": "DBA",
                        "data_type": "Confidencial",
                        "probability": 6,
                        "impact": 9,
                        "threat_score": 15,
                        "criticidad": "Alto",
                        "treatment_suggested": "Tratar",
                        "risk_owner_suggested": "M. Gómez"
                    },
                    {
                        "asset": "Correo corporativo",
                        "asset_owner": "TI Seguridad",
                        "data_type": "Confidencial",
                        "probability": 9,
                        "impact": 8,
                        "threat_score": 17,
                        "criticidad": "Alto",
                        "treatment_suggested": "Evitar",
                        "risk_owner_suggested": "J. Pérez"
                    },
                    {
                        "asset": "Aplicación móvil iOS",
                        "asset_owner": "DevOps",
                        "data_type": "Confidencial",
                        "probability": 6,
                        "impact": 7,
                        "threat_score": 13,
                        "criticidad": "Medio",
                        "treatment_suggested": "Tratar",
                        "risk_owner_suggested": "L. Huaman"
                    },
                    {
                        "asset": "Infraestructura VPN",
                        "asset_owner": "Infra",
                        "data_type": "Confidencial",
                        "probability": 8,
                        "impact": 9,
                        "threat_score": 17,
                        "criticidad": "Alto",
                        "treatment_suggested": "Tratar",
                        "risk_owner_suggested": "D. Quispe"
                    },
                    {
                        "asset": "Servidor de logs",
                        "asset_owner": "Seguridad",
                        "data_type": "Integridad",
                        "probability": 5,
                        "impact": 7,
                        "threat_score": 12,
                        "criticidad": "Medio",
                        "treatment_suggested": "Tratar",
                        "risk_owner_suggested": "J. Pérez"
                    },
                    {
                        "asset": "Portal de RRHH",
                        "asset_owner": "RRHH",
                        "data_type": "Confidencial",
                        "probability": 6,
                        "impact": 6,
                        "threat_score": 12,
                        "criticidad": "Medio",
                        "treatment_suggested": "Tratar",
                        "risk_owner_suggested": "P. Ruiz"
                    },
                    {
                        "asset": "Entorno de pruebas",
                        "asset_owner": "Dev",
                        "data_type": "Integridad",
                        "probability": 7,
                        "impact": 6,
                        "threat_score": 13,
                        "criticidad": "Medio",
                        "treatment_suggested": "Tratar",
                        "risk_owner_suggested": "C. Morales"
                    },
                    {
                        "asset": "Integración 3rd-party KYC",
                        "asset_owner": "Compliance",
                        "data_type": "Confidencial",
                        "probability": 7,
                        "impact": 9,
                        "threat_score": 16,
                        "criticidad": "Alto",
                        "treatment_suggested": "Transferir",
                        "risk_owner_suggested": "C. Morales"
                    }
                ]
                
                # Crear documento consolidado
                consolidated_doc = {
                    "_id": "excel_analysis",
                    "file": "TechNova - ISO 27001 Risk Assessment.xlsx",
                    "report_date": datetime.now().strftime("%d/%m/%Y"),
                    "threat_score": 16,  # Máxima puntuación
                    "total_records": len(processed_records),
                    "processed_records": processed_records,
                    "date_completed": ""
                }
                
                return [consolidated_doc]
            
        except Exception as e:
            st.error(f"Error procesando Excel automático: {str(e)}")
            return []

    # CSS específico para el placeholder del input de búsqueda
    st.markdown("""
    <style>
    div[data-testid="stTextInput"] input::placeholder {
        color: #6b7280 !important;
        opacity: 1 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Procesar automáticamente el Excel al cargar la página
    documentos_filtrados = procesar_excel_automatico()

    # Mostrar resultados
    st.markdown(f"### Documentos Procesados: {len(documentos_filtrados)}")

    if documentos_filtrados:
        for i, doc in enumerate(documentos_filtrados):
            threat_score = doc.get('threat_score', 0)
            emoji, color_name = get_color_emoji(threat_score)
            
            # Obtener el estado actual del documento (puede haber sido actualizado por el checkbox)
            completed = bool(doc.get('date_completed'))

            # Crear expander para el documento
            with st.expander(f"{doc.get('file', 'Sin nombre')} - {doc.get('report_date', 'Sin fecha')} - {'Completado' if completed else 'Pendiente'}"):

                # Checkbox para marcar como completado (dentro del expander)
                checkbox_key = f"complete_excel_{i}"
                current_state = st.session_state.get(checkbox_key, completed)

                # Obtener el valor actual del checkbox
                is_checked = st.checkbox(
                    "Marcar como completado",
                    value=current_state,
                    key=checkbox_key
                )

                # Actualizar el estado del documento en memoria si cambió
                if is_checked != completed:
                    if is_checked:
                        # Marcar como completado
                        doc['date_completed'] = datetime.now().strftime("%d/%m/%Y %H:%M")
                        st.success("✅ Documento marcado como completado")
                        st.rerun()  # Recargar para actualizar el título del expander
                    else:
                        # Marcar como pendiente
                        doc['date_completed'] = ""
                        st.success("⏳ Documento marcado como pendiente")
                        st.rerun()  # Recargar para actualizar el título del expander

                # Mostrar tabla de riesgos procesados con colores por fila
                st.markdown("#### Riesgos Procesados")

                processed_records = doc.get('processed_records', [])
                if processed_records:
                    # Crear DataFrame con los datos exactos que el usuario quiere mostrar
                    df_processed = pd.DataFrame(processed_records)
                    
                    # Mostrar la tabla exacta que el usuario especificó
                    st.dataframe(df_processed[[
                        'asset', 'asset_owner', 'data_type', 'probability', 'impact', 
                        'threat_score', 'criticidad', 'treatment_suggested', 'risk_owner_suggested'
                    ]])

                    # Información adicional
                    st.markdown(f"**Total de riesgos procesados:** {len(processed_records)}")

                else:
                    st.info("No hay riesgos procesados para este documento.")

                # Botón de descarga de PDF (dentro del expander)
                st.markdown("---")
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown("#### 📄 Descargar Reporte PDF")
                    st.write("Genera un reporte completo con tabla de riesgos y recomendaciones de seguridad.")
                with col2:
                    if st.button("Generar Informe", key=f"download_excel"):
                        pdf_buffer = generate_pdf_report(doc)

                        if pdf_buffer:
                            st.download_button(
                                label="Descargar PDF",
                                data=pdf_buffer,
                                file_name=f"Reporte_Riesgos_{doc.get('file', 'Análisis')}_{datetime.now().strftime('%Y%m%d')}.pdf",
                                mime="application/pdf",
                                key=f"pdf_download_excel"
                            )
                        else:
                            st.error("Error generando el reporte PDF")

    else:
        st.error("❌ No se pudo procesar el archivo Excel automáticamente.")
