from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from typing import List, Union
import mysql.connector

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
PORT: int = 8080

# USar el siguiente Middleware sólo para pruebas locales y no en producción
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
    )

db = mysql.connector.connect(
    host="localhost",
    user="daniel",
    password="c4b3z0n4",
    database="fullcrud_db",
    consume_results=True
)

class Usuario(BaseModel):
    id_usuario: Union[int, None]=None
    usuario: str
    contrasena: str

class Persona(BaseModel):
    id_persona:Union[int, None] = None
    nombres:str
    apellidoP:str
    apellidoM:str
    fechaNac:str
    estadoCivil:str
    numhijos:int

@app.get("/")
def message():
    return {"msg": "Hola mundo desde FastAPI"}

@app.get("/usuarios")
def getUsuarios():
    usuarios = []
    query = "SELECT * FROM usuarios"
    cursor = db.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    no_regs = cursor.rowcount
    if no_regs>0:
        for record in records:
            usuario = {
                "id_usuario"    :   record[0],
                "usuario"       :   record[1],
                "contrasena"    :   record[2]
            }
            usuarios.append(usuario)
        return {"status":"ok", "msg":"Si hay usuarios", "data": usuarios} 
    else:
        return {"status":"ok", "msg":"No hay usuarios registrados"}

@app.get("/usuarios/{id}")
def getUsuarioById(id):
    query = "SELECT * FROM usuarios WHERE id_usuario={}".format(id)
    cursor = db.cursor()
    cursor.execute(query)
    record = cursor.fetchone()
    no_regs = cursor.rowcount
    if no_regs>0:
        usuario = {
            "id_usuario"    :   record[0],
            "usuario"       :   record[1],
            "contrasena"    :   record[2]
        }
        return {"status":"ok", "msg":"Si se encontró el usuario", "data": usuario} 
    else:
        return {"status":"error", "msg":"No se encontró el usuario"}

@app.post("/usuarioByUC")
def getUsuarioByUsuarioContrasena(user:Usuario):
    try:
        query = "SELECT * FROM usuarios WHERE usuario='{}' AND contrasena='{}';".format(user.usuario, user.contrasena)
        cursor = db.cursor()
        cursor.execute(query)
        record = cursor.fetchone()
        no_regs = cursor.rowcount
        if no_regs>0:
            usuario = {
                "id_usuario":  record[0],
                "usuario"   :  record[1],
                "contrasena":  record[2],
            }
            return {
                "status":"ok", 
                "msg":"Usuario encontrado", 
                "data": usuario
                }
        else:
            return {
                "status":"error", 
                "msg":"Usuario no encontrado", 
                }
    except:
        return {
                "status":"error", 
                "msg":"Ocurrio un error en la consulta", 
                }
    
@app.post("/usuarios")
def setUsuario(user: Usuario):
    query = "INSERT INTO usuarios (`usuario`, `contrasena`) VALUES ('{}', '{}')".format(user.usuario, user.contrasena)
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    return {
        "status":"ok", 
        "msg":"Usuario agregado", 
        "data": { 
            "id_usuario": lastIndex("usuarios", "id_usuario") 
            }
        }

@app.put("/usuarios")
def updateUsuario(user: Usuario):
    print("entra")
    try:
        query = "UPDATE usuarios SET usuario='{}', contrasena='{}' WHERE id_usuario={};".format(user.usuario, user.contrasena, user.id_usuario)
        print("\n->", query)
        cursor = db.cursor()
        cursor.execute(query)
        db.commit()
        return {
            "status":"ok", 
            "msg":"Usuario modificado", 
            "data": { 
                "id_usuario": user.id_usuario
                }
        }
    except:
        return {
                "status":"error", 
                "msg":"Ocurrio un error en la consulta", 
        }

@app.delete("/usuarios")
def delUsuario(user: Usuario):
    try:
        query = "DELETE from usuarios WHERE id_usuario={};".format(user.id_usuario)
        print("\n->", query)
        cursor = db.cursor()
        cursor.execute(query)
        db.commit()
        return {
            "status":"ok", 
            "msg":"Usuario eliminado", 
            "data": { 
                "id_usuario": user.id_usuario
                }
        }
    except:
        return {
                "status":"error", 
                "msg":"Ocurrio un error en el borrado del usuario", 
        }

@app.get("/personas")
def getPersonas():
    personas=[]
    query = "select * from personas;"
    cursor = db.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    no_res = cursor.rowcount
    if no_res > 0:
        for record in records:
            persona = {
                "id_persona" : record[0],
                "nombres": record[1],
                "apellidoP" : record[2],
                "apellidoM" : record[3],
                "fechaNac" : record[4],
                "estadoCivil" : record[5],
                "numhijos" : record[6],
            }
            personas.append(persona)
        return {"status": "ok", "msg": "Si hay personas registrados", "data": personas}
    else:
        return {"status":"ok", "msg": "No hay personas registradas"}

@app.post("/personas")
def setUsuarios(per:Persona):
    query = "insert into personas (`nombre`, `apaterno`, `amaterno`, `fechanac`, `edocivil`, `no_hijos`) values ('{}','{}','{}','{}','{}','{}')".format(per.nombres, per.apellidoP, per.apellidoM, per.fechaNac, per.estadoCivil, per.numhijos)
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    return {"status": "ok", "msg": "Persona Agregada",
            "data": {
                "id_persona": lastIndex("personas", "id_persona")
            }}

def lastIndex(tabla:str, attr:str):
    query ="SELECT {} from {} order by {} desc".format(attr, tabla, attr)
    cursor = db.cursor()
    cursor.execute(query)
    record = cursor.fetchone()
    return record[0]

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=PORT)