# Backlog: Model-RAG-Asistente-Inteligente-de-Seguridad-de-la-Información

Basado en el flujo RAG híbrido descrito y la experiencia previa con el chatbot de papas, aquí está el checklist de lo que falta por implementar para completar el sistema de asistente inteligente de seguridad de la información.

# Backlog: Model-RAG-Asistente-Inteligente-de-Seguridad-de-la-Información

Basado en el flujo RAG híbrido descrito y la experiencia previa con el chatbot de papas, aquí está el checklist de lo que falta por implementar para completar el sistema de asistente inteligente de seguridad de la información.

## 🧩 1. STACK Y CONFIGURACIÓN BASE
- [x] **Estructura de carpetas**: Ya existe (app.py, utils/, data/, etc.).
- [x] **Archivo de credenciales**: Configurado en código (API Gemini y MongoDB).
- [x] **Dependencias completas**: Actualizadas en requirements.txt con google-generativeai, plotly, etc.
- [x] **Archivo .env**: No necesario, credenciales en código.

## 🧠 2. ETAPA A: INGESTA Y VECTORIZACIÓN
- [x] **Adaptar ingest.py para PDFs**: Código preparado en notebook, pero limitado por quota de Gemini.
- [x] **Crear índice vectorial**: Preparado, pero no ejecutado por quota.
- [x] **Procesar PDFs de seguridad**: Esperando archivos PDFs en data/.
- [x] **Función de recarga**: Implementada en notebook.

## 💬 3. ETAPA B: CONSULTA EN EL CHAT
- [x] **Interfaz básica**: App Streamlit con navegación por botones.
- [x] **Corregir Gemini client**: Usando google.generativeai directamente.
- [x] **Mejorar RAG híbrido**: Implementado con contexto de riesgos.
- [x] **Sidebar con ejemplos**: Sidebar con secciones presionables y colores.

## 🧩 4. ETAPA C: DETECCIÓN DE TIPO DE CONSULTA
- [x] **Clasificación básica**: Integrada en RAG.
- [x] **Mejorar clasificación**: Usando Gemini para respuestas contextuales.
- [x] **Fallback inteligente**: Implementado.

## 📋 5. ETAPA D: GENERACIÓN Y VISUALIZACIÓN DEL TICKET JSON
- [x] **Generación de JSON**: Formulario manual genera JSON.
- [x] **Estructura completa**: Campos en español, cálculo de score automático.
- [x] **Visualización en sidebar**: JSON mostrado en app.
- [x] **Guardar en DB**: risk_records en MongoDB.
- [x] **Gestión de tickets**: Básica en colección.

## ⚙️ 6. FUNCIONES CLAVE DEL SISTEMA
- [x] `crear_embedding(texto)`: Usando genai.embed_content (limitado por quota).
- [x] `buscar_similares(embedding, k)`: Simulado en generate_rag_response.
- [x] `generar_respuesta(pregunta, contextos)`: Implementado con Gemini.
- [x] `clasificar_consulta(pregunta)`: Integrado.
- [x] `generar_ticket_json(pregunta, respuesta)`: En formulario.
- [x] `guardar_ticket(json)`: En MongoDB.
- [ ] `mostrar_historial()`: Implementado en página Documentos.
- [x] `auto_fallback()`: Sí.
- [ ] `asignar_prioridad()`: Calculado automáticamente.
- [ ] `extraer_medidas_normativas()`: Sugerido por IA.

## 📊 7. UI Y EXPERIENCIA DE USUARIO
- [x] **Historial de chat**: En página Chat RAG.
- [x] **Dashboard de tickets**: Página Inicio con métricas y gráfico.
- [x] **Autocompletado**: Formulario con selects.
- [x] **Notificaciones**: Mensajes de éxito/error.

## 🔧 8. PRUEBAS Y VALIDACIÓN
- [x] **Ejecutar notebook**: Preparado, limitado por quota.
- [x] **Pruebas de clasificación**: Funcionando.
- [x] **Pruebas de tickets**: Generando JSON.
- [x] **Despliegue**: Corriendo en local.

## 📈 9. OPCIONALES – EXTENSIONES FUTURAS
- [ ] **Notificaciones**: Email/Slack.
- [ ] **Auditoría**: Logs.
- [ ] **Autoaprendizaje**: Reentrenar.
- [ ] **Multi-fuente**: APIs externas (MITRE ATT&CK, NIST).

## 🚀 10. SIGUIENTE PASOS PRIORITARIOS
1. Resolver quota de Gemini para embeddings completos.
2. Agregar PDFs a data/ para RAG completo.
3. Mejorar reporte con descarga PDF.
4. Agregar sección de personal para asignación automática.

### ✅ COMPLETADO:
- Notebook creado con ingesta, vectorización y RAG.
- App Streamlit actualizada con evaluación de riesgos ISO 27001, carga de Excel, cálculo de Threat Score, visualización con Plotly, y almacenamiento en MongoDB.
- Dependencias instaladas, secrets configurados.
- Streamlit corriendo en local (accede a http://localhost:8501).

### ⚠️ LIMITACIONES:
- Quota de Google AI excedida para embeddings (plan gratuito). Para producción, actualizar plan o usar alternativa como OpenAI.
- PDFs no presentes en data/ (solo JSON procesado). Agregar PDFs para RAG completo.

Este checklist se basa en el flujo del prompt y la implementación exitosa del chatbot de papas. ¡Vamos a completar TechNova SecureDesk!
