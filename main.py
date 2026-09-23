from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="API REST de Gestión de Usuarios",
    description="Challenge 2 - API desarrollada con FastAPI",
    version="1.0.0"
)

# Base de datos en memoria (diccionario de usuarios)
usuarios_db = {}

# Token constante simulado para la autenticación
TOKEN_ABC123 = "abc123tokensecreto"

# ---------------------------------------------------------
# MODELOS DE DATOS (PYDANTIC)
# ---------------------------------------------------------

class UsuarioRegistro(BaseModel):
    username: str
    password: str
    rol: str

class UsuarioLogin(BaseModel):
    username: str
    password: str

class RolUpdate(BaseModel):
    nuevo_rol: str

# ---------------------------------------------------------
# ENDPOINTS HTTP
# ---------------------------------------------------------

# 1. POST: Registrar usuario
@app.post("/usuarios/registrar", status_code=status.HTTP_201_CREATED, tags=["Usuarios"])
def registrar_usuario_endpoint(usuario: UsuarioRegistro):
    if usuario.username in usuarios_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El usuario '{usuario.username}' ya está registrado en la aplicación."
        )
    
    usuarios_db[usuario.username] = {
        "password": usuario.password,
        "rol": usuario.rol
    }
    
    return {
        "mensaje": f"El usuario '{usuario.username}' fue registrado correctamente con el rol de '{usuario.rol}'.",
        "username": usuario.username,
        "rol": usuario.rol
    }

# 2. POST: Autenticar usuario (Login)
@app.post("/usuarios/login", tags=["Usuarios"])
def autenticar_usuario_endpoint(datos: UsuarioLogin):
    datos_usuario = usuarios_db.get(datos.username)
    
    if datos_usuario and datos_usuario["password"] == datos.password:
        return {
            "autenticado": True,
            "token": TOKEN_ABC123,
            "rol": datos_usuario["rol"],
            "mensaje": f"[EXITO] Autenticacion correcta para '{datos.username}'."
        }
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"[ERROR] credenciales no validas para el usuario '{datos.username}'."
    )

# 3. PUT: Modificar rol de usuario
@app.put("/usuarios/{username}/rol", tags=["Usuarios"])
def modificar_rol_endpoint(username: str, datos: RolUpdate):
    if username in usuarios_db:
        usuarios_db[username]["rol"] = datos.nuevo_rol
        return {
            "exito": True,
            "mensaje": f"[EXITO] Se cambio el rol del usuario '{username}' a '{datos.nuevo_rol}'.",
            "username": username,
            "nuevo_rol": datos.nuevo_rol
        }
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"[ERROR] No se pudo cambiar el rol porque el usuario '{username}' no existe."
    )

# 4. DELETE: Eliminar usuario
@app.delete("/usuarios/{username}", status_code=status.HTTP_200_OK, tags=["Usuarios"])
def eliminar_usuario_endpoint(username: str):
    if username in usuarios_db:
        del usuarios_db[username]
        return {
            "exito": True,
            "mensaje": f"[EXITO] El usuario '{username}' fue eliminado correctamente."
        }
    
    raise HTTPException(
        status_code=status.HTTP_404_NO