import streamlit as st
from models.cv_model import AnalysisCV
from services.pdf_processor import text_extract_pdf
from services.cv_evaluator import evaluate_candidate

def main():
    """Función principal que define la interfaz de usuario de Streamlit"""
    
    st.set_page_config(
        page_title="Sistema de Evaluación de CVs",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("📄 Sistema de Evaluación de CVs con IA")
    st.markdown("""
    **Analiza currículums y evalúa candidatos de manera objetiva usando IA**
    
    Este sistema utiliza inteligencia artificial para:
    - Extraer información clave de currículums en PDF
    - Analizar la experiencia y habilidades del candidato
    - Evaluar el ajuste al puesto específico
    - Proporcionar recomendaciones objetivas de contratación
    """)
    
    st.divider()
    
    col_entrada, col_resultado = st.columns([1, 1], gap="large")
    
    with col_entrada:
        procesar_entrada()
    
    with col_resultado:
        mostrar_area_resultados()

def procesar_entrada():
    """Maneja la entrada de datos del usuario"""
    
    st.header("📋 Datos de Entrada")
    
    archivo_cv = st.file_uploader(
        "**1. Sube el CV del candidato (PDF)**",
        type=['pdf'],
        help="Selecciona un archivo PDF que contenga el currículum a evaluar. Asegúrate de que el texto sea legible y no esté en formato de imagen."
    )
    
    if archivo_cv is not None:
        st.success(f"✅ Archivo cargado: {archivo_cv.name}")
        st.info(f"📊 Tamaño: {archivo_cv.size:,} bytes")
    
    st.markdown("---")
    
    st.markdown("**2. Descripción del puesto de trabajo**")
    job_description = st.text_area(
        "Detalla los requisitos, responsabilidades y habilidades necesarias:",
        height=250,
        placeholder="""Ejemplo detallado:

            **Puesto:** Desarrollador Frontend Senior

            **Requisitos obligatorios:**
            - 3+ años de experiencia en desarrollo frontend
            - Dominio de React.js y JavaScript/TypeScript
            - Experiencia con HTML5, CSS3 y frameworks CSS (Bootstrap, Tailwind)
            - Conocimiento de herramientas de build (Webpack, Vite)

            **Requisitos deseables:**
            - Experiencia con Next.js o similares
            - Conocimientos de testing (Jest, Cypress)
            - Familiaridad con metodologías ágiles
            - Inglés intermedio-avanzado

            **Responsabilidades:**
            - Desarrollo de interfaces de usuario responsivas
            - Colaboración con equipos de diseño y backend
            - Optimización de rendimiento de aplicaciones web
            - Mantenimiento de código legacy""",
        help="Sé específico sobre requisitos técnicos, experiencia requerida y responsabilidades del puesto."
    )
    
    st.markdown("---")
    
    col_btn1, col_btn2 = st.columns([1, 1])
    
    with col_btn1:
        analizar = st.button(
            "🔍 Analizar Candidato", 
            type="primary",
            use_container_width=True
        )
    
    with col_btn2:
        if st.button("🗑️ Limpiar", use_container_width=True):
            st.rerun()
    
    st.session_state['archivo_cv'] = archivo_cv
    st.session_state['job_description'] = job_description
    st.session_state['analizar'] = analizar

def mostrar_area_resultados():
    """Muestra el área de resultados del análisis"""
    
    st.header("📊 Resultado del Análisis")
    
    if st.session_state.get('analizar', False):
        archivo_cv = st.session_state.get('archivo_cv')
        job_description = st.session_state.get('job_description', '').strip()
        
        if archivo_cv is None:
            st.error("⚠️ Por favor sube un archivo PDF con el currículum")
            return
            
        if not job_description:
            st.error("⚠️ Por favor proporciona una descripción detallada del puesto")
            return
        
        procesar_analisis(archivo_cv, job_description)
    else:
        st.info("""
        👆 **Instrucciones:**
        
        1. Sube un CV en formato PDF en la columna izquierda
        2. Describe detalladamente el puesto de trabajo
        3. Haz clic en "Analizar Candidato"
        4. Aquí aparecerá el análisis completo del candidato
        
        **Consejos para mejores resultados:**
        - Usa CVs con texto seleccionable (no imágenes escaneadas)
        - Sé específico en la descripción del puesto
        - Incluye tanto requisitos obligatorios como deseables
        """)

def procesar_analisis(archivo_cv, job_description):
    """Procesa el análisis completo del CV"""
    
    with st.spinner("🔄 Procesando currículum..."):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("📄 Extrayendo texto del PDF...")
        progress_bar.progress(25)
        
        text_cv = text_extract_pdf(archivo_cv)
        
        if text_cv.startswith("Error"):
            st.error(f"❌ {text_cv}")
            return
        
        status_text.text("🤖 Preparando análisis con IA...")
        progress_bar.progress(50)
        
        status_text.text("📊 Analizando candidato...")
        progress_bar.progress(75)
        
        resultado = evaluate_candidate(text_cv, job_description)
        
        status_text.text("✅ Análisis completado")
        progress_bar.progress(100)
        
        progress_bar.empty()
        status_text.empty()
        
        mostrar_resultados(resultado)

def mostrar_resultados(resultado: AnalysisCV):
    """Muestra los resultados del análisis de manera estructurada y profesional"""
    
    st.subheader("🎯 Evaluación Principal")
    
    if resultado.adjustment_percentage >= 80:
        color = "🟢"
        nivel = "EXCELENTE"
        mensaje = "Candidato altamente recomendado"
    elif resultado.adjustment_percentage >= 60:
        color = "🟡"
        nivel = "BUENO"
        mensaje = "Candidato recomendado con reservas"
    elif resultado.adjustment_percentage >= 40:
        color = "🟠"
        nivel = "REGULAR"
        mensaje = "Candidato requiere evaluación adicional"
    else:
        color = "🔴"
        nivel = "BAJO"
        mensaje = "Candidato no recomendado"
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.metric(
            label="Porcentaje de Ajuste al Puesto",
            value=f"{resultado.adjustment_percentage}%",
            delta=f"{color} {nivel}"
        )
        st.markdown(f"**{mensaje}**")
    
    st.divider()
    
    st.subheader("👤 Perfil del Candidato")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**👨‍💼 Nombre:** {resultado.name_candidate}")
        st.info(f"**⏱️ Experiencia:** {resultado.years_experience} años")
    
    with col2:
        st.info(f"**🎓 Educación:** {resultado.education}")
    
    st.subheader("💼 Experiencia Relevante")
    st.info(f"📋 **Resumen de experiencia:**\n\n{resultado.relevant_experience}")
    
    st.divider()
    
    st.subheader("🛠️ Habilidades Técnicas Clave")
    if resultado.key_skills:
        cols = st.columns(min(len(resultado.key_skills), 4))
        for i, habilidad in enumerate(resultado.key_skills):
            with cols[i % len(cols)]:
                st.success(f"✅ {habilidad}")
    else:
        st.warning("No se identificaron habilidades técnicas específicas")
    
    st.divider()
    
    col_fortalezas, col_mejoras = st.columns(2)
    
    with col_fortalezas:
        st.subheader("💪 Fortalezas Principales")
        if resultado.strengths:
            for i, strengths in enumerate(resultado.strengths, 1):
                st.markdown(f"**{i}.** {strengths}")
        else:
            st.info("No se identificaron fortalezas específicas")
    
    with col_mejoras:
        st.subheader("📈 Áreas de Desarrollo")
        if resultado.area_improvement:
            for i, area in enumerate(resultado.area_improvement, 1):
                st.markdown(f"**{i}.** {area}")
        else:
            st.info("No se identificaron áreas de mejora específicas")
    
    st.divider()
    
    st.subheader("📋 Recomendación Final")
    
    if resultado.adjustment_percentage >= 70:
        st.success("""
        ✅ **CANDIDATO RECOMENDADO**
        
        El perfil del candidato está bien alineado con los requisitos del puesto. 
        Se recomienda proceder con las siguientes etapas del proceso de selección.
        """)
    elif resultado.adjustment_percentage >= 50:
        st.warning("""
        ⚠️ **CANDIDATO CON POTENCIAL**
        
        El candidato muestra potencial pero requiere evaluación adicional. 
        Se recomienda una entrevista técnica para validar competencias específicas.
        """)
    else:
        st.error("""
        ❌ **CANDIDATO NO RECOMENDADO**
        
        El perfil no se alinea suficientemente con los requisitos del puesto. 
        Se recomienda continuar la búsqueda de candidatos más adecuados.
        """)
    
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("💾 Guardar Análisis", use_container_width=True):
            st.info("Funcionalidad de guardado - En desarrollo")