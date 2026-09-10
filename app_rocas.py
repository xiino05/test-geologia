import streamlit as st
import unicodedata
import random

# Configuración de la página web
st.set_page_config(page_title="Test de Rocas", page_icon="🪨", layout="centered")

# Base de datos completa
elementos = [
    # Rocas Metamórficas
    {"nombre": "Pizarra", "propiedades": ["brillo escaso", "textura laminar", "foliacion poco penetrativa"], "origen": "regional bajo grado"},
    {"nombre": "Filita", "propiedades": ["brillo notorio", "textura laminar", "compuesta principalmente por micas"], "origen": "regional bajo grado"},
    {"nombre": "Esquisto de micas", "propiedades": ["foliacion penetrativa", "textura esquistosa", "presencia de micas"], "origen": "regional bajo grado"},
    {"nombre": "Esquisto de granate", "propiedades": ["foliacion penetrativa", "textura esquistosa", "presencia de granates"], "origen": "regional alto grado"},
    {"nombre": "Gneiss", "propiedades": ["textura bandeada", "alternancia de bandas oscuras y claras", "tonalidad rosacea"], "origen": "regional alto grado"},
    {"nombre": "Mármol", "propiedades": ["textura bandeada", "efervescencia con hcl", "color claro"], "origen": "metamorfismo contacto"},
    
    # Rocas Ígneas
    {"nombre": "Gabro", "propiedades": ["alto contenido en piroxenos", "alto contenido en plagioclasas basicas", "textura faneritica"], "origen": "intrusiva"},
    {"nombre": "Diorita", "propiedades": ["presencia de micas", "alto contenido en plagioclasas intermedias", "color oscuro"], "origen": "intrusiva"},
    {"nombre": "Diorita Cuarcífera", "propiedades": ["presencia de micas", "alto contenido en plagioclasas intermedias", "color oscuro"], "origen": "intrusiva"},
    {"nombre": "Tonalita", "propiedades": ["poco feldespato potasico", "similar contenido de plagioclasa y cuarzo", "textura feneritica"], "origen": "intrusiva"},
    {"nombre": "Granodiorita", "propiedades": ["bajo contenido de feldespato potasico", "alto contenido de plagioclasa", "textura faneritica"], "origen": "intrusiva"},
    {"nombre": "Granito", "propiedades": ["equidad minerales formadores", "leve color rosado", "textura faneritica"], "origen": "intrusiva"},
    {"nombre": "Granito Alcalino", "propiedades": ["alto contenido feldespato potasico", "color rosado", "textura faneritica"], "origen": "intrusiva"},
    {"nombre": "Basalto", "propiedades": ["textura afanitica", "color negro", "porosidades"], "origen": "extrusiva"},
    {"nombre": "Andesita", "propiedades": ["textura porfidica", "fenocristales de plagioclasa", "bajo contenido de feldespato potasico"], "origen": "extrusiva"},
    {"nombre": "Toba", "propiedades": ["ligera", "porosa", "presencia de cristales"], "origen": "piroclastico"},
    {"nombre": "Pómez", "propiedades": ["ligera", "porosa", "textura vesicular"], "origen": "piroclastico"},
    
    # Rocas Sedimentarias
    {"nombre": "Lutita", "propiedades": ["grano fino", "fisibles", "pueden contener fosiles"], "origen": "mecanico, transporte y sedimentacion"},
    {"nombre": "Arenisca", "propiedades": ["porosa", "buena seleccion", "suele ser ligera"], "origen": "mecanico, transporte y sedimentacion"},
    {"nombre": "Conglomerado", "propiedades": ["clastos redondeados", "seleccion mala"], "origen": "mecanico, transporte y sedimentacion"},
    {"nombre": "Caliza", "propiedades": ["reaccion con hcl", "colores claros"], "origen": "medio quimico"},
    {"nombre": "Coquina", "propiedades": ["reaccion con hcl", "presencia de conchas de moluscos", "fragil"], "origen": "acumulacion de conchas"}
]

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
    st.session_state.resultado_actual = {} # Nuevo: Guarda el detalle de la pregunta actual

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
            
            props_correctas = [normalizar_texto(p) for p in roca_actual["propiedades"]]
            respuestas = [p1, p2] if len(roca_actual["propiedades"]) == 2 else [p1, p2, p3]
            
            props_encontradas = []
            analisis_props = []
            aciertos_pregunta = 0
            totales_pregunta = 0
            
            # Revisar propiedades
            for resp in respuestas:
                resp_norm = normalizar_texto(resp)
                acierto = False
                texto_mostrar = resp if resp.strip() != "" else "(En blanco)"
                
                for prop in props_correctas:
                    if prop in resp_norm and prop not in props_encontradas and resp_norm != "":
                        props_encontradas.append(prop)
                        acierto = True
                        break
                        
                analisis_props.append({"texto": texto_mostrar, "correcto": acierto})
                if acierto:
                    st.session_state.puntaje += 1
                    aciertos_pregunta += 1
                st.session_state.totales += 1
                totales_pregunta += 1
                
            # Revisar origen
            origen_correcto = normalizar_texto(roca_actual["origen"])
            resp_origen_norm = normalizar_texto(origen)
            acierto_origen = False
            texto_origen_mostrar = origen if origen.strip() != "" else "(En blanco)"
            
            if origen_correcto in resp_origen_norm and resp_origen_norm != "":
                acierto_origen = True
                st.session_state.puntaje += 1
                aciertos_pregunta += 1
            st.session_state.totales += 1
            totales_pregunta += 1
            
            # Guardar resultados de esta ronda en la memoria
            st.session_state.resultado_actual = {
                "props": analisis_props,
                "origen": {"texto": texto_origen_mostrar, "correcto": acierto_origen},
                "aciertos": aciertos_pregunta,
                "totales": totales_pregunta
            }
            
            st.rerun()

    # Si ya se verificó, mostrar resultados y botón de siguiente
    if st.session_state.verificado:
        res = st.session_state.resultado_actual
        
        # Conteo de la pregunta actual
        st.info(f"Desempeño en esta roca: **{res['aciertos']} correctas de {res['totales']} posibles.**")
        
        # Desglose visual de las respuestas del usuario
        st.markdown("### Tus respuestas:")
        for i, p in enumerate(res["props"]):
            simbolo = "✅" if p["correcto"] else "❌"
            st.write(f"- {simbolo} Propiedad {i+1}: {p['texto']}")
            
        simbolo_origen = "✅" if res["origen"]["correcto"] else "❌"
        st.write(f"- {simbolo_origen} Origen: {res['origen']['texto']}")
        
        st.write("---")
        # Respuestas esperadas (para retroalimentación)
        st.markdown("### Respuestas correctas esperadas:")
        st.write(f"**Propiedades:** {', '.join(roca_actual['propiedades'])}")
        st.write(f"**Origen:** {roca_actual['origen']}")
        
        if st.button("Siguiente Roca ➔"):
            st.session_state.verificado = False
            st.session_state.indice += 1
            st.session_state.resultado_actual = {}
            st.rerun()

    st.write("---")
    st.markdown(f"### Puntaje Total: {st.session_state.puntaje} / {st.session_state.totales}")