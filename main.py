from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from typing import List, Union
import mysql.connector

app = FastAPI()
PORT: int = 8080

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

def lastIndex(tabla:str, attr:str):
    query ="SELECT {} from {} order by {} desc".format(attr, tabla, attr)
    cursor = db.cursor()
    cursor.execute(query)
    record = cursor.fetchone()
    return record[0]

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=PORT)