import PySimpleGUI as sg
import os

sg.theme("Dark Green3")


def guardar_usuario(usuario, password, archivo="usuarios.txt"):
    """Guarda un usuario y contraseña en el archivo de texto."""
    with open(archivo, "a") as file:
        file.write(f"{usuario},{password}\n")

def leer_usuarios(archivo="usuarios.txt"):
    """Lee los usuarios del archivo y los devuelve como una lista de pares (usuario, contraseña)."""
    usuarios = []
    try:
        with open(archivo, "r") as file:
            for linea in file:
                user, pwd = linea.strip().split(",")
                usuarios.append((user, pwd))
    except FileNotFoundError:
        with open(archivo, "w") as file:  # Crear archivo vacío si no existe
            pass
    return usuarios

def verificar_usuario(usuario, password, archivo="usuarios.txt"):
    """Verifica si un usuario y contraseña existen en el archivo."""
    usuarios = leer_usuarios(archivo)
    return (usuario, password) in usuarios

# --- Funciones para manejar eventos ---
def guardar_evento(nombre, fecha, hora, lugar, cupo, imagen):
    try:
        with open("eventos.txt", "a") as archivo:
            archivo.write(f"{nombre},{fecha},{hora},{lugar},{cupo},{imagen}\n")
    except Exception as e:
        print(f"Error al guardar el evento: {e}")


def cargar_eventos():
    try:
        eventos = []
        with open("eventos.txt", "r") as archivo:
            for linea in archivo:
                datos = linea.strip().split(",")
                if len(datos) != 6:
                    print(f"Línea inválida: {linea.strip()}")
                    continue
                nombre, fecha, hora, lugar, cupo, imagen = datos
                eventos.append({
                    "nombre": nombre,
                    "fecha": fecha,
                    "hora": hora,
                    "lugar": lugar,
                    "cupo": int(cupo),
                    "imagen": imagen
                })
        return eventos
    except FileNotFoundError:
        print("El archivo eventos.txt no existe.")
        return []
    except Exception as e:
        print(f"Error al cargar eventos: {e}")
        return []


config_file = "configuracion.txt"

# Función para cargar la configuración desde el archivo TXT
def cargar_configuracion():
    configuracion = {
        "validar_aforo": False,
        "solicitar_imagenes": False,
        "modificar_registros": False,
        "eliminar_registros": False,
    }
    try:
        with open(config_file, "r") as f:
            for linea in f:
                clave, valor = linea.strip().split("=")
                configuracion[clave] = valor == "True"
    except FileNotFoundError:
        # Si el archivo no existe, devolver configuraciones por defecto
        pass
    return configuracion

# Función para guardar la configuración en el archivo TXT
def guardar_configuracion(config):
    with open(config_file, "w") as f:
        for clave, valor in config.items():
            f.write(f"{clave}={valor}\n")

# Cargar la configuración inicial
configuracion = cargar_configuracion()

# --- Cargar eventos al iniciar ---
eventos = cargar_eventos()  # Cargar eventos desde el archivo
participantes = []  # Lista de participantes como diccionarios

# --- Ventana de Login ---
def ventana_login():
    layout_login = [
        [sg.Text("Usuario"), sg.InputText(key="usuario")],
        [sg.Text("Contraseña"), sg.InputText(key="password", password_char="*")],
        [sg.Button("Iniciar Sesión"), sg.Button("Cancelar")],
    ]
    return sg.Window("Login", layout_login)

# --- Layout para la pestaña de Eventos ---
layoutEventos = [
    [sg.Text("Nombre Evento"), sg.InputText(key="NameEvent")],
    [sg.Text("Fecha"), sg.InputText(key="DATE")],
    [sg.Text("Hora"), sg.InputText(key="TIME")],
    [sg.Text("Lugar"), sg.InputText(key="PLACE")],
    [sg.Text("Cupo"), sg.InputText(key="CUPO")],
    [sg.Text('Agrega Imagen'), sg.Input(key='FileEventos', enable_events=True), sg.FileBrowse(key="Buscar")],
    [sg.Button('AgregarEventos'), sg.Button('ModificarEventos'), sg.Button('EliminarEventos')],
    [sg.Listbox(values=[e["nombre"] for e in eventos], size=(40, 10), key="LISTA", enable_events=True)],
    [sg.Image(key="ImagenEventos")],
]

# --- Layout para la pestaña de Participantes ---
layoutParticipantes = [
    [sg.Text("Evento"), sg.Combo([e["nombre"] for e in eventos], key="COMBO")],
    [sg.Text("Tipo Documento"), sg.InputText(key="TipoDocumento")],
    [sg.Text("Numero Documento"), sg.InputText(key="NumeroDocumento")],
    [sg.Text("Telefono"), sg.InputText(key="TELEFONO")],
    [sg.Text("Tipo Participante"), sg.Combo(["Estudiante", "Profesor", "Otro"], key="TipoParticipante")],
    [sg.Text("Direccion"), sg.InputText(key="Direccion")],
    [sg.Text("Nombre"), sg.InputText(key="NAME")],
    [sg.Text('Agrega Imagen'), sg.Input(key='FileParticipantes', enable_events=True), sg.FileBrowse(key="Buscar")],
    [sg.Button("Agregar"), sg.Button("Modificar"), sg.Button("Eliminar")],
    [sg.Listbox(values=[], size=(40, 10), key="ListaParticipantes", enable_events=True)],
    [sg.Image(key="ImagenParticipantes")],
]

# --- Layout para la pestaña de Configuración ---
layoutConfiguracion = [
    [sg.Checkbox("Validar Aforo al agregar participantes", key="validar_aforo", default=configuracion["validar_aforo"])],
    [sg.Checkbox("Solicitar Imagenes", key="solicitar_imagenes", default=configuracion["solicitar_imagenes"])],
    [sg.Checkbox("Modificar Registros", key="modificar_registros", default=configuracion["modificar_registros"])],
    [sg.Checkbox("Eliminar Registros", key="eliminar_registros", default=configuracion["eliminar_registros"])],
    [sg.Button("Guardar Configuración", key="guardar_configuracion")],
]

tabEventos = sg.Tab("Eventos", layoutEventos)
tabParticipantes = sg.Tab("Participantes", layoutParticipantes)
tabConfiguracion = sg.Tab("Configuracion", layoutConfiguracion)

# --- Ventana Principal ---
def ventana_principal():
    layout = [[sg.TabGroup([[tabEventos, tabParticipantes, tabConfiguracion]])]]
    return sg.Window("LA COP 16", layout)

# --- Lógica Principal ---
window_login = ventana_login()

while True:
    event, values = window_login.read()

    if event == sg.WIN_CLOSED or event == "Cancelar":
        break

    if event == "Iniciar Sesión":
        usuario = values["usuario"]
        password = values["password"]
        if verificar_usuario(usuario, password):
            sg.popup("Login exitoso")
            window_login.close()
            window = ventana_principal()
            break
        else:
            sg.popup_error("Usuario o contraseña incorrectos")

# --- Loop de la Ventana Principal ---
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        guardar_evento(eventos)  # Guardar eventos al cerrar
        break

    # ----- Funcionalidad para Eventos -----
    if event == "AgregarEventos":
        nombre = values["NameEvent"]
        fecha = values["DATE"]
        hora = values["TIME"]
        lugar = values["PLACE"]
        cupo = values["CUPO"]
        imagen = values["FileEventos"]

        guardar_evento(nombre, fecha, hora, lugar, cupo, imagen)


        try:
            if not nombre or not fecha or not hora or not lugar or not cupo:
                raise ValueError("Todos los campos son obligatorios.")

            if not cupo.isdigit():
                raise ValueError("El campo 'Cupo' debe ser un número.")

            if nombre in [e["nombre"] for e in eventos]:
                raise ValueError("El evento ya existe.")

            if imagen and not os.path.exists(imagen):
                raise FileNotFoundError("No se encontró la imagen seleccionada.")

            eventos.append({
                "nombre": nombre,
                "fecha": fecha,
                "hora": hora,
                "lugar": lugar,
                "cupo": int(cupo),
                "imagen": imagen
            })
            window["LISTA"].update([e["nombre"] for e in eventos])
            window["COMBO"].update(values=[e["nombre"] for e in eventos])  # Actualiza el ComboBox de participantes
            sg.popup("Evento agregado con éxito.")
        except Exception as e:
            sg.popup_error(f"Error al agregar evento: {e}")

    if event == "ModificarEventos":
        seleccionado = values["LISTA"]
        if seleccionado:
            index = [e["nombre"] for e in eventos].index(seleccionado[0])
            evento = eventos[index]
            evento["nombre"] = values["NameEvent"] or evento["nombre"]
            evento["fecha"] = values["DATE"] or evento["fecha"]
            evento["hora"] = values["TIME"] or evento["hora"]
            evento["lugar"] = values["PLACE"] or evento["lugar"]
            evento["cupo"] = int(values["CUPO"]) if values["CUPO"].isdigit() else evento["cupo"]
            evento["imagen"] = values["FileEventos"] or evento["imagen"]
            window["LISTA"].update([e["nombre"] for e in eventos])
            window["COMBO"].update(values=[e["nombre"] for e in eventos])  # Actualiza el ComboBox de participantes
            sg.popup("Evento modificado con éxito.")

    if event == "EliminarEventos":
        seleccionado = values["LISTA"]
        if seleccionado:
            index = [e["nombre"] for e in eventos].index(seleccionado[0])
            del eventos[index]
            window["LISTA"].update([e["nombre"] for e in eventos])
            window["COMBO"].update(values=[e["nombre"] for e in eventos])  # Actualiza el ComboBox de participantes
            sg.popup("Evento eliminado con éxito.")





