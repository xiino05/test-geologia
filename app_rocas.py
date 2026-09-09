import streamlit as st
import unicodedata
import random

# Configuración de la página web (para que se vea bien en celular)
st.set_page_config(page_title="Test de Rocas", page_icon="🪨", layout="centered")

# Base de datos
elementos = [
    {"nombre": "Pizarra", "propiedades": ["brillo escaso", "textura laminar", "foliacion poco penetrativa"], "origen": "regional bajo grado"},
    {"nombre": "Filita", "propiedades": ["brillo notorio", "textura laminar", "compuesta principalmente por micas"], "origen": "regional bajo grado"},
    {"nombre": "Esquisto de micas", "propiedades": ["foliacion penetrativa", "textura esquistosa", "presencia de micas"], "origen": "regional bajo grado"},
    {"nombre": "Esquisto de granate", "propiedades": ["foliacion penetrativa", "textura esquistosa", "presencia de granates"], "origen": "regional alto grado"},
    {"nombre": "Gneiss", "propiedades": ["textura bandeada", "alternancia de bandas oscuras y claras", "tonalidad rosacea"], "origen": "regional alto grado"},
    {"nombre": "Mármol", "propiedades": ["textura bandeada", "efervescencia con hcl", "color claro"], "origen": "metamorfismo contacto"},
    {"nombre": "Gabro", "propiedades": ["alto contenido en piroxenos", "alto contenido en plagioclasas basicas", "textura faneritica"], "origen": "intrusiva"},
    {"nombre": "Basalto", "propiedades": ["textura afanitica", "color negro", "porosidades"], "origen": "extrusiva"},
    {"nombre": "Caliza", "propiedades": ["reaccion con hcl", "colores claros"], "origen": "medio quimico"},
    {"nombre": "Conglomerado", "propiedades": ["clastos redondeados", "seleccion mala"], "origen": "mecanico, transporte y sedimentacion"}
] # (Agregué algunas rocas, puedes completar la lista como en el código anterior)

def normalizar_texto(texto):
    texto = unicodedata.normalize('NFD', texto).encode('ascii', 'ignore').decode('utf-8')
    return texto.lower().strip()

# Inicializar la memoria del juego
if 'indice' not in st.session_state:
    random.shuffle(elementos)
    st.session_state.elementos = elementos
    st.session_state.indice = 0
    st.session_state.puntaje = 0
    st.session_state.totales = 0
    st.session_state.verificado = False

st.title("🎓 Simulador: Test de Rocas")

# Comprobar si el juego terminó
if st.session_state.indice >= len(st.session_state.elementos):
    st.success(f"¡Juego terminado! Tu puntaje final es {st.session_state.puntaje} de {st.session_state.totales}")
    if st.button("Jugar de nuevo"):
        st.session_state.clear()
        st.rerun()
else:
    roca_actual = st.session_state.elementos[st.session_state.indice]
    
    st.subheader(f"Roca a analizar: **{roca_actual['nombre'].upper()}**")
    
    # Formularios de ingreso
    p1 = st.text_input("Propiedad 1:", key=f"p1_{st.session_state.indice}")
    p2 = st.text_input("Propiedad 2:", key=f"p2_{st.session_state.indice}")
    
    p3 = ""
    if len(roca_actual["propiedades"]) == 3:
        p3 = st.text_input("Propiedad 3:", key=f"p3_{st.session_state.indice}")
        
    origen = st.text_input("Origen:", key=f"origen_{st.session_state.indice}")

    # Botón para verificar
    if not st.session_state.verificado:
        if st.button("Verificar Respuestas", type="primary"):
            st.session_state.verificado = True
            
            # Lógica de validación
            props_correctas = [normalizar_texto(p) for p in roca_actual["propiedades"]]
            respuestas = [p1, p2] if len(roca_actual["propiedades"]) == 2 else [p1, p2, p3]
            props_encontradas = []
            
            # Revisar propiedades
            for resp in respuestas:
                resp_norm = normalizar_texto(resp)
                acierto = False
                for prop in props_correctas:
                    if prop in resp_norm and prop not in props_encontradas:
                        st.session_state.puntaje += 1
                        props_encontradas.append(prop)
                        acierto = True
                        break
                st.session_state.totales += 1
                
            # Revisar origen
            origen_correcto = normalizar_texto(roca_actual["origen"])
            if origen_correcto in normalizar_texto(origen) and origen != "":
                st.session_state.puntaje += 1
            st.session_state.totales += 1
            
            st.rerun() # Recargar la página para mostrar resultados

    # Si ya se verificó, mostrar resultados y botón de siguiente
    if st.session_state.verificado:
        st.info("Respuestas registradas.")
        st.write(f"**Propiedades correctas eran:** {', '.join(roca_actual['propiedades'])}")
        st.write(f"**El origen correcto era:** {roca_actual['origen']}")
        
        if st.button("Siguiente Roca ➔"):
            st.session_state.verificado = False
            st.session_state.indice += 1
            st.rerun()

    st.write("---")
    st.markdown(f"### Puntaje: {st.session_state.puntaje} / {st.session_state.totales}")