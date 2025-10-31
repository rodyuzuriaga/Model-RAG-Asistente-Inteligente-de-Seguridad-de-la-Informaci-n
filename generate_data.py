import json
import random
from datetime import datetime, timedelta, timezone

# Definir distribución exacta según tabla proporcionada
area_config = {
    "Administración": {
        "count": 3,
        "prob_range": (5, 7),
        "prob_mean": 6,
        "imp_range": (4, 7),
        "imp_mean": 5.5,
        "threat_range": (9, 13),
        "nr_range": (25, 35),
        "nr_mean": 30,
        "madurez": 2.0,
        "iso": "A.8 Gestión de Activos",
        "notas": "Riesgos por error humano y acceso indebido a documentos internos."
    },
    "Calidad": {
        "count": 5,
        "prob_range": (6, 8),
        "prob_mean": 7,
        "imp_range": (5, 8),
        "imp_mean": 6.5,
        "threat_range": (11, 15),
        "nr_range": (28, 36),
        "nr_mean": 32,
        "madurez": 2.2,
        "iso": "A.12 Seguridad de Operaciones",
        "notas": "Inconsistencias en reportes digitales y trazabilidad deficiente."
    },
    "Desarrollo de Software": {
        "count": 2,
        "prob_range": (7, 9),
        "prob_mean": 8,
        "imp_range": (7, 10),
        "imp_mean": 8.5,
        "threat_range": (14, 18),
        "nr_range": (38, 49),
        "nr_mean": 44,
        "madurez": 2.5,
        "iso": "A.14 Adquisición, desarrollo y mantenimiento",
        "notas": "Vulnerabilidades en código, exposición de APIs, dependencias no verificadas."
    },
    "Finanzas": {
        "count": 3,
        "prob_range": (5, 7),
        "prob_mean": 6,
        "imp_range": (4, 6),
        "imp_mean": 5,
        "threat_range": (9, 12),
        "nr_range": (24, 30),
        "nr_mean": 26,
        "madurez": 2.0,
        "iso": "A.18 Cumplimiento",
        "notas": "Riesgo de error en conciliaciones, acceso a reportes financieros sensibles."
    },
    "Legal": {
        "count": 2,
        "prob_range": (5, 6),
        "prob_mean": 5.5,
        "imp_range": (5, 8),
        "imp_mean": 6.5,
        "threat_range": (10, 13),
        "nr_range": (28, 34),
        "nr_mean": 31,
        "madurez": 2.0,
        "iso": "A.18 Cumplimiento",
        "notas": "Fuga de documentos contractuales o incumplimiento normativo."
    },
    "Logística": {
        "count": 6,
        "prob_range": (6, 8),
        "prob_mean": 7,
        "imp_range": (4, 6),
        "imp_mean": 5,
        "threat_range": (10, 13),
        "nr_range": (25, 32),
        "nr_mean": 28,
        "madurez": 2.1,
        "iso": "A.13 Comunicaciones y Operaciones",
        "notas": "Fallos de red, errores en sincronización de entregas digitales."
    },
    "Marketing": {
        "count": 4,
        "prob_range": (6, 9),
        "prob_mean": 7.5,
        "imp_range": (6, 9),
        "imp_mean": 7.5,
        "threat_range": (12, 17),
        "nr_range": (30, 40),
        "nr_mean": 34,
        "madurez": 2.0,
        "iso": "A.9 Control de Acceso",
        "notas": "Riesgo de campañas falsas o fuga de leads; phishing a clientes."
    },
    "Operaciones": {
        "count": 2,
        "prob_range": (4, 6),
        "prob_mean": 5,
        "imp_range": (3, 6),
        "imp_mean": 4.5,
        "threat_range": (8, 11),
        "nr_range": (15, 25),
        "nr_mean": 20,
        "madurez": 1.8,
        "iso": "A.12 Seguridad de Operaciones",
        "notas": "Caídas de sistemas internos, interrupción de servicios."
    },
    "Recursos Humanos": {
        "count": 6,
        "prob_range": (6, 8),
        "prob_mean": 7,
        "imp_range": (5, 7),
        "imp_mean": 6,
        "threat_range": (11, 14),
        "nr_range": (25, 35),
        "nr_mean": 29,
        "madurez": 2.1,
        "iso": "A.9 Control de Acceso",
        "notas": "Exposición de datos personales de empleados, errores en permisos."
    },
    "Seguridad Informática": {
        "count": 8,
        "prob_range": (7, 10),
        "prob_mean": 8.5,
        "imp_range": (7, 10),
        "imp_mean": 8.5,
        "threat_range": (14, 19),
        "nr_range": (40, 55),
        "nr_mean": 46,
        "madurez": 2.3,
        "iso": "A.12 Seguridad de Operaciones",
        "notas": "Malware, accesos no autorizados, ransomware, phishing."
    },
    "Ventas": {
        "count": 5,
        "prob_range": (6, 9),
        "prob_mean": 7.5,
        "imp_range": (6, 8),
        "imp_mean": 7,
        "threat_range": (12, 16),
        "nr_range": (30, 38),
        "nr_mean": 33,
        "madurez": 2.0,
        "iso": "A.13 Comunicaciones y Operaciones",
        "notas": "Pérdida de leads o exposición de información de clientes."
    },
    "Área de TI": {
        "count": 10,
        "prob_range": (6, 9),
        "prob_mean": 7.5,
        "imp_range": (6, 9),
        "imp_mean": 7,
        "threat_range": (12, 17),
        "nr_range": (32, 42),
        "nr_mean": 37,
        "madurez": 2.4,
        "iso": "A.12 Seguridad de Operaciones",
        "notas": "Fallas en servidores, configuraciones inseguras, brechas en accesos."
    }
}

# Para tratamientos, mantener distribución anterior pero ajustar
tratamientos_lista = ['Tratar'] * 23 + ['Transferir'] * 17 + ['Aceptar'] * 5 + ['Evitar'] * 11
random.shuffle(tratamientos_lista)

# Índices para críticos y mitigados
total_risks = sum(config['count'] for config in area_config.values())
criticos_indices = random.sample(range(total_risks), 8)  # Ajustar a 8 críticos
mitigados_indices = random.sample(range(total_risks), 15)

# Datos base
activos = [
    "Servidor de base de datos", "Aplicación web interna", "Correo corporativo",
    "Sistema de gestión financiera", "Red corporativa", "Dispositivos móviles",
    "Almacenamiento en la nube", "Sistema de autenticación", "Base de datos de clientes",
    "Portal de empleados", "Sistema de backup", "VPN corporativa",
    "Aplicación móvil", "Sistema de monitoreo", "Firewall perimetral",
    "Servidores de desarrollo", "Base de datos histórica", "Sistema de reportes",
    "API de integración", "Plataforma de e-learning"
]

tipos_dato = [
    "Datos de clientes", "Datos operativos internos", "Datos personales",
    "Información financiera", "Datos confidenciales", "Información estratégica",
    "Registros de empleados", "Datos de proveedores", "Información regulatoria"
]

riesgos_detalle = [
    "Amenazas a la confidencialidad por acceso no autorizado a datos sensibles.",
    "Amenazas a la integridad por modificación no autorizada de información crítica.",
    "Amenazas a la disponibilidad por ataques DDoS o fallas del sistema.",
    "Amenazas a la confidencialidad e integridad por malware y ransomware.",
    "Amenazas a la disponibilidad por configuración errónea de servicios.",
    "Amenazas a la confidencialidad por phishing e ingeniería social.",
    "Amenazas a la integridad por inyección SQL o XSS.",
    "Amenazas a la disponibilidad por pérdida física de equipos.",
    "Amenazas a la confidencialidad por credenciales comprometidas.",
    "Amenazas a la integridad por actualizaciones no autorizadas.",
    "Amenazas a la disponibilidad por sobrecarga de recursos.",
    "Amenazas a la confidencialidad por interceptación de comunicaciones.",
    "Amenazas a la integridad por errores de usuario.",
    "Amenazas a la disponibilidad por fallos en proveedores externos.",
    "Amenazas a la confidencialidad por dispositivos perdidos o robados."
]

responsables = [
    "Carlos Rivas", "Lucía Mendoza", "Rody Uzuriaga", "Ana García",
    "Miguel Torres", "Sofia Ramírez", "Diego López", "Carmen Silva",
    "Javier Morales", "Patricia Ruiz", "Roberto Castro", "Elena Vargas"
]

def get_color_prob_imp(value):
    if value <= 3:
        return "verde"
    elif value <= 5:
        return "amarillo"
    elif value <= 8:
        return "naranja"
    else:
        return "rojo"

def get_color_puntuacion(value):
    if value <= 5:
        return "verde"
    elif value <= 10:
        return "amarillo"
    elif value <= 15:
        return "naranja"
    else:
        return "rojo"

def suggest_treatment(criticidad, tipo_dato, activo):
    rand = random.random()
    if rand < 0.089:  # Aceptar: 5
        return 'Aceptar'
    elif rand < 0.089 + 0.196:  # Evitar: 11
        return 'Evitar'
    elif rand < 0.089 + 0.196 + 0.304:  # Transferir: 17
        return 'Transferir'
    else:  # Tratar: 23
        return 'Tratar'

def compute_criticidad(puntuacion):
    if puntuacion <= 6:
        return "Bajo"
    elif puntuacion <= 12:
        return "Medio"
    elif puntuacion <= 19:
        return "Alto"
    else:
        return "Crítico"

# Generar registros según configuración
data = []
today = datetime(2025, 10, 30)
idx = 0

for area, config in area_config.items():
    for _ in range(config['count']):
        # Generar valores dentro de rangos
        prob = random.randint(*config['prob_range'])
        imp = random.randint(*config['imp_range'])
        threat_score = prob + imp
        nr = random.randint(*config['nr_range'])
        
        # Asegurar que threat_score esté en rango
        if threat_score < config['threat_range'][0]:
            threat_score = config['threat_range'][0]
        elif threat_score > config['threat_range'][1]:
            threat_score = config['threat_range'][1]
        
        eficacia = random.randint(40, 80)
        rr = nr * (1 - eficacia/100)
        cm = random.randint(1, 10)
        exposicion = random.randint(1, 10)
        va = random.randint(1, 5)
        pa = nr * va

        criticidad = compute_criticidad(threat_score)
        tratamiento = tratamientos_lista[idx % len(tratamientos_lista)]

        # Estado de mitigación
        fecha_completada = ""
        if idx in mitigados_indices:
            dias_atras = random.randint(1, 30)
            fecha_completada = (today - timedelta(days=dias_atras)).strftime("%Y-%m-%d")

        # Fecha objetivo
        if criticidad == "Crítico":
            days = 7
        elif criticidad == "Alto":
            days = 15
        elif criticidad == "Medio":
            days = 30
        else:
            days = 90

        fecha_objetivo = (today + timedelta(days=days)).strftime("%Y-%m-%d")

        record = {
            "company": "TechNova S.A.",
            "report_date": "2025-10-30",
            "asset": random.choice(activos),
            "asset_owner": area,
            "data_type": random.choice(tipos_dato),
            "risk_details": random.choice(riesgos_detalle),
            "probability": prob,
            "impact": imp,
            "threat_score": threat_score,
            "criticidad": criticidad,
            "color": get_color_puntuacion(threat_score),
            "color_probabilidad": get_color_prob_imp(prob),
            "color_impacto": get_color_prob_imp(imp),
            "color_puntuacion": get_color_puntuacion(threat_score),
            "treatment_suggested": tratamiento,
            "target_remediation_date_proposed": fecha_objetivo,
            "date_completed": fecha_completada,
            "responsible_suggested": random.choice(responsables),
            "nivel_riesgo_NR": nr,
            "riesgo_residual_RR": round(rr, 1),
            "eficacia_control_EC": eficacia,
            "costo_mitigacion_CM": cm,
            "exposicion_E": exposicion,
            "valor_activo_VA": va,
            "prioridad_atencion_PA": pa,
            "madurez_control": config['madurez'],
            "clasificacion_iso": config['iso'],
            "notas_tecnicas": config['notas'],
            "ingested_at": datetime.now(timezone.utc).isoformat()
        }
        data.append(record)
        idx += 1

# Generar responsables
responsables_data = []
for resp in responsables:
    responsable = {
        "name": resp,
        "role": random.choice(["Administrador TI", "DBA", "DevOps", "Seguridad", "Compliance", "RRHH", "Desarrollo", "Operaciones"]),
        "email": f"{resp.lower().replace(' ', '.')}@technova.com",
        "area": random.choice(["TI", "Seguridad", "Desarrollo", "Operaciones", "Finanzas", "RRHH"]),
        "company": "TechNova S.A."
    }
    responsables_data.append(responsable)

# Crear JSON
json_data = {
    "company": {
        "name": "TechNova S.A.",
        "date": "2025-10-30"
    },
    "data": data,
    "responsables": responsables_data,
    "color_rules": {
        "probabilidad_impacto": {
            "0-3": "verde",
            "4-5": "amarillo",
            "6-8": "naranja",
            "9-10": "rojo"
        },
        "puntuacion": {
            "2-5": "verde",
            "6-10": "amarillo",
            "11-15": "naranja",
            "16-20": "rojo"
        }
    },
    "formulas": {
        "puntuacion_amenaza": "probabilidad + impacto",
        "nivel_riesgo_NR": "probabilidad * impacto",
        "riesgo_residual_RR": "NR * (1 - eficacia_control/100)",
        "eficacia_control_EC": "(NR - RR) / NR * 100",
        "prioridad_atencion_PA": "NR * valor_activo"
    }
}

# Guardar
with open('techNova_risk_data.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f, indent=2, ensure_ascii=False)

print("✅ Datos generados según distribución exacta de la tabla y guardados en techNova_risk_data.json")
print(f"📊 {len(data)} registros de riesgo generados")
print(f"👥 {len(responsables_data)} responsables generados")