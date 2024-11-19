from fastapi import FastAPI, UploadFile, File, Form
from typing import Optional
import os
import uuid

# Creación del servidor
app = FastAPI()

# Definición de la base de usuarios simulada
usuarios = [
    {
        "id": 0,
        "nombre": "Homero Simpson",
        "edad": 40,
        "domicilio": "Av. Siempre Viva",
    },
    {
        "id": 1,
        "nombre": "Marge Simpson",
        "edad": 38,
        "domicilio": "Av. Siempre Viva",
    },
    {
        "id": 2,
        "nombre": "Lisa Simpson",
        "edad": 8,
        "domicilio": "Av. Siempre Viva",
    },
    {
        "id": 3,
        "nombre": "Bart Simpson",
        "edad": 10,
        "domicilio": "Av. Siempre Viva",
    },
]

@app.post("/fotos")
async def guarda_foto(
    nombre: str = Form(...),
    direccion: str = Form(...),
    foto: UploadFile = File(...),
    vip: Optional[bool] = Form(False)
):
    # Definir rutas base para fotos
    home_usuario = os.path.expanduser("~")
    ruta_base_vip = os.path.join(home_usuario, "fotos-usuarios-vip")
    ruta_base_no_vip = os.path.join(home_usuario, "fotos-usuarios")

    # Crear carpetas si no existen
    os.makedirs(ruta_base_vip, exist_ok=True)
    os.makedirs(ruta_base_no_vip, exist_ok=True)

    # Determinar ruta según si el usuario es VIP
    ruta_base = ruta_base_vip if vip else ruta_base_no_vip

    # Generar nombre único para el archivo
    nombre_archivo = f"{uuid.uuid4()}{os.path.splitext(foto.filename)[1]}"
    ruta_imagen = os.path.join(ruta_base, nombre_archivo)

    # Guardar el archivo
    with open(ruta_imagen, "wb") as archivo_foto:
        contenido = await foto.read()
        archivo_foto.write(contenido)

    print("Datos recibidos:")
    print(f"  Nombre: {nombre}")
    print(f"  Dirección: {direccion}")
    print(f"  VIP: {'Sí' if vip else 'No'}")
    print("Guardando la foto en:", ruta_imagen)

    # Preparar la respuesta
    respuesta = {
        "Nombre": nombre,
        "Dirección": direccion,
        "VIP": vip,
        "Ruta": ruta_imagen
    }
    return respuesta

@app.get("/")
def hola_mundo():
    print("Invocando a ruta /")
    respuesta = {
        "mensaje": "¡Hola, mundo!"
    }
    return respuesta

@app.get("/usuarios/{id}")
def usuario_por_id(id: int):
    print("Buscando usuario por ID:", id)
    return usuarios[id]

@app.get("/usuarios/{id}/compras/{id_compra}")
def compras_usuario_por_id(id: int, id_compra: int):
    print("Buscando compra con ID:", id_compra, " del usuario con ID:", id)
    compra = {
        "id_compra": 787,
        "producto": "TV",
        "precio": 14000,
    }
    return compra

@app.get("/usuarios")
def lista_usuarios(*, lote: int = 10, pag: int, orden: Optional[str] = None):
    print("Lote:", lote, " Página:", pag, " Orden:", orden)
    return usuarios

@app.post("/usuarios")
def guardar_usuario(
    nombre: str = Form(...), edad: int = Form(...), domicilio: str = Form(...)
):
    print("Usuario a guardar:", nombre, edad, domicilio)
    usr_nuevo = {
        "id": len(usuarios),
        "nombre": nombre,
        "edad": edad,
        "domicilio": domicilio,
    }
    usuarios.append(usr_nuevo)
    return usr_nuevo

@app.put("/usuario/{id}")
def actualizar_usuario(id: int, nombre: str = Form(...), edad: int = Form(...), domicilio: str = Form(...)):
    usr_act = usuarios[id]
    usr_act["nombre"] = nombre
    usr_act["edad"] = edad
    usr_act["domicilio"] = domicilio
    return usr_act

@app.delete("/usuario/{id}")
def borrar_usuario(id: int):
    if 0 <= id < len(usuarios):
        usuario = usuarios[id]
        usuarios.remove(usuario)
    else:
        usuario = None
    return {"status_borrado": "ok"}
