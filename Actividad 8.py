import PySimpleGUI as sg
import os
import matplotlib.pyplot as plt
import pandas as pdt

sg.theme("Dark Green3")


def guardar_usuario(usuario, password, archivo="usuarios.txt"):
    
    with open(archivo, "a") as file:
        file.write(f"{usuario},{password}\n")

def leer_usuarios(archivo="usuarios.txt"):
    
    usuarios = []
    try:
        with open(archivo, "r") as file:
            for linea in file:
                user, pwd = linea.strip().split(",")
                usuarios.append((user, pwd))
    except FileNotFoundError:
        with open(archivo, "w") as file:
            pass
    return usuarios

def verificar_usuario(usuario, password, archivo="usuarios.txt"):
    
    usuarios = leer_usuarios(archivo)
    return (usuario, password) in usuarios


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

def guardar_participante(participante, archivo="participantes.txt"):
    
    try:
        with open(archivo, "a") as file:
            file.write(
                f"{participante['evento']},{participante['tipo_documento']},{participante['numero_documento']},"
                f"{participante['telefono']},{participante['tipo_participante']},{participante['direccion']},"
                f"{participante['nombre']},{participante['imagen']}\n"
            )
    except Exception as e:
        print(f"Error al guardar el participante: {e}")


def cargar_participantes(archivo="participantes.txt"):
    
    participantes = []
    try:
        with open(archivo, "r") as file:
            for linea in file:
                datos = linea.strip().split(",")
                if len(datos) != 8:
                    
                    continue
                evento, tipo_documento, numero_documento, telefono, tipo_participante, direccion, nombre, imagen = datos
                participantes.append({
                    "evento": evento,
                    "tipo_documento": tipo_documento,
                    "numero_documento": numero_documento,
                    "telefono": telefono,
                    "tipo_participante": tipo_participante,
                    "direccion": direccion,
                    "nombre": nombre,
                    "imagen": imagen
                })
    except FileNotFoundError:
        print("El archivo participantes.txt no existe. Creando uno vacío...")
        open(archivo, "w").close()
    except Exception as e:
        print(f"Error al cargar participantes: {e}")
    return participantes



participantes = cargar_participantes()


def participantes_todos_los_eventos(participantes, eventos):
   
    todos_los_eventos = {evento["nombre"] for evento in eventos}
    return [
        p["nombre"] for p in participantes
        if {p["evento"] for p in participantes if p["nombre"] == p["nombre"]} == todos_los_eventos
    ]


def participantes_al_menos_un_evento(participantes):
    
    return list({p["nombre"] for p in participantes})


def participantes_solo_primer_evento(participantes, eventos):
  
    if not eventos:
        return []
    primer_evento = eventos[0]["nombre"]
    return [
        p["nombre"] for p in participantes
        if p["evento"] == primer_evento and sum(1 for x in participantes if x["nombre"] == p["nombre"]) == 1
    ]

config_file = "configuracion.txt"

def cargar_configuracion():
    configuracion = {
        "validar_aforo": True,
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
       
        pass
    return configuracion


def guardar_configuracion(config):
    with open(config_file, "w") as f:
        for clave, valor in config.items():
            f.write(f"{clave}={valor}\n")


configuracion = cargar_configuracion()
eventos = cargar_eventos()  
 

def ventana_login():
    layout_login = [
        [sg.Text("Usuario"), sg.InputText(key="usuario")],
        [sg.Text("Contraseña"), sg.InputText(key="password", password_char="*")],
        [sg.Button("Iniciar Sesión"), sg.Button("Cancelar")],
    ]
    return sg.Window("Login", layout_login)


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


layoutConfiguracion = [
    [sg.Checkbox("Validar Aforo al agregar participantes", key="validar_aforo", default=configuracion["validar_aforo"])],
    [sg.Checkbox("Solicitar Imagenes", key="solicitar_imagenes", default=configuracion["solicitar_imagenes"])],
    [sg.Checkbox("Modificar Registros", key="modificar_registros", default=configuracion["modificar_registros"])],
    [sg.Checkbox("Eliminar Registros", key="eliminar_registros", default=configuracion["eliminar_registros"])],
    [sg.Button("Guardar Configuracion", key="guardar_configuracion")],
]

layoutAnalisis = [
    [sg.Text("Participantes que fueron a todos los eventos")],
    [sg.Listbox(values=[],size=(40, 5), key="TodosLosEventos", disabled=True)],

    [sg.Text("Participantes que fueron al menos a un evento")],
    [sg.Listbox(values=[],size=(40, 5), key="AlMenosUnEvento", disabled=True)],

    [sg.Text("Participantes que fueron solo al primer evento")],
    [sg.Listbox(values=[],size=(40, 5), key="SoloPrimerEvento", disabled=True)],
]


tabEventos = sg.Tab("Eventos", layoutEventos)
tabParticipantes = sg.Tab("Participantes", layoutParticipantes)
tabConfiguracion = sg.Tab("Configuracion", layoutConfiguracion)
tabAnalisis = sg.Tab("Análisis", layoutAnalisis)



def ventana_principal():
    layout = [[sg.TabGroup([[tabEventos, tabParticipantes,tabAnalisis, tabConfiguracion]])]]
    return sg.Window("LA COP 16", layout)
	
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


while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        guardar_evento(eventos)  
        break

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
            window["COMBO"].update(values=[e["nombre"] for e in eventos])  
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
            window["COMBO"].update(values=[e["nombre"] for e in eventos])  
            sg.popup("Evento modificado con éxito.")

    if event == "EliminarEventos":
        seleccionado = values["LISTA"]
        if seleccionado:
            index = [e["nombre"] for e in eventos].index(seleccionado[0])
            del eventos[index]
            window["LISTA"].update([e["nombre"] for e in eventos])
            window["COMBO"].update(values=[e["nombre"] for e in eventos])  
            sg.popup("Evento eliminado con éxito.")

    if event == "Agregar":
        try:
           
            evento = values["COMBO"]
            tipo_documento = values["TipoDocumento"]
            numero_documento = values["NumeroDocumento"]
            telefono = values["TELEFONO"]
            tipo_participante = values["TipoParticipante"]
            direccion = values["Direccion"]
            nombre = values["NAME"]
            imagen = values["FileParticipantes"]

           
            if not all([evento, tipo_documento, numero_documento, telefono, tipo_participante, direccion, nombre]):
                raise ValueError("Todos los campos son obligatorios.")

            if not numero_documento.isdigit():
                raise ValueError("El número de documento debe ser un valor numérico.")

            if imagen and not os.path.exists(imagen):
                raise FileNotFoundError("No se encontró la imagen seleccionada.")

            
            if any(p["numero_documento"] == numero_documento for p in participantes):
                raise ValueError("Ya existe un participante con este número de documento.")

            
            if configuracion["validar_aforo"]:
                evento_seleccionado = next((e for e in eventos if e["nombre"] == evento), None)
                if evento_seleccionado:
                    inscritos = sum(1 for p in participantes if p["evento"] == evento)
                    if inscritos >= evento_seleccionado["cupo"]:
                        raise ValueError("No hay cupos disponibles para este evento.")

            
            nuevo_participante = {
                "evento": evento,
                "tipo_documento": tipo_documento,
                "numero_documento": numero_documento,
                "telefono": telefono,
                "tipo_participante": tipo_participante,
                "direccion": direccion,
                "nombre": nombre,
                "imagen": imagen
            }
            participantes.append(nuevo_participante)
            guardar_participante(nuevo_participante)
            window["ListaParticipantes"].update([p["nombre"] for p in participantes if p["evento"] == evento])
            sg.popup("Participante agregado con éxito.")
        except Exception as e:
            sg.popup_error(f"Error al agregar participante: {e}")

    if event == "Modificar":
        
        try:
            seleccionado = values["ListaParticipantes"]
            if not seleccionado:
                raise ValueError("Debe seleccionar un participante para modificar.")

            index = next(
                (i for i, p in enumerate(participantes) if p["nombre"] == seleccionado[0] and p["evento"] == values["COMBO"]),
                None
            )
            if index is None:
                raise ValueError("Participante no encontrado.")

           
            participantes[index]["tipo_documento"] = values["TipoDocumento"] or participantes[index]["tipo_documento"]
            participantes[index]["numero_documento"] = values["NumeroDocumento"] or participantes[index]["numero_documento"]
            participantes[index]["telefono"] = values["TELEFONO"] or participantes[index]["telefono"]
            participantes[index]["tipo_participante"] = values["TipoParticipante"] or participantes[index]["tipo_participante"]
            participantes[index]["direccion"] = values["Direccion"] or participantes[index]["direccion"]
            participantes[index]["nombre"] = values["NAME"] or participantes[index]["nombre"]
            participantes[index]["imagen"] = values["FileParticipantes"] or participantes[index]["imagen"]

         
            with open("participantes.txt", "w") as file:
                for p in participantes:
                    guardar_participante(p, archivo="participantes.txt")
            window["ListaParticipantes"].update([p["nombre"] for p in participantes if p["evento"] == values["COMBO"]])
            sg.popup("Participante modificado con éxito.")
        except Exception as e:
            sg.popup_error(f"Error al modificar participante: {e}")


    if event == "Eliminar":
        
        try:
            seleccionado = values["ListaParticipantes"]
            if not seleccionado:
                raise ValueError("Debe seleccionar un participante para eliminar.")

            participantes = [p for p in participantes if not (p["nombre"] == seleccionado[0] and p["evento"] == values["COMBO"])]


            with open("participantes.txt", "w") as file:
                for p in participantes:
                    guardar_participante(p, archivo="participantes.txt")
            window["ListaParticipantes"].update([p["nombre"] for p in participantes if p["evento"] == values["COMBO"]])
            sg.popup("Participante eliminado con éxito.")

        except Exception as e:
            sg.popup_error(f"Error al eliminar participante: {e}")
            
    if event == "Guardar Configuracion":
       
        guardar_configuracion(values)
        sg.popup("Configuración guardada exitosamente.", title="Guardado")

    
    if event == "ActualizarAnálisis":
        try:
          
            todos_los_eventos = participantes_todos_los_eventos(participantes, eventos)
            al_menos_un_evento = participantes_al_menos_un_evento(participantes)
            solo_primer_evento = participantes_solo_primer_evento(participantes, eventos)

            window["TodosLosEventos"].update("\n".join(todos_los_eventos))
            window["AlMenosUnEvento"].update("\n".join(al_menos_un_evento))
            window["SoloPrimerEvento"].update("\n".join(solo_primer_evento))

        except Exception as e:
            sg.popup_error(f"Error al actualizar el análisis: {e}")

data_participantes = {
    'Nombre': ['Juan', 'Ana', 'Luis', 'María', 'Pedro', 'Laura', 'Carlos', 'Sofía', 'Jorge'],
    'Tipo': ['Estudiante', 'Profesor', 'Estudiante', 'Profesor', 'Estudiante', 'Estudiante', 'Profesor', 'Estudiante', 'Estudiante'],
    'Evento': ['Evento A', 'Evento A', 'Evento B', 'Evento B', 'Evento C', 'Evento C', 'Evento A', 'Evento B', 'Evento C']
}

data_eventos = {
    'Evento': ['Evento A', 'Evento B', 'Evento C'],
    'Fecha': ['2023-11-01', '2023-11-05', '2023-11-10']
}

df_participantes = pdt.DataFrame(data_participantes)
df_eventos = pdt.DataFrame(data_eventos)


def distribucion_participantes(ax):
   
    data = df_participantes['Tipo'].value_counts()
    ax.pie(data, labels=data.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    ax.set_title('Distribución de participantes por tipo')

def participantes_por_evento(ax):
    
    data = df_participantes['Evento'].value_counts()
    ax.bar(data.index, data.values, color='green')
    ax.set_title('Participantes por evento')
    ax.set_xlabel('Evento')
    ax.set_ylabel('Cantidad de participantes')

def eventos_por_fecha(ax):
  
    eventos_por_fecha = df_eventos['Fecha'].value_counts()
    ax.barh(eventos_por_fecha.index, eventos_por_fecha.values, color='lightgreen')
    ax.set_title('Eventos por fecha')
    ax.set_xlabel('Cantidad de eventos')
    ax.set_ylabel('Fecha')


def crear_layout_graficos():
    
    fig, axs = plt.subplots(3, 1, figsize=(8, 15))  

   
    distribucion_participantes(axs[0])
    participantes_por_evento(axs[1])
    eventos_por_fecha(axs[2])

    
    plt.tight_layout()
    plt.show()


crear_layout_graficos()

