## Backend fastAPI

fastAPI nos ayuda de manera ágil a implimentar un backend con interacción con cualquier tipo de base de datos ya sea relacional o no-relacional. Se recomienda que para montar el presente proyecto se sigan los siguientes pasos:
- Creación de un entorno virtual, ejecuta en una terminal: **python -m venv fastapi-env**
- Activación del entorno virtual en Windows, ejecuta: **fastapi-env\Scripts\activate**
- Activación del entorno virtual en Unix o MacOS, ejecuta: **source fastapi-env/bin/activate**
- Instalación de fastapi y uvicorn, ejecuta: **pip install fastapi uvicorn**
- Instalación de mysql-connector-python, ejecuta: **pip install mysql-connector-python**
- Ejecución de fastapi, entra a la carpeta del proyecto y ejecuta: **uvicorn main:app --host 127.0.0.1 --port 8080 --reload**
