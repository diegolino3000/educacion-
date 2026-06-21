import streamlit as st
import random

st.set_page_config(page_title="Aprende Matemáticas", page_icon="📚", layout="wide")

# Inicialización
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'grade' not in st.session_state:
    st.session_state.grade = None
if 'subject' not in st.session_state:
    st.session_state.subject = "Matemáticas"
if 'progress' not in st.session_state:
    st.session_state.progress = {}
if 'current_level' not in st.session_state:
    st.session_state.current_level = None

# ==================== LOGIN ====================
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("🚀 Aprende Matemáticas")
        st.subheader("Bienvenido")

        tab1, tab2 = st.tabs(["🔑 Iniciar Sesión", "📝 Registrarse"])

        with tab1:
            username = st.text_input("Usuario", key="login_user")
            password = st.text_input("Contraseña", type="password", key="login_pass")
            if st.button("Iniciar Sesión", type="primary"):
                if username and password:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()

        with tab2:
            new_user = st.text_input("Elige un usuario", key="reg_user")
            new_pass = st.text_input("Elige una contraseña", type="password", key="reg_pass")
            if st.button("Registrarse", type="primary"):
                if new_user and new_pass:
                    st.session_state.logged_in = True
                    st.session_state.username = new_user
                    st.rerun()

else:
    st.title(f"📚 Aprende Matemáticas - {st.session_state.username}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"**Grado:** {st.session_state.grade or '—'}")
    with col2:
        st.write(f"**Materia:** {st.session_state.subject}")
    with col3:
        if st.button("🚪 Cerrar Sesión"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    st.divider()

    if not st.session_state.grade:
        st.header("📋 Información del estudiante")
        st.session_state.age = st.number_input("¿Cuántos años tienes?", 8, 13, 10)
        
        grade = st.radio("Grado", ["4° de primaria", "5° de primaria", "6° de primaria"], horizontal=True)
        st.session_state.grade = grade
        
        subject = st.radio("Materia", ["Matemáticas", "Inglés"], horizontal=True)
        st.session_state.subject = subject
        
        if st.button("Continuar al Mapa de Niveles", type="primary"):
            st.rerun()

    else:
        st.header("🗺️ Mapa de Niveles - 20 Niveles")

        secciones = ["Básicos", "Álgebra", "Geometría", "Estadística y Probabilidad"]
        
        for i, seccion in enumerate(secciones):
            st.subheader(f"📍 Sección {i+1}: {seccion}")
            cols = st.columns(5)
            
            for nivel in range(1, 6):
                with cols[nivel-1]:
                    nivel_id = f"{seccion}_{nivel}"
                    estrellas = st.session_state.progress.get(nivel_id, 0)
                    
                    desbloqueado = (nivel == 1) or st.session_state.progress.get(f"{seccion}_{nivel-1}", 0) == 3
                    
                    if desbloqueado:
                        if st.button(f"Nivel {nivel} {'⭐' * estrellas}", key=f"btn_{nivel_id}", use_container_width=True):
                            st.session_state.current_level = nivel_id
                            st.rerun()
                    else:
                        st.button(f"🔒 Nivel {nivel}", key=f"lock_{nivel_id}", disabled=True, use_container_width=True)

        # Evaluación
        if st.session_state.current_level:
            st.divider()
            seccion, nivel = st.session_state.current_level.split("_")
            st.header(f"✍️ {seccion} - Nivel {nivel}")

            preguntas = [
                {"q": "¿Cuánto es 45 + 37?", "o": ["72", "82", "92"], "r": "82"},
                {"q": "Si 3x = 24, ¿cuánto vale x?", "o": ["6", "8", "9"], "r": "8"},
                {"q": "Área de un rectángulo 6x4", "o": ["20", "24", "28"], "r": "24"},
                {"q": "¿Cuánto es 8 × 7?", "o": ["48", "56", "64"], "r": "56"},
                {"q": "2x + 5 = 15. ¿x=?", "o": ["x=5", "x=10", "x=15"], "r": "x=5"},
            ]
            
            p = random.choice(preguntas)
            st.write(f"**Pregunta:** {p['q']}")
            respuesta = st.radio("Elige la respuesta:", p["o"], key=f"q_{st.session_state.current_level}")
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("✅ Enviar respuesta", type="primary"):
                    if respuesta == p["r"]:
                        st.success("¡Correcto! +1 estrella ⭐")
                        current = st.session_state.progress.get(st.session_state.current_level, 0)
                        st.session_state.progress[st.session_state.current_level] = min(3, current + 1)
                    else:
                        st.error(f"Incorrecto. La respuesta es: **{p['r']}**")
                    st.rerun()
            with col_b:
                if st.button("❌ Salir del nivel"):
                    st.session_state.current_level = None
                    st.rerun()
