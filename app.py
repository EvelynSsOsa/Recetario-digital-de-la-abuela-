import streamlit as st
from pathlib import Path
import os
import shutil ## invetigar para que era que se ocupaba este libreria de aquí, según yo para eliminar algo

# Configuración de la página
st.set_page_config(
    page_title="Mi Recetario",
    page_icon="📖",
    layout="wide"
)


# Funciones de la lógica de negocio (prácticamente iguales)
def rutas():
    """Obtiene la ruta base del recetario"""
    dep_rutas = os.getcwd()
    ruta_rece = Path(dep_rutas, "recetario")
    ruta_rece.mkdir(exist_ok=True)
    return ruta_rece

def crear_categoria(rutas):
    with st.form("crear_categoria_form"):
        nueva_categoria = st.text_input("Nombre de la nueva categoria: ")
        submitted = st.form_submit_button("Crear categoria")

        if submitted and nueva_categoria:
            cate_nue = rutas/ nueva_categoria
            cate_nue.mkdir(exist_ok=True)
            st.success(f"¡Categoria '{nueva_categoria}' creada con éxito!")
            return cate_nue
        elif submitted:
            st.warning("Por favor, ingresa un nombre para la categoria")
    return None

def crear_receta(ruta_categoria):
    """Crea una nueva receta en la categoría seleccionada"""
    with st.form("crear_receta_form"):
        nota = st.text_input("📝 Nombre de la receta:")

        st.write("📋 Ingresa tu receta paso a paso:")
        recetita = []

        # Usamos un área de texto para ingresar la receta completa
        receta_texto = st.text_area(
            "Escribe tu receta (un paso por línea):",
            height=200,
            placeholder="Ejemplo:\n1. Picar la cebolla\n2. Sofreír los ingredientes\n3. Cocinar a fuego lento..."
        )

        submitted = st.form_submit_button("💾 Guardar receta")

        if submitted and nota and receta_texto:
            # Dividir el texto en líneas
            recetita = [linea for linea in receta_texto.split('\n') if linea.strip()]

            # Formatear la receta
            receta_completa = nota + "\n" + "=" * 40 + "\n\n" + "\n".join(recetita)

            # Guardar la receta
            receta_nueva = ruta_categoria / f"{nota}.txt"

            # Verificar si ya existe
            if receta_nueva.exists():
                st.warning("⚠️ Ya existe una receta con ese nombre. ¿Quieres sobrescribirla?")
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("Sí, sobrescribir"):
                        with open(receta_nueva, "w") as archivo:
                            archivo.write(receta_completa)
                        st.success(f"✅ ¡Receta '{nota}' actualizada con éxito!")
                with col2:
                    if st.form_submit_button("No, cancelar"):
                        st.info("Operación cancelada")
            else:
                with open(receta_nueva, "w") as archivo:
                    archivo.write(receta_completa)
                st.success(f"✅ ¡Receta '{nota}' guardada con éxito!")
                return receta_nueva
        elif submitted:
            st.warning("⚠️ Por favor, ingresa un nombre y el contenido de la receta.")
    return None


def seleccionar_categoria(categorias):
    """Muestra y permite seleccionar una categoría"""
    # Obtener todas las categorías
    categorias_lista = [cate.name for cate in categorias.iterdir() if cate.is_dir()]

    if not categorias_lista:
        st.warning("📂 No hay categorías disponibles. ¡Crea una primero!")
        return None

    # Selector de categoría
    cate_seleccionada = st.selectbox(
        "📁 Selecciona una categoría:",
        categorias_lista
    )

    if cate_seleccionada:
        selecion_categoria = categorias / cate_seleccionada
        return selecion_categoria
    return None


def seleccionar_receta(cate_selec):
    """Selecciona una receta de la categoría"""
    if not cate_selec or not cate_selec.exists():
        return None

    recetas = [rec.name.replace('.txt', '') for rec in cate_selec.glob("*.txt")]

    if not recetas:
        st.info("📭 Aún no has creado ninguna receta en esta categoría.")
        return None

    # Selector de receta
    receta_seleccionada = st.selectbox(
        "📖 Selecciona una receta:",
        recetas
    )

    if receta_seleccionada:
        receta_lectura = cate_selec / f"{receta_seleccionada}.txt"
        return receta_lectura
    return None


def leer_receta(receta_seleccionada):
    """Lee y muestra el contenido de una receta"""
    if receta_seleccionada and receta_seleccionada.exists():
        with open(receta_seleccionada, "r") as archivo:
            contenido = archivo.read()
        return contenido
    return None


def eliminar_receta(receta_seleccionada):
    """Elimina una receta"""
    if receta_seleccionada and receta_seleccionada.exists():
        # Confirmación antes de eliminar
        if st.button("🗑️ Confirmar eliminación", type="primary"):
            receta_seleccionada.unlink()
            st.success("✅ ¡Receta eliminada con éxito!")
            st.rerun()
    else:
        st.warning("⚠️ No hay ninguna receta seleccionada para eliminar.")


def eliminar_categoria(categoria_seleccionada):
    """Elimina una categoría completa"""
    if categoria_seleccionada and categoria_seleccionada.exists():
        # Verificar si tiene recetas
        recetas = list(categoria_seleccionada.glob("*.txt"))
        if recetas:
            st.warning(f"⚠️ Esta categoría contiene {len(recetas)} receta(s). Se eliminarán también.")

        # Confirmación antes de eliminar
        if st.button("🗑️ Confirmar eliminación de categoría", type="primary"):
            shutil.rmtree(categoria_seleccionada)
            st.success("✅ ¡Categoría eliminada con éxito!")
            st.rerun()
    else:
        st.warning("⚠️ No hay ninguna categoría seleccionada para eliminar.")


# Interfaz principal de Streamlit
def main():
    # Título y descripción
    st.title("📖 Mi Recetario Personal")
    st.markdown("---")

    # Sidebar con menú de navegación
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2933/2933244.png", width=100)
        st.title("📚 Menú Principal")

        opcion = st.radio(
            "¿Qué quieres hacer hoy?",
            ["📖 Leer receta", "✍️ Crear receta", "📁 Crear categoría",
             "🗑️ Eliminar receta", "🗂️ Eliminar categoría", "ℹ️ Acerca de"]
        )

        st.markdown("---")
        st.caption("Tu recetario digital personal 📖")

    # Contenido principal según la opción seleccionada
    base = rutas()

    if opcion == "📖 Leer receta":
        st.header("📖 Leer una receta")

        cat = seleccionar_categoria(base)
        if cat:
            receta = seleccionar_receta(cat)
            if receta:
                contenido = leer_receta(receta)
                if contenido:
                    st.markdown("---")
                    # Mostrar la receta en un formato bonito
                    st.subheader(f"📝 {receta.stem}")

                    # Dividir título y contenido
                    lineas = contenido.split('\n')
                    if len(lineas) > 1:
                        st.markdown(f"**{lineas[0]}**")
                        st.markdown("---")
                        contenido_receta = '\n'.join(lineas[2:]) if len(lineas) > 2 else ''
                        st.markdown(contenido_receta)
                    else:
                        st.markdown(contenido)

    elif opcion == "✍️ Crear receta":
        st.header("✍️ Crear una nueva receta")

        cat = seleccionar_categoria(base)
        if cat:
            crear_receta(cat)

    elif opcion == "📁 Crear categoría":
        st.header("📁 Crear una nueva categoría")
        crear_categoria(base)

    elif opcion == "🗑️ Eliminar receta":
        st.header("🗑️ Eliminar una receta")

        cat = seleccionar_categoria(base)
        if cat:
            receta = seleccionar_receta(cat)
            if receta:
                st.warning(f"⚠️ ¿Estás seguro de que quieres eliminar la receta '{receta.stem}'?")
                eliminar_receta(receta)

    elif opcion == "🗂️ Eliminar categoría":
        st.header("🗂️ Eliminar una categoría")

        cat = seleccionar_categoria(base)
        if cat:
            st.warning(f"⚠️ ¿Estás seguro de que quieres eliminar la categoría '{cat.name}'?")
            eliminar_categoria(cat)

    elif opcion == "ℹ️ Acerca de":
        st.header("ℹ️ Acerca de Mi Recetario")
        st.markdown("""
        ### 📖 Mi Recetario Personal

        Una aplicación para gestionar tus recetas de cocina de manera fácil y organizada.

        **Características:**
        - 📁 Organiza tus recetas por categorías
        - ✍️ Crea y edita tus recetas fácilmente
        - 📖 Lee tus recetas con un formato limpio
        - 🗑️ Elimina recetas y categorías que ya no necesites

        **Tecnologías utilizadas:**
        - Python 🐍
        - Streamlit 🎈
        - Pathlib para manejo de archivos 📁

        ¡Disfruta cocinando! 🍳
        """)

    # Mostrar estadísticas en el sidebar
    with st.sidebar:
        st.markdown("---")
        st.subheader("📊 Estadísticas")

        # Contar categorías y recetas
        if base.exists():
            categorias = [c for c in base.iterdir() if c.is_dir()]
            total_recetas = 0
            for cat in categorias:
                recetas = list(cat.glob("*.txt"))
                total_recetas += len(recetas)

            st.metric("📁 Categorías", len(categorias))
            st.metric("📖 Recetas", total_recetas)


if __name__ == "__main__":
    main()
