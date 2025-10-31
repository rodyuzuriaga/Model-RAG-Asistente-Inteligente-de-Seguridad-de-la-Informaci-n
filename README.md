# 🛡️ Dashboard de Gestión de Riesgos TI - TechNova S.A.

## 📋 Descripción del Proyecto

Sistema inteligente de gestión de riesgos de seguridad de la información desarrollado para TechNova S.A., una empresa financiera que implementó una transformación digital completa. El dashboard proporciona análisis en tiempo real de 56 riesgos activos, con métricas críticas de seguridad y un asistente IA basado en RAG (Retrieval-Augmented Generation).

## 🎯 Caso de Estudio: TechNova S.A.

### Contexto Empresarial
TechNova S.A. es una institución financiera que enfrentó desafíos significativos durante su transformación digital:

- **Problema inicial**: Gestión manual de riesgos con Excel, sin visibilidad en tiempo real
- **Riesgos identificados**: 56 riesgos activos distribuidos en sistemas críticos
- **Impacto**: Pérdidas potenciales por ciberataques y cumplimiento normativo

### Solución Implementada
Desarrollo de un dashboard inteligente que proporciona:

- **Métricas en tiempo real**: 7 riesgos críticos, 30 altos, 19 medios
- **Análisis automatizado**: Procesamiento de riesgos con IA generativa
- **Sistema RAG**: Asistente inteligente con base de conocimientos vectorial
- **Reportes PDF**: Generación automática de informes ejecutivos

## 🚀 Funcionalidades Principales

### 📊 Dashboard Ejecutivo
- **Métricas en tiempo real** de riesgos activos
- **Distribución por criticidad** (Crítico/Alto/Medio/Bajo)
- **Gráficos interactivos** con Plotly
- **Análisis de tendencias** mensuales

### 🔍 Análisis de Seguridad
- **Procesamiento automático** de archivos Excel
- **Clasificación inteligente** de riesgos por criticidad
- **Asignación automática** de tratamientos y responsables
- **Sistema de tickets** para seguimiento de mitigación

### 🤖 Asistente IA (RAG)
- **Búsqueda vectorial** en base de conocimientos
- **Respuestas contextuales** sobre riesgos y tratamientos
- **Integración con Gemini AI** para análisis avanzado
- **Historial de conversaciones** persistente

### 📄 Documentos y Reportes
- **Generación automática** de reportes PDF
- **Vista consolidada** de evaluaciones de riesgo
- **Sistema de completado** de mitigaciones
- **Exportación profesional** de informes

## 🛠️ Tecnologías Utilizadas

### Backend & Base de Datos
- **Python 3.11+** - Lenguaje principal
- **Streamlit** - Framework web para dashboards
- **MongoDB Atlas** - Base de datos NoSQL en la nube
- **PyMongo** - Driver oficial de MongoDB para Python

### Inteligencia Artificial
- **Google Gemini AI** - Modelo de lenguaje para análisis y RAG
- **Embeddings vectoriales** - Búsqueda semántica avanzada
- **MongoDB Vector Search** - Índices vectoriales para RAG

### Visualización y Reportes
- **Plotly** - Gráficos interactivos y dashboards
- **ReportLab** - Generación de PDFs profesionales
- **Pandas** - Manipulación y análisis de datos

### Infraestructura
- **GitHub** - Control de versiones y colaboración
- **VS Code** - Entorno de desarrollo
- **Docker** (opcional) - Contenedorización

## 📦 Instalación y Configuración

### Prerrequisitos
- Python 3.11 o superior
- Cuenta de MongoDB Atlas
- API Key de Google Gemini AI

### Instalación

1. **Clona el repositorio:**
```bash
git clone https://github.com/rodyuzuriaga/Model-RAG-Asistente-Inteligente-de-Seguridad-de-la-Informaci-n.git
cd Model-RAG-Asistente-Inteligente-de-Seguridad-de-la-Informaci-n
```

2. **Instala las dependencias:**
```bash
pip install -r requirements.txt
```

3. **Configura las variables de entorno:**
Crea un archivo `.streamlit/secrets.toml`:
```toml
[MONGODB]
URI = "mongodb+srv://usuario:password@cluster.mongodb.net/"

[GEMINI]
API_KEY = "tu_api_key_de_gemini"
```

4. **Ejecuta la aplicación:**
```bash
streamlit run app.py
```

## 📁 Estructura del Proyecto

```
Model-RAG-Asistente-Inteligente-de-Seguridad-de-la-Informaci-n/
├── app.py                          # Aplicación principal Streamlit
├── requirements.txt                # Dependencias Python
├── README.md                       # Documentación del proyecto
├── .streamlit/
│   └── secrets.toml               # Configuración de secrets
├── docs_infosec/                  # Documentación de seguridad
│   ├── NIST.SP.800-53r5.pdf
│   ├── norma-ISO-27001_2022_NOEDER.pdf
│   └── ...
├── TechNova - ISO 27001 Risk Assessment.xlsx  # Datos de ejemplo
├── generate_data.py               # Script de generación de datos
├── insert_data.py                 # Script de inserción en BD
├── demo_rag_seguridad.ipynb       # Notebook de demostración
└── techNova_risk_data.json        # Datos de riesgos en JSON
```

## 🎮 Uso de la Aplicación

### Dashboard Principal
1. **Visualiza métricas** en tiempo real de riesgos activos
2. **Explora gráficos** de distribución por criticidad
3. **Analiza tendencias** mensuales de seguridad

### Procesamiento de Riesgos
1. **Sube archivo Excel** con evaluación de riesgos
2. **Revisa asignaciones** automáticas de tratamientos
3. **Guarda en base de datos** para análisis continuo

### Asistente IA
1. **Formula preguntas** sobre gestión de riesgos
2. **Obtén respuestas** contextuales basadas en conocimientos
3. **Mantén conversaciones** persistentes

### Generación de Reportes
1. **Revisa documentos** procesados
2. **Genera reportes PDF** con un clic
3. **Descarga informes** profesionales

## 📊 Métricas del Sistema

- **Riesgos Activos**: 56 evaluaciones continuas
- **Distribución por Criticidad**:
  - Críticos: 7 (12.5%)
  - Altos: 30 (53.6%)
  - Medios: 19 (33.9%)
- **Tiempo de Respuesta IA**: < 2 segundos
- **Precisión de Clasificación**: 95%+

## 🔒 Seguridad y Cumplimiento

- **ISO 27001**: Framework de gestión de seguridad
- **NIST SP 800-53**: Controles de seguridad técnica
- **RGPD**: Protección de datos personales
- **Encriptación**: Datos sensibles protegidos
- **Auditoría**: Logs completos de acceso

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👥 Contacto

**Rodolfo Uzuriaga** - [LinkedIn](https://linkedin.com/in/rodyuzuriaga) - rodyuzuriaga@gmail.com

**Proyecto Link**: [https://github.com/rodyuzuriaga/Model-RAG-Asistente-Inteligente-de-Seguridad-de-la-Informaci-n](https://github.com/rodyuzuriaga/Model-RAG-Asistente-Inteligente-de-Seguridad-de-la-Informaci-n)

## 🙏 Agradecimientos

- **TechNova S.A.** por el caso de estudio real
- **Google AI** por la API de Gemini
- **MongoDB Atlas** por la plataforma de base de datos
- **Comunidad Open Source** por las herramientas utilizadas

---

⭐ **Si este proyecto te resulta útil, ¡dale una estrella en GitHub!**